import sys
import os
from antlr4 import *
from antlr4.tree.Trees import Trees
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser
from antlr4.error.ErrorListener import ErrorListener
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import re


class CustomErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.error_messages = set()  # Ahora es un conjunto para evitar duplicados

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Asegúrate de que cada mensaje de error sea único
        if "missing ')' at" in msg or (
            "mismatched input" in msg and offendingSymbol.text == "("
        ):
            error_msg = f"Linea {line}:{column} Error: parentesis sin cerrar"
        elif "extraneous input" in msg and offendingSymbol.text == ")":
            error_msg = f"Linea {line}:{column} Error: parentesis sin abrir"
        elif "no viable alternative" in msg:
            error_msg = f"Linea {line}:{column} Error: token no reconocido '{offendingSymbol.text}'"
        elif "mismatched input" in msg and offendingSymbol.text in ["+", "-", "*", "/"]:
            error_msg = f"Linea {line}:{column} Error: No hay operadores que debe contener el lenguaje"
        elif "token recognition error at" in msg:
            error_msg = f"Linea {line}:{column} Error: operador no puede estar al inicio de la cadena"
        elif "missing NEWLINE at '<EOF>'" in msg:
            error_msg = f"Linea {line}:{column} Error: se esperaba un salto de línea al final de la entrada"
        elif "extraneous input '\\r\\n' expecting {'(', INT}" in msg:
            error_msg = f"Linea {line}:{column} Error: Para iniciar una linea de texto debe empezar con un numero o abriendo un parentesis"
        elif "extraneous input 'class' expecting" in msg:
            error_msg = f"Linea {line}:{column} Error: Entrada inesperada 'class', se esperaba '}}' o OBJECT_ID"
        elif "missing ';' at 'else'" in msg:
            error_msg = f"Linea {line}:{column} Error: Falta ';' después de 'else'"
        elif "missing '<-' at" in msg:
            error_msg = f"Linea {line}:{column} Error: Falta '<-' en la asignación"
        elif "mismatched input '<EOF>' expecting ';'" in msg:
            error_msg = f"Linea {line}:{column} Error: Se esperaba ';' antes de finalizar el archivo"
        elif "missing 'fi' at ';'" in msg:
            error_msg = f"Linea {line}:{column} Error: Falta 'fi' antes de ';'"
        elif "missing ';' at 'secondMethod'" in msg:
            error_msg = (
                f"Linea {line}:{column} Error: Falta ';' después de 'secondMethod'"
            )
        elif "extraneous input '}' expecting ';'" in msg:
            error_msg = (
                f"Linea {line}:{column} Error: Entrada inesperada se esperaba ';'"
            )
        elif "mismatched input ';' expecting" in msg:
            error_msg = f"Linea {line}:{column} Error: Entrada inesperada ';', se esperaban otros tokens"
        elif "Error: token no reconocido 'String'" in msg:
            error_msg = f"Linea {line}:{column} Error: token no reconocido 'String'"
        elif "extraneous input ';' expecting" in msg:
            error_msg = f"Linea {line}:{column} Error: Entrada inesperada ';', se esperaba '{{', '}}', 'if', 'while', 'return', o OBJECT_ID"
        else:
            error_msg = f"Linea {line}:{column} {msg}"

        self.error_messages.add(error_msg)


def plot_tree(parser, tree):
    def build_node(node, parent=None):
        node_type = type(node).__name__

        if isinstance(node, TerminalNode):
            label = Trees.getNodeText(node, parser)
        else:
            label = (
                node_type.split("Context")[0]
                if node_type.endswith("Context")
                else node_type
            )

        # Ignore empty nodes
        if label.strip() == "":
            return None

        # Prepare label for Graphviz
        label = label.replace('"', '\\"').replace(" ", "_")

        label_with_id = label + f"_{id(node)}"
        any_node = Node(label_with_id, parent=parent, displayed_label=label)

        if not isinstance(node, TerminalNode):
            for i in range(node.getChildCount()):
                child = node.getChild(i)
                child_node = build_node(child, any_node)
                if child_node is None:
                    continue

        return any_node

    root = build_node(tree)
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.displayed_label))

    DotExporter(
        root,
        nodeattrfunc=lambda node: 'label="%s"' % node.displayed_label.replace(" ", "_"),
    ).to_dotfile("tree.dot")

    with open("tree.dot", "r") as f:
        content = f.readlines()

    attributes = ["rankdir=TB;\n", "nodesep=0.6;\n", "ranksep=0.8;\n"]
    content[1:1] = attributes

    with open("tree.dot", "w") as f:
        f.writelines(content)

    os.system("dot -Tpng tree.dot -o tree.png")


class SymbolTable:
    def __init__(self):
        self.table = {}

    def add_symbol(self, name, type, scope):
        self.table[name] = {"type": type, "scope": scope}

    def lookup_symbol(self, name):
        return self.table.get(name, None)

    def print_table(self):
        for name, info in self.table.items():
            print(f"{name} -> {info}")


class MyYAPLListener(ParseTreeListener):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def enterClassDef(self, ctx):
        type_ids = ctx.TYPE_ID()
        if isinstance(type_ids, list):
            for type_id in type_ids:
                self.symbol_table.add_symbol(type_id.getText(), "ClassType", "global")
        else:
            self.symbol_table.add_symbol(type_ids.getText(), "ClassType", "global")

    def enterFeature(self, ctx):
        object_ids = ctx.OBJECT_ID()
        type_ids = ctx.TYPE_ID()
        if isinstance(object_ids, list):
            for object_id, type_id in zip(object_ids, type_ids):
                self.symbol_table.add_symbol(
                    object_id.getText(), type_id.getText(), "global"
                )
        else:
            self.symbol_table.add_symbol(
                object_ids.getText(), type_ids.getText(), "global"
            )

    def enterFormal(self, ctx):
        object_ids = ctx.OBJECT_ID()
        type_ids = ctx.TYPE_ID()
        if isinstance(object_ids, list):
            for object_id, type_id in zip(object_ids, type_ids):
                self.symbol_table.add_symbol(
                    object_id.getText(), type_id.getText(), "local"
                )
        else:
            self.symbol_table.add_symbol(
                object_ids.getText(), type_ids.getText(), "local"
            )

    def exitProgram(self, ctx):
        self.symbol_table.print_table()


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = YAPLLexer(input_stream)
    stream = CommonTokenStream(lexer)

    error_listener = CustomErrorListener()

    parser = YAPLParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    try:
        tree = parser.program()

        if parser.getNumberOfSyntaxErrors() > 0:
            print("Se detectaron los siguientes errores:")
            for error in error_listener.error_messages:
                print(error)
            print("Finalizando el programa.")
            return

        print(Trees.toStringTree(tree, None, parser))

        listener = MyYAPLListener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        plot_tree(parser, tree)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)

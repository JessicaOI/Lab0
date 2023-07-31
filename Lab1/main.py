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


class Method:
    def __init__(self, name, return_type, params):
        self.name = name
        self.return_type = return_type
        self.params = params  # This is a list of Symbols


class Attribute:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Symbol:
    def __init__(self, name, type, methods=[], attributes=[]):
        self.name = name
        self.type = type
        self.methods = methods
        self.attributes = attributes


class SymbolTable:
    def __init__(self, type_system):
        self.symbols = {}
        self.scope = "global"
        self.type_system = type_system

        # Initialize predefined types and methods
        self.symbols["Int"] = Symbol(
            "Int", "class", attributes=[Attribute("value", "Int")]
        )
        self.symbols["String"] = Symbol(
            "String", "class", attributes=[Attribute("value", "String")]
        )
        self.symbols["Bool"] = Symbol(
            "Bool", "class", attributes=[Attribute("value", "Bool")]
        )
        self.symbols["IO"] = Symbol("IO", "class")

    def add_symbol(self, symbol):
        if symbol.name in self.symbols:
            raise Exception(f"Symbol {symbol.name} already exists.")
        if not self.type_system.check_type(symbol.type):
            raise Exception(f"Type {symbol.type} is not supported.")
        self.symbols[symbol.name] = symbol

    def get_symbol(self, name):
        return self.symbols.get(name, None)

    def add_method(self, class_name, method):
        class_symbol = self.get_symbol(class_name)
        if not class_symbol:
            raise Exception(f"Class {class_name} does not exist.")
        for m in class_symbol.methods:
            if m.name == method.name:
                raise Exception(f"Method {method.name} already exists in {class_name}.")
        class_symbol.methods.append(method)

    def get_method(self, class_name, method_name):
        class_symbol = self.get_symbol(class_name)
        if not class_symbol:
            raise Exception(f"Class {class_name} does not exist.")
        for method in class_symbol.methods:
            if method.name == method_name:
                return method
        return None

    def add_attribute(self, class_name, attribute):
        class_symbol = self.get_symbol(class_name)
        if not class_symbol:
            raise Exception(f"Class {class_name} does not exist.")
        for a in class_symbol.attributes:
            if a.name == attribute.name:
                raise Exception(
                    f"Attribute {attribute.name} already exists in {class_name}."
                )
        class_symbol.attributes.append(attribute)

    def get_attribute(self, class_name, attr_name):
        class_symbol = self.get_symbol(class_name)
        if not class_symbol:
            raise Exception(f"Class {class_name} does not exist.")
        for attribute in class_symbol.attributes:
            if attribute.name == attr_name:
                return attribute
        return None

    def enter_scope(self, class_name):
        if self.scope != "global":
            raise Exception("Can't enter a new scope before exiting the current one.")
        self.scope = class_name

    def exit_scope(self):
        self.scope = "global"


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

        plot_tree(parser, tree)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)

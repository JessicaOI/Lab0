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
from tabulate import tabulate


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


class Symbol:
    def __init__(
        self,
        name,
        type,
        scope,
        lexeme,
        token,
        memory_pos,
        line_num,
        line_pos,
        semantic_type,
        num_params,
        param_types,
        pass_method,
    ):
        self.name = name
        self.type = type
        self.scope = scope
        self.lexeme = lexeme
        self.token = token
        self.memory_pos = memory_pos
        self.line_num = line_num
        self.line_pos = line_pos
        self.semantic_type = semantic_type
        self.num_params = num_params
        self.param_types = param_types
        self.pass_method = pass_method


class SymbolTable:
    def __init__(self):
        self.symbols = []

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def print_table(self):
        for symbol in self.symbols:
            print(
                f"Name: {symbol.name}, Tipo de Dato: {symbol.type}, Scope: {symbol.scope}, Lexema: {symbol.lexeme}, Token: {symbol.token}, Memory Pos: {symbol.memory_pos}, Line Num: {symbol.line_num}, Line Pos: {symbol.line_pos}, Tipo Semantico: {symbol.semantic_type}, Num Params: {symbol.num_params}, Tipo de Parametros: {symbol.param_types}, Metodo para paso de parámetros: {symbol.pass_method}"
            )

    def symbol_exists(self, name, scope):
        return any(
            symbol.name == name and symbol.scope == scope for symbol in self.symbols
        )


class MyYAPLListener(ParseTreeListener):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_scope = "global"
        self.current_memory_position = 0
        self.table = []
        self.main_class_found = (
            False  # Para verificar si se encuentra una clase MainClass
        )
        self.main_found = False  # Para verificar si se encuentra una clase Main
        self.main_method_in_main_class_found = (
            False  # Para verificar si se encuentra un método mainMethod en MainClass
        )
        self.main_method_in_main_found = (
            False  # Para verificar si se encuentra un método main en Main
        )

    def enterClassDef(self, ctx):
        type_ids = ctx.TYPE_ID() if isinstance(ctx.TYPE_ID(), list) else [ctx.TYPE_ID()]
        for type_id in type_ids:
            type_id = type_id.getText()
            class_name = ctx.TYPE_ID()[0].getText()
            # <-- Verificación aquí: Comprobar si el nombre de la clase es "Main"
            if class_name == "MainClass":
                self.main_class_found = True
            elif class_name == "Main":
                self.main_found = True
            symbol = Symbol(
                name=type_id,
                type="ClassType",
                scope=self.current_scope,
                lexeme=type_id,
                token="ClassType",
                memory_pos=self.current_memory_position,
                line_num=ctx.start.line,
                line_pos=ctx.start.column,
                semantic_type="ClassType",
                num_params=0,
                param_types=[],
                pass_method="byValue",
            )
            self.symbol_table.add_symbol(symbol)
            self.current_memory_position += 1
            self.table.append(list(symbol.__dict__.values()))
        self.current_scope = type_ids[0].getText()

    def exitClassDef(self, ctx):
        self.current_scope = "global"

    def enterFeature(self, ctx):
        object_ids = (
            ctx.OBJECT_ID() if isinstance(ctx.OBJECT_ID(), list) else [ctx.OBJECT_ID()]
        )
        type_ids = ctx.TYPE_ID() if isinstance(ctx.TYPE_ID(), list) else [ctx.TYPE_ID()]
        for object_id, type_id in zip(object_ids, type_ids):
            object_id = object_id.getText()
            type_id = type_id.getText()
            symbol = Symbol(
                name=object_id,
                type="Feature",
                scope=self.current_scope,
                lexeme=object_id,
                token="Feature",
                memory_pos=self.current_memory_position,
                line_num=ctx.start.line,
                line_pos=ctx.start.column,
                semantic_type=type_id,
                num_params=0,
                param_types=[],
                pass_method="byValue",
            )
            if self.symbol_table.symbol_exists(object_id, self.current_scope):
                print(
                    f"Error en línea {ctx.start.line}: La variable {object_id} ya ha sido declarada en este ámbito."
                )
                return
            self.symbol_table.add_symbol(symbol)
            self.current_memory_position += 1
            self.table.append(list(symbol.__dict__.values()))

    def enterFormal(self, ctx):
        object_ids = (
            ctx.OBJECT_ID() if isinstance(ctx.OBJECT_ID(), list) else [ctx.OBJECT_ID()]
        )
        type_ids = ctx.TYPE_ID() if isinstance(ctx.TYPE_ID(), list) else [ctx.TYPE_ID()]
        for object_id, type_id in zip(object_ids, type_ids):
            object_id = object_id.getText()
            type_id = type_id.getText()
            symbol = Symbol(
                name=object_id,
                type="Formal",
                scope=self.current_scope,
                lexeme=object_id,
                token="Formal",
                memory_pos=self.current_memory_position,
                line_num=ctx.start.line,
                line_pos=ctx.start.column,
                semantic_type=type_id,
                num_params=0,
                param_types=[],
                pass_method="byValue",
            )
            self.symbol_table.add_symbol(symbol)
            self.current_memory_position += 1
            self.table.append(list(symbol.__dict__.values()))

    def enterMethodDef(self, ctx):
        method_name = (
            ctx.method_name.getText()
        )  # Suponiendo que `method_name` es cómo obtienes el nombre del método en tu gramática
        return_type = (
            ctx.return_type.getText()
        )  # Suponiendo que `return_type` es cómo obtienes el tipo de retorno en tu gramática

        formal_params = []
        if (
            ctx.formal_params
        ):  # Suponiendo que `formal_params` es cómo obtienes los parámetros formales
            for param in ctx.formal_params:
                param_type = param.param_type.getText()
                param_name = param.param_name.getText()
                formal_params.append((param_type, param_name))

        # Comprobación para MainClass
        if self.current_scope == "MainClass" and method_name == "mainMethod":
            self.main_method_in_main_class_found = True

        # Comprobación para Main
        if self.current_scope == "Main" and method_name == "main":
            self.main_method_in_main_found = True
            if len(formal_params) > 0:
                print(
                    "Error: el método main en la clase Main no debe tener parámetros."
                )

        # Agregando el método a la tabla de símbolos
        symbol = Symbol(
            name=method_name,
            type_=return_type,
            scope=self.current_scope,
            formal_params=formal_params
            # Añadir cualquier otro atributo necesario
        )
        self.symbol_table.add_symbol(symbol)
        self.current_memory_position += 1
        self.table.append(list(symbol.__dict__.values()))

        # Cambiar el alcance actual al método que estamos visitando
        self.current_scope = f"{self.current_scope}.{method_name}"

    def exitProgram(self, ctx):

        if not self.main_class_found and not self.main_found:
            print("Error: No se ha encontrado ni la clase MainClass ni la clase Main.")
        elif self.main_class_found and not self.main_method_in_main_class_found:
            print(
                "Error: No se ha encontrado el método mainMethod en la clase MainClass."
            )
        elif self.main_found and not self.main_method_in_main_found:
            print("Error: No se ha encontrado el método main en la clase Main.")

        headers = [
            "Name",
            "Tipo de Dato",
            "Scope",
            "Lexema",
            "Token",
            "Memory Pos",
            "Line Num",
            "Line Pos",
            "Tipo Semantico",
            "Num Params",
            "Tipo de Parametros",
            "Metodo para paso de parámetros",
        ]
        print(tabulate(self.table, headers=headers))


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

        listener = MyYAPLListener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)

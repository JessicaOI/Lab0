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
import tkinter as tk
from tkinter import filedialog, messagebox, Text, simpledialog

text_editor = None

def initialize_text_editor(root, content):
    global text_editor

    # Crear el botón y agregarlo a la interfaz
    execute_button = tk.Button(root, text="Ejecutar Validaciones", command=execute_functions)
    execute_button.pack(pady=10)

    # Crear el editor de texto y llenarlo con el contenido del archivo
    text_editor = Text(root, wrap=tk.WORD)
    text_editor.insert(tk.END, content)
    text_editor.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)




def select_file(root):
    global file_path
    file_path = filedialog.askopenfilename()
    
    if not file_path:
        return

    with open(file_path, 'r') as file:
        content = file.read()

    initialize_text_editor(root, content)  # Inicializar el editor de texto después de seleccionar un archivo


def validate_content():
    global text_editor, file_path  # Agregamos file_path a las variables globales aquí
    content = text_editor.get(1.0, tk.END).strip()
    
    
    # Ahora en lugar de escribir en un archivo temporal, escribimos en el archivo seleccionado
    with open(file_path, "w") as file:
        file.write(content)

    # Asumiendo que main() es la función que realiza la validación con ANTLR
    main(file_path)

def execute_functions():
    global file_path
    try:
        # Aquí debes llamar a tus funciones de análisis sintáctico, creación de tabla de símbolos, y validaciones semánticas
        # Por ejemplo:
        # sintactic_analysis_function()
        # symbol_table_creation_function()
        # semantic_validations_function()

        input_stream = FileStream(file_path)
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
        
        print("Todas las funcionalidades se ejecutaron correctamente.")
    except Exception as e:
        print(f"Error: {e}")

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

    # def add_symbol(self, symbol):
    #     self.symbols.append(symbol)

    def print_table(self):
        for symbol in self.symbols:
            print(
                f"Name: {symbol.name}, Tipo de Dato: {symbol.type}, Scope: {symbol.scope}, Lexema: {symbol.lexeme}, Token: {symbol.token}, Memory Pos: {symbol.memory_pos}, Line Num: {symbol.line_num}, Line Pos: {symbol.line_pos}, Tipo Semantico: {symbol.semantic_type}, Num Params: {symbol.num_params}, Tipo de Parametros: {symbol.param_types}, Metodo para paso de parámetros: {symbol.pass_method}"
            )

    def check_duplicate(self, symbol_name, scope):
        for symbol in self.symbols:
            if symbol.name == symbol_name and symbol.scope == scope:
                raise ValueError(f"Error: Variable duplicada '{symbol_name}' en el scope '{scope}'")

    def add_symbol(self, symbol):
        self.check_duplicate(symbol.name, symbol.scope)
        self.symbols.append(symbol)

    def is_declared(self, symbol_name, scope):
        for symbol in self.symbols:
            if symbol.name == symbol_name and symbol.scope == scope:
                return True
        return False


class MyYAPLListener(ParseTreeListener):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_scope = "global"
        self.current_memory_position = 0
        self.table = []

    def enterClassDef(self, ctx):
        type_ids = ctx.TYPE_ID() if isinstance(ctx.TYPE_ID(), list) else [ctx.TYPE_ID()]
        for type_id in type_ids:
            type_id = type_id.getText()
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

    def exitProgram(self, ctx):
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

    def enterVariableAccess(self, ctx):
        var_name = ctx.OBJECT_ID().getText()
        if not self.symbol_table.is_declared(var_name, self.current_scope):
            raise ValueError(f"Error: Uso de variable no declarada '{var_name}'")



def main(argv):
    global text_editor

    # Inicializar la ventana principal
    root = tk.Tk()
    root.title("YAPL Validator GUI")
    root.geometry("600x400")

    # Esto abrirá el cuadro de diálogo de selección de archivo tan pronto como se inicie la aplicación
    select_file(root)  # Añadimos esto aquí

    menu = tk.Menu(root)
    root.config(menu=menu)
    file_menu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)

    # Agregar acciones al menú File
    file_menu.add_command(label="Open...", command=select_file)  # Modificamos el comando aquí

    root.mainloop()

    # input_stream = FileStream(argv[1])
    # lexer = YAPLLexer(input_stream)
    # stream = CommonTokenStream(lexer)

    # error_listener = CustomErrorListener()

    # parser = YAPLParser(stream)
    # parser.removeErrorListeners()
    # parser.addErrorListener(error_listener)

    # try:
    #     tree = parser.program()

    #     if parser.getNumberOfSyntaxErrors() > 0:
    #         print("Se detectaron los siguientes errores:")
    #         for error in error_listener.error_messages:
    #             print(error)
    #         print("Finalizando el programa.")
    #         return

    #     print(Trees.toStringTree(tree, None, parser))

    #     plot_tree(parser, tree)

    #     listener = MyYAPLListener()
    #     walker = ParseTreeWalker()
    #     walker.walk(listener, tree)

    # except Exception as e:
    #     print(e)

    
if __name__ == "__main__":
    main(sys.argv)

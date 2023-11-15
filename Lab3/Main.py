import sys
import os
from antlr4 import *
from antlr4.tree.Trees import Trees
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser
from YAPLListener import YAPLListener
from antlr4.error.ErrorListener import ErrorListener
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import re
from tabulate import tabulate
from copy import deepcopy
import tkinter as tk
from tkinter import filedialog, messagebox, Text, simpledialog
import inspect
import traceback
import os

# ---------------------GUI------------------------------------------------------------
text_editor = None
console = None

# Se crear el el GUI el espacio del editor de texto
def redraw_line_numbers(canvas, text_widget):
    canvas.delete("all")  # limpiamos todo lo que estaba dibujado anteriormente

    i = text_widget.index("@0,0")
    while True:
        dline = text_widget.dlineinfo(i)
        if dline is None:
            break
        y = dline[1]
        linenum = str(i).split(".")[0]
        canvas.create_text(2, y, anchor="nw", text=linenum, fill="black")
        i = text_widget.index("%s+1line" % i)


def initialize_text_editor(root, content):
    global text_editor, line_numbers_canvas

    execute_button = tk.Button(
        root, text="Ejecutar Validaciones", command=execute_functions
    )
    execute_button.pack(pady=10)

    editor_frame = tk.Frame(root)
    editor_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    line_numbers_canvas = tk.Canvas(editor_frame, width=30, bg="lightgrey")
    line_numbers_canvas.pack(side=tk.LEFT, fill=tk.Y)

    text_editor = Text(editor_frame, wrap=tk.WORD)
    text_editor.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
    text_editor.insert(tk.END, content)

    text_editor.bind(
        "<KeyRelease>",
        lambda event: redraw_line_numbers(line_numbers_canvas, text_editor),
    )
    text_editor.bind(
        "<MouseWheel>",
        lambda event: redraw_line_numbers(line_numbers_canvas, text_editor),
    )
    redraw_line_numbers(
        line_numbers_canvas, text_editor
    )  # Inicializar números de línea


# Se crea en el GUI la ventana que permite al usuario seleccionar un archivo
def select_file(root):
    global file_path
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    with open(file_path, "r") as file:
        content = file.read()

    initialize_text_editor(
        root, content
    )  # Inicializar el editor de texto después de seleccionar un archivo


# Guardar cambios en el archivo abierto en el text editor
def save_file():
    global file_path  # Suponiendo que tienes una variable global que guarda la ruta del archivo actual
    with open(file_path, "w") as file:
        content = text_editor.get(1.0, tk.END)
        file.write(content)


# A la hora de cerrar el programa preguntar si se quieren guardar los cambios
def on_closing(root):
    # Verifica si el contenido ha sido modificado
    if text_editor.edit_modified():
        answer = messagebox.askyesnocancel(
            "Guardar", "¿Desea guardar los cambios antes de salir?"
        )
        if answer == True:
            save_file()
            root.destroy()
        elif answer == False:
            root.destroy()
    else:
        root.destroy()


def save_to_file(codigo_intermedio, filename="codigo_intermedio.txt"):
    with open(filename, "w") as file:
        file.write(codigo_intermedio)


# Se crea la consola del GUI
def initialize_console(root):
    global console

    # 1. Crea un frame que contenga tanto al widget Text como al Scrollbar.
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    # 2. Crear el Scrollbar horizontal.
    h_scroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL)

    # 3. Crear el widget Text y configurarlo para usar el Scrollbar.
    console = tk.Text(
        frame, bg="black", fg="white", wrap=tk.NONE, xscrollcommand=h_scroll.set
    )

    # 4. Configurar el Scrollbar para comunicarse con el widget Text.
    h_scroll.config(command=console.xview)

    # 5. Empaquetar el widget Text y el Scrollbar en el frame.
    console.pack(expand=True, fill=tk.BOTH)  # Nota que eliminamos 'side=tk.LEFT'
    h_scroll.pack(fill=tk.X)  # Nota que también eliminamos 'side=tk.BOTTOM'


# Redirigir lo que normalmente se imprime en la consola de visual al programa con GUI
class IOWrapper:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Auto-scroll

    def flush(self):
        pass


# Al presionar el boton se ejecuta el programa en el GUI
def execute_functions():
    global file_path
    global codigo_intermedio

    try:
        input_stream = FileStream(file_path, encoding="latin1")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        print("Finalizando el programa debido a un error inesperado.")
        return

    error_listener = CustomErrorListener()

    lexer = CustomYAPLLexer(input_stream, error_listener)

    # Creamos un stream para análisis léxico
    lex_stream = CommonTokenStream(lexer)
    lex_stream.fill()  # Esto llenará el stream y recolectará los tokens y posibles errores léxicos

    if len(error_listener.error_messages) > 0:
        print("\nSe detectaron los siguientes errores léxicos:")
        for error in error_listener.error_messages:
            print(error)
        print("Finalizando el programa debido a errores léxicos.")
        return

    # Restablecemos el lexer y creamos un nuevo stream para análisis sintáctico
    lexer.reset()
    syn_stream = CommonTokenStream(lexer)
    parser = YAPLParser(syn_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    # Analizamos el programa (esto puede generar errores sintácticos)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("\nSe detectaron los siguientes errores sintácticos:")
        for error in error_listener.error_messages:
            print(error)
        print("Finalizando el programa debido a errores sintácticos.")
        return

    # Si llegamos aquí, no hay errores léxicos ni sintácticos
    #print("Análisis léxico y sintáctico completado sin errores.")

    try:
        plot_tree(parser, tree)

        # Camina por el árbol incluso si hay errores sintácticos
        listener = MyYAPLListener()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        # Ahora, al final, verifica e imprime todos los errores detectados
        if parser.getNumberOfSyntaxErrors() > 0 or len(listener.semantic_errors) > 0:
            print("Se detectaron los siguientes errores:")

            for error in error_listener.error_messages:
                print("Error Sintáctico: " + error)

            for error in listener.semantic_errors:
                print("Error Semántico: " + error)

            print("Finalizando el programa.")
            return

        # Usando el Generador
        generador = GeneradorCodigoIntermedio()
        walker.walk(
            generador, tree
        )  # Utilizamos el walker con el GeneradorCodigoIntermedio
        codigo_intermedio = generador.get_codigo_intermedio()
        generador.imprimir_codigo_intermedio()
        # Uso de la clase mips
        translator = IntermediateToMIPS(listener.symbol_table)
        mips_code = translator.generate_code(codigo_intermedio)  # 'your_intermediate_code' es el código intermedio que has proporcionado
        translator.save_mips_to_file(mips_code, "mi_archivo_mips.txt")

        # Guarda el código intermedio en un archivo
        save_to_file(codigo_intermedio)

    except Exception as e:  # Captura otras excepciones para asegurar una salida limpia

        print(f"Error: {e}")
        traceback.print_exc()  # Imprime la traza completa del error
        print("Finalizando el programa debido a un error inesperado.")


# -------------------------------------Fin GUI------------------------------------
class LexicalError(Exception):
    pass


# ---------------------Analisis lexico--------------------------------------------
class CustomYAPLLexer(YAPLLexer):
    def __init__(self, input_stream, error_listener=None):
        super().__init__(input_stream)
        self._error_listener = error_listener

    def recover(self, re):
        position = self._tokenStartCharIndex
        line = self._tokenStartLine
        column = position - self._tokenStartColumn
        offending_token = self._input.getText(
            self._tokenStartCharIndex, self._input.index
        )
        msg = f"Token no reconocido: {offending_token}"
        if self._error_listener:
            self._error_listener.lexicalError(line, column, msg)
        else:
            print(f"Linea {line}:{column} {msg}")
        super().recover(re)


# ---------------------Fin Analisis lexico--------------------------------------------

# ----------------------Analisis sintanctico--------------------------------------
# Mensajes de error personalizados
class CustomErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.error_messages = set()

    def lexicalError(self, line, column, msg):
        error_msg = f"Linea {line}:{column} Error Lexico: {msg}"
        self.error_messages.add(error_msg)

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
        elif "no viable alternative at input 'IO.'" in msg:
            error_msg = f"Linea {line}:{column} Error: Método de IO no definido o incorrecto"
        elif "mismatched input" in msg and "expecting {'Int', 'String', 'Bool'}" in msg:
            error_msg = f"Linea {line}:{column} Error: Tipo incorrecto para el método de IO"
        elif "call to undefined function" in msg:
            error_msg = f"Linea {line}:{column} Error: Llamada a función no definida en IO"

        else:
            # Ignora errores específicos relacionados con la clase 'IO'
            if "mismatched input '<EOF>' expecting {'class', 'IO'}" in msg:
                return
            else:
                error_msg = f"Linea {line}:{column} {msg}"

        self.error_messages.add(error_msg)


# Arbol
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

    #---------Imprimir Arbol de analisis sintactico-------
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


# ----------------------Fin analisis sintanctico--------------------------------------

class SymbolType:
    CLASS = 'Class'
    FUNCTION = 'Function'
    VARIABLE = 'Variable'
    PARAMETER = 'Parameter'

# -------------------------Declaraciones Tabla de simbolos----------------------------
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
        parent_class=None,
        default_value=None,
        byte_size=None,
        # value=None,
        symbol_type=None,
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
        self.parent_class = parent_class
        self.default_value = default_value
        self.byte_size = byte_size
        # self.value = value
        self.symbol_type = symbol_type


class SymbolTable:
    def __init__(self):
        self.symbols = []
        self.class_inheritance = (
            {}
        )  # Este diccionario mapeará una clase a su clase base, si es que hereda de alguna.

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def print_table(self):
        # Limpiar la consola antes de imprimir
        os.system("clear" if os.name == "posix" else "cls")

        headers = [
            "Name",
            "Type",
            "Scope",
            "Lexeme",
            "Token",
            "Memory Pos",
            "Line Num",
            "Line Pos",
            "Semantic Type",
            "Num params",
            "Param Types",
            "Pass Method",
            "Parent Class",
            "Default Value",
            "Byte Size",
            # "Value",
            "Symbol Type",
        ]
        table_data = []
        for symbol in self.symbols:
            # Agrega 'symbol.symbol_type' a la lista de valores de cada símbolo
            symbol_data = list(symbol.__dict__.values())
            #print(symbol_data)
            #symbol_data.append(getattr(symbol, 'symbol_type', 'N/A'))  # Añade symbol_type o 'N/A' si no está presente
            table_data.append(symbol_data)

        print(tabulate(table_data, headers=headers, tablefmt="pretty"))

    def symbol_exists(self, name, scope):
        return any(
            symbol.name == name and symbol.scope == scope for symbol in self.symbols
        )

    def add_inheritance(self, derived, base):
        self.class_inheritance[derived] = base

        # Copiar el tamaño de la clase base al alcance de la clase derivada
        base_size = self.get_total_class_size(base)
        for symbol in self.symbols:
            if symbol.name == derived and symbol.scope == derived:
                symbol.byte_size = base_size
                break

    def symbol_exists_with_inheritance(self, name, scope):
        # Verifica primero en el alcance dado
        if any(
            symbol.name == name and symbol.scope == scope for symbol in self.symbols
        ):
            # print(f"{name} encontrado en {scope}")  # Debugging line
            return True

        # Verifica en clases base (si existen)
        while scope in self.class_inheritance:
            scope = self.class_inheritance[scope]
            if any(
                symbol.name == name and symbol.scope == scope for symbol in self.symbols
            ):
                # print(f"{name} encontrado en la clase base {scope}")  # Debugging line
                return True

        print(
            f"{name} no encontrado en ninguna parte desde el alcance inicial {scope}"
        )  # Debugging line
        return False

    def get_symbol(self, name, scope):
        for symbol in self.symbols:
            if symbol.name == name and symbol.scope == scope:
                return symbol
        return None  # Retorna None si no se encuentra el símbolo

    def is_subtype(self, subtype, supertype):
        # Verificar si subtype es un subtipo válido de supertype
        # Esto puede involucrar buscar en la jerarquía de herencia de clases
        while subtype in self.class_inheritance:
            if subtype == supertype:
                return True
            subtype = self.class_inheritance[subtype]
        return False

    # -------------------------Funciones para controlar herencia--------------------------------------

    def get_symbol_with_inheritance(self, name, scope):
        # Verifica primero en el alcance dado
        for symbol in self.symbols:
            if symbol.name == name and symbol.scope == scope:
                return symbol

        # Verifica en clases base (si existen)
        while scope in self.class_inheritance:
            scope = self.class_inheritance[scope]
            for symbol in self.symbols:
                if symbol.name == name and symbol.scope == scope:
                    return symbol

        return None  # Retorna None si no se encuentra el símbolo

    def get_parent_class(self, class_name):
        """Devuelve el nombre de la clase padre de class_name, si es que tiene una."""
        return self.class_inheritance.get(class_name, None)

    def get_class_size(self, class_name):
        """Obtiene el tamaño de una clase específica, sin incluir el tamaño de sus clases padre."""
        for symbol in self.symbols:
            if symbol.name == class_name and symbol.type == "ClassType":
                return symbol.byte_size
        return 0  # Retorna 0 si no se encuentra la clase

    def get_total_class_size(self, class_name):
        """Obtiene el tamaño total de una clase, incluyendo el tamaño de sus clases padre."""
        total_size = 0
        current_class = class_name
        while current_class:
            total_size += self.get_class_size(current_class)
            # Obtener la clase padre de current_class
            current_class = self.get_parent_class(current_class)
        return total_size

    def update_class_size(self, class_name, added_size):
        classes_to_update = [class_name] + self.get_derived_classes(class_name)

        for class_to_update in classes_to_update:
            # Buscar el símbolo en la lista symbols
            symbol = next(
                (
                    s
                    for s in self.symbols
                    if s.name == class_to_update and s.type == "ClassType"
                ),
                None,
            )
            if symbol:
                # Inicializar el byte_size si es None
                if symbol.byte_size is None:
                    symbol.byte_size = 0
                # Sumar el added_size
                symbol.byte_size += added_size
                # Agregar el tamaño de la clase base si está heredando de alguna
                if (
                    class_to_update in self.class_inheritance
                    and symbol.byte_size is not None
                ):
                    base_class_name = self.class_inheritance[class_to_update]
                    base_class_size = self.get_total_class_size(base_class_name)
                    symbol.byte_size += base_class_size

    def get_derived_classes(self, base_class):
        return [
            derived
            for derived, base in self.class_inheritance.items()
            if base == base_class
        ]

    def set_inheritance(self, derived_class_name, base_class_name):
        base_class_size = next(
            (
                sym.byte_size
                for sym in self.symbols
                if sym.name == base_class_name and sym.type == "ClassType"
            ),
            0,
        )

        for symbol in self.symbols:
            if symbol.name == derived_class_name and symbol.type == "ClassType":
                if symbol.byte_size is None:
                    symbol.byte_size = 0
                symbol.byte_size += base_class_size
                break

    # -------------------------Termina funciones para controlar herencia--------------------------------------


# -------------------------Fin declaraciones tabla de simbolos------------------------------------------

# -------------------------Analisis Semantico---------------------------------------------
class MyYAPLListener(YAPLListener):
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
        # Almacenar todos los errores semanticos
        self.semantic_errors = []
        # Regla-Tipos de datos: Tipos basicos
        self.basic_types = {"Int", "String", "Bool"}
        self.has_class = False
        self.has_attribute = False
        self.has_method = False
        self.type_size_map = {
            "Int": 4,  # Suponiendo que un entero ocupa 4 bytes
            "String": 256,  # Suponiendo que un carácter en una cadena ocupa 1 byte
            "Bool": 1,  # Suponiendo que un booleano ocupa 1 byte
        }
        self.variable_values = {}  # Para inicializar variable_values

    def enterClassDef(self, ctx):
        print("Hola")
        self.has_class = True
        type_ids = ctx.TYPE_ID() if isinstance(ctx.TYPE_ID(), list) else [ctx.TYPE_ID()]

        if len(type_ids) > 2:
            self.semantic_errors.append(
                f"Error en línea {ctx.start.line}: No se permite la herencia múltiple."
            )
            return

        class_name = type_ids[0].getText()  # Asegúrate de obtener el nombre de la clase correctamente
        self.current_scope = class_name

        parent_class_name = None
        # Verificación de la clase Main
        if class_name == "Main":
            if ctx.INHERITS():  # Verifica si hay una cláusula INHERITS
                parent_class_name = ctx.TYPE_ID(1).getText() if ctx.TYPE_ID(1) else None
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: La clase Main no puede heredar de {parent_class_name}."
                )
                return  # Retorna inmediatamente después de agregar el error semántico
            self.main_found = True

        # Creación del símbolo para la clase actual
        symbol = Symbol(
            name=class_name,
            type="ClassType",
            scope=self.current_scope,
            lexeme=class_name,
            token="ClassType",
            memory_pos=self.current_memory_position,
            line_num=ctx.start.line,
            line_pos=ctx.start.column,
            semantic_type="ClassType",
            num_params=0,
            param_types=[],
            pass_method="byValue",
            byte_size=0,
            parent_class=parent_class_name,
            symbol_type=SymbolType.CLASS,
        )
        self.symbol_table.add_symbol(symbol)
        self.current_memory_position += 1
        self.table.append(list(symbol.__dict__.values()))

        parent_class_name = None
        visited_classes = set()

        # Si la clase tiene una clase padre (por la presencia de INHERITS
        if ctx.INHERITS():
            original_parent_class_name = (
                ctx.TYPE_ID(1).getText() if ctx.TYPE_ID(1) else None
            )
            parent_class_name = original_parent_class_name
            visited_classes.add(class_name)  # Añade el nombre de la clase actual

            while parent_class_name:
                if parent_class_name in visited_classes:
                    self.semantic_errors.append(
                        f"Error en línea {ctx.start.line}: No se permite la herencia recursiva."
                    )
                    return
                visited_classes.add(parent_class_name)
                parent_symbol = self.symbol_table.get_symbol(
                    parent_class_name, "ClassType"
                )
                parent_class_name = (
                    parent_symbol.parent_class_name if parent_symbol else None
                )

            # Añadir la relación de herencia
            self.symbol_table.add_inheritance(class_name, original_parent_class_name)

            # Añade el tamaño total de la clase padre al tamaño de la clase derivada
            class_symbol = self.symbol_table.get_symbol(class_name, class_name)
            if class_symbol:
                class_symbol.byte_size = self.symbol_table.get_total_class_size(
                    original_parent_class_name
                )

            # Se añade al atributo parent class el nombre de la clase padre
            # Buscar el símbolo de la clase hija en la tabla de símbolos
            derived_symbol = self.symbol_table.get_symbol(class_name, class_name)
            if derived_symbol:
                derived_symbol.parent_class = original_parent_class_name

    def exitClassDef(self, ctx):
        self.current_scope = "global"

    def enterFeature(self, ctx):
        # print(f"Entrando a enterFeature en línea {ctx.start.line}: {ctx.getText()[:100]}...")


           

        self.has_attribute = True

        # Obteniendo los object_ids y type_ids
        object_ids = (
            ctx.OBJECT_ID() if isinstance(ctx.OBJECT_ID(), list) else [ctx.OBJECT_ID()]
        )
        type_ids = ctx.TYPE_ID() if isinstance(ctx.TYPE_ID(), list) else [ctx.TYPE_ID()]

        method_name = object_ids[0].getText() if object_ids else None
        class_name = self.current_scope

        # Verificación para la clase Main y método main
        if class_name == "Main" and method_name == "main":
            self.main_method_in_main_found = True
            formals = ctx.formalList()

            if formals:
                self.semantic_errors.append(
                    "Error: el método main en la clase Main no debe tener parámetros."
                )
                return

        for object_id, type_id in zip(object_ids, type_ids):
            object_id = object_id.getText()
            type_id = type_id.getText()

            if type_id not in self.basic_types and type_id != "IO":
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: Tipo '{type_id}' no reconocido."
                )
                continue

            if ctx.LPAREN():  # Si hay paréntesis, es un método
                symbol_type = SymbolType.FUNCTION
            else:  # De lo contrario, es una variable
                symbol_type = SymbolType.VARIABLE

            # Estableciendo valores default y el tamaño en bytes
            default_value = None
            feature_byte_size = self.type_size_map.get(type_id, 0)

            if type_id == "Int":
                default_value = 0
            elif type_id == "String":
                default_value = ""
            elif type_id == "Bool":
                default_value = False

            # Creación del símbolo de la característica
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
                default_value=default_value,
                byte_size=feature_byte_size,
                symbol_type=symbol_type,
            )

            if self.symbol_table.symbol_exists(
                object_id, self.current_scope
            ) or self.symbol_table.symbol_exists_with_inheritance(
                object_id, self.current_scope
            ):
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: La variable o método {object_id} ya ha sido declarada en este ámbito o una clase base."
                )
                return

            self.symbol_table.add_symbol(symbol)
            self.current_memory_position += 1
            self.table.append(list(symbol.__dict__.values()))

            # Añadir el tamaño de la nueva característica a la clase
            class_symbol = self.symbol_table.get_symbol(
                self.current_scope, self.current_scope
            )
            if class_symbol:
                if class_symbol.byte_size is None:
                    class_symbol.byte_size = 0
                class_symbol.byte_size += feature_byte_size
        self.symbol_table.print_table()

    def enterExpression(self, ctx: YAPLParser.ExpressionContext):
        if ctx.getChildCount() == 2:
            operand = ctx.getChild(1)
            operator = ctx.getChild(0).getText()
            object_id = (
                operand.getText()
                if isinstance(operand, antlr4.tree.TerminalNode)
                else None
            )

            if operator == "~":
                # Código existente para el operador ~
                if object_id:
                    symbol = self.symbol_table.get_symbol(object_id, self.current_scope)
                    if symbol and symbol.semantic_type != "Int":
                        self.semantic_errors.append(
                            f"Error en línea {ctx.start.line}: El operando {object_id} debe ser de tipo Int para la operación unaria ~."
                        )
                        return
                elif operand.INT():
                    return
                else:
                    self.semantic_errors.append(
                        f"Error en línea {ctx.start.line}: Operandos no válidos para la operación unaria ~."
                    )
                    return
            elif operator == "not":
                # Nuevo código para el operador 'not'
                if object_id:
                    # Buscar en las clases base (heredadas)
                    symbol = self.symbol_table.get_symbol_with_inheritance(
                        object_id, self.current_scope
                    )
                    if symbol and symbol.semantic_type != "Bool":
                        self.semantic_errors.append(
                            f"Error en línea {ctx.start.line}: El operando {object_id} debe ser de tipo Bool para la operación 'not'."
                        )
                        return
                elif operand.TRUE() or operand.FALSE():
                    return
                else:
                    self.semantic_errors.append(
                        f"Error en línea {ctx.start.line}: Operandos no válidos para la operación 'not'."
                    )
                    return

        # Comprueba operaciones binarias, que tendrían tres hijos (e.g., expression '+' expression)
        if ctx.getChildCount() == 3:
            left_operand = ctx.getChild(0)
            operator = ctx.getChild(1).getText()
            right_operand = ctx.getChild(2)

            # Manejar la recursión para expresiones con múltiples operadores
            left_type = self.get_expression_type(left_operand)
            right_type = self.get_expression_type(right_operand)

            # Verificar la compatibilidad de tipos
            if left_type != "Int" or right_type != "Int":
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: Los operandos para el operador {operator} deben ser de tipo Int."
                )
                return

        else:
            # Manejo para otras expresiones (no binarias)
            object_id = ctx.OBJECT_ID().getText() if ctx.OBJECT_ID() else None
            # print(f"Verificando {object_id} en el ámbito {self.current_scope}")  # Debugging line
            if object_id and not self.symbol_table.symbol_exists_with_inheritance(
                object_id, self.current_scope
            ):
                # Debugging line: Explicar exactamente qué y cómo se está buscando
                # print(
                #     f"Error Trigger: Se buscó {object_id} en el ámbito {self.current_scope} y no se encontró."
                # )
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: Uso del atributo {object_id} antes de su declaración."
                )
                return

    def enterExpressionStatement(self, ctx):
        object_id = (
            ctx.OBJECT_ID().getText()
        )  # Obtén el identificador a la izquierda del operador de asignación
        expression = (
            ctx.expression()
        )  # Suponiendo que `expression` es cómo obtienes la expresión a la derecha del operador de asignación

        # Verifica si el identificador ha sido declarado
        if not self.symbol_table.symbol_exists(object_id, self.current_scope):
            self.semantic_errors.append(
                f"Error en línea {ctx.start.line}: Uso de la variable {object_id} antes de su declaración."
            )
            return

        symbol = self.symbol_table.get_symbol(object_id, self.current_scope)
        id_semantic_type = symbol.semantic_type

        expr_semantic_type = self.get_expression_type(expression)
        # print(f"Expresión: {expression.getText()}, Tipo Detectado: {expr_semantic_type}")

        # Si la expresión es una simple asignación (ejemplo: var4 = 1)
        if expression.getChildCount() == 1:
            single_operand = expression.getChild(0).getText()

            # Si el operando es un número
            if single_operand.isdigit():
                # symbol.value = int(single_operand)
                symbol.value = int(single_operand)
                # print(f"Valor de {object_id}: {symbol.value}")
            # Aquí también puedes agregar lógica para otros tipos de operandos si es necesario.

        # Evaluamos y almacenamos el valor si es una operación aritmética simple.

        # Evaluamos y almacenamos el valor si es una operación aritmética simple.
        elif expression.getChildCount() >= 3 and (expression.getChildCount() % 2 == 1):
            # Obtener e inicializar variables para realizar operaciones
            result = 0
            operator = None

            # Iterar sobre cada nodo hijo en la expresión
            for i in range(expression.getChildCount()):
                child = expression.getChild(i)
                child_text = child.getText()

                # Si el nodo hijo es un operador
                if child_text in ["+", "-", "*", "/"]:
                    operator = child_text

                # Si el nodo hijo es un operando
                else:
                    operand = int(child_text) if child_text.isdigit() else None

                    # Si operand no es None y es la primera operación, asignar resultado a operand
                    if operand is not None and result == 0 and operator is None:
                        result = operand
                    # Si operand y operator no son None, realizar la operación
                    elif operand is not None and operator is not None:
                        if operator == "+":
                            result += operand
                        elif operator == "-":
                            result -= operand
                        elif operator == "*":
                            result *= operand
                        elif operator == "/":
                            result /= operand
                        # Resetear el operador
                        operator = None

            # Almacenar el valor resultante para la variable.
            symbol.value = result

        # Verificar la compatibilidad de tipos
        if id_semantic_type != expr_semantic_type:
            # Caso especial para permitir el casteo implícito de Bool a Int
            if id_semantic_type == "Int" and expr_semantic_type == "Bool":
                pass
            # Caso especial para permitir el casteo implícito de Int a Bool
            elif id_semantic_type == "Bool" and expr_semantic_type == "Int":
                pass
            elif not self.symbol_table.is_subtype(expr_semantic_type, id_semantic_type):
                # Agrega este mensaje de depuración
                print(
                    f"[DEBUG] En la línea {ctx.start.line}: Tipo de {object_id} (id_semantic_type): {id_semantic_type}, Tipo de la expresión (expr_semantic_type): {expr_semantic_type}"
                )
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: El tipo de la expresión no coincide con el tipo declarado para {object_id}."
                )

    # Método auxiliar para obtener el tipo semántico de una expresión (esto es solo un ejemplo simplificado)
    def get_expression_type(self, expr_ctx):
        if expr_ctx is None:
            return None

        # Si es un literal
        if expr_ctx.INT():
            return "Int"
        elif expr_ctx.STRING_LITERAL():
            return "String"
        elif expr_ctx.TRUE() or expr_ctx.FALSE():
            return "Bool"

        # Si es un identificador, puede ser una variable o una función sin argumentos
        if expr_ctx.OBJECT_ID():
            object_id = expr_ctx.OBJECT_ID().getText()
            symbol = self.symbol_table.get_symbol(object_id, self.current_scope)
            if symbol:
                return symbol.semantic_type

        # Si la expresión es una llamada a función
        if expr_ctx.getChildCount() > 1 and expr_ctx.getChild(1).getText() == "(":
            function_name = expr_ctx.getChild(0).getText()
            symbol = self.symbol_table.get_symbol(function_name, self.current_scope)
            if symbol:
                # Aquí podrías comprobar la coincidencia de los argumentos con los parámetros de la función si es necesario.
                # Debes extraer los argumentos de expr_ctx y compararlos con los parámetros esperados para la función.
                return symbol.semantic_type  # Devuelve el tipo de retorno de la función

        # Para operaciones aritméticas binarias
        elif expr_ctx.getChildCount() == 3:
            left_type = self.get_expression_type(expr_ctx.getChild(0))
            right_type = self.get_expression_type(expr_ctx.getChild(2))
            # Si ambos lados de la operación son del tipo Int, entonces el resultado es Int
            if left_type == "Int" and right_type == "Int":
                return "Int"
            # Aquí puedes añadir más condiciones para otros tipos de operaciones

        # Si ninguna de las condiciones anteriores coincide, devuelve "Unknown"
        return "Unknown"

    def enterStatement(self, ctx):
        # La siguiente condición verifica si la sentencia es un 'if' o un 'while'
        if ctx.getChild(0).getText() in ["if", "while"]:
            # Obtener la expresión
            expr = ctx.expression()

            # Aquí puedes asumir que cada expresión puede tener un OBJECT_ID()
            object_id = expr.OBJECT_ID().getText() if expr.OBJECT_ID() else None

            if object_id:
                # Obtener el símbolo correspondiente al identificador
                symbol = self.symbol_table.get_symbol(object_id, self.current_scope)
                if symbol:
                    # Comprobar si el tipo de la expresión es Bool
                    if symbol.semantic_type != "Bool":
                        self.semantic_errors.append(
                            f"Error en línea {ctx.start.line}: La expresión en la estructura de control debe ser de tipo Bool."
                        )
                        return
            elif expr.TRUE() or expr.FALSE():
                # Si es un valor booleano literal, entonces está bien
                return
            else:
                # Aquí puedes manejar otros tipos de expresiones que podrían no ser válidos para 'if' o 'while'
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: La expresión en la estructura de control debe ser de tipo Bool."
                )
                return

    def enterFormal(self, ctx):
        object_ids = (
            ctx.OBJECT_ID() if isinstance(ctx.OBJECT_ID(), list) else [ctx.OBJECT_ID()]
        )

        
        type_ids = ctx.TYPE_ID() if isinstance(ctx.TYPE_ID(), list) else [ctx.TYPE_ID()]

     
        for object_id, type_id in zip(object_ids, type_ids):
            object_id = object_id.getText()
            type_id = type_id.getText()
            if type_id in self.basic_types:
                pass_method = "byValue"
            else:
                pass_method = "byReference"

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
                pass_method=pass_method,
            )
            self.symbol_table.add_symbol(symbol)
            self.current_memory_position += 1
            self.table.append(list(symbol.__dict__.values()))

    def exitProgram(self, ctx):

        if not self.main_found:
            self.semantic_errors.append("Error: No se ha encontrado la clase Main.")
        elif self.main_found and not self.main_method_in_main_found:
            self.semantic_errors.append(
                "Error: No se ha encontrado el método main en la clase Main."
            )

        if not (self.has_class and self.has_attribute):
            self.semantic_errors.append(
                "Error: Un programa en YAPL debe tener al menos una definición de clase con atributos y métodos."
            )

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
            "Clase del padre",
            "Valor default",
            "Tamaño en bytes"
            "Tipo del simbolo"
        ]

        # --------Imprimir tabla de simbolos--------
        # print(tabulate(self.table, headers=headers, tablefmt="pretty"))


# -------------------------Fin Analisis Semantico---------------------------------------------

# -------------------------Generador codigo intermedio---------------------------------------------
class Cuadruplo:
    def __init__(self, operador, arg1=None, arg2=None, destino=None):
        self.operador = operador
        self.arg1 = arg1
        self.arg2 = arg2
        self.destino = destino

    def __str__(self):
        return f"{self.operador} {self.arg1} {self.arg2} {self.destino}"


MAX_TEMP_REGISTERS = 10  # Asumiendo $t0-$t9

class GeneradorCodigoIntermedio(YAPLListener):
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.cuadruplos = []
        self.current_scope = "global"
        self.scopes = {"global": {}}
        self.in_if_block = False
        self.in_else_block = False
        self.label_stack = []
        self.inside_block = False
        self.jump_stack = []
        self.processed_statements = set()
        self.contained_statements = {}
        self.visited_nodes = set()
        self.available_temporaries = []
        self.processed_temporaries = set()
        self.processed_operations = set()
        self.prompt_counter = 0
        self.prompt_variables = {}
        self.already_read_int = False

    
    # Método para obtener una nueva variable temporal
    def new_temp(self):
        if not self.available_temporaries:
            # Si no hay temporales disponibles, intenta liberar alguno
            for temp in list(self.processed_temporaries):
                self.release_temp(temp)
                if self.available_temporaries:
                    break  # Si se ha liberado un registro, sal del bucle
            
            if not self.available_temporaries:
                if self.temp_counter < MAX_TEMP_REGISTERS - 1:
                    # Si aún es posible, crea un nuevo temporal
                    self.temp_counter += 1
                    temp = f"$t{self.temp_counter}"
                    self.processed_temporaries.add(temp)
                    return temp
                else:
                    # Si has alcanzado el límite máximo de registros, maneja el "spill"
                    raise Exception("No more temporary registers available, implement spilling logic")

        # Si hay registros temporales disponibles, utilízalos
        temp = self.available_temporaries.pop(0)
        self.processed_temporaries.add(temp)
        return temp



    def release_temp(self, temporary):
        if temporary.startswith("$t") and temporary in self.processed_temporaries:
            # Verificamos si la temporal está en uso antes de liberarla
            if not self.is_temporary_in_use(temporary):
                self.processed_temporaries.remove(temporary)
                self.available_temporaries.append(temporary)

    def is_temporary_in_use(self, temp):
        # Verificamos si la temporal se utiliza en cuádruplos pendientes
        for quad in self.cuadruplos:
            if temp == quad.arg1 or temp == quad.arg2:
                return True
        return False

    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def enter_scope(self, scope_name):
        self.current_scope = scope_name
        self.scopes[scope_name] = {}

    def exit_scope(self):
        self.current_scope = "global"

    def enterClassDef(self, ctx: YAPLParser.ClassDefContext):
        class_name = ctx.TYPE_ID()[0].getText()
        self.enter_scope(class_name)
        self.add_cuadruplo(Cuadruplo("begin_class", class_name, "-", "-"))

    def exitClassDef(self, ctx: YAPLParser.ClassDefContext):
        class_name = ctx.TYPE_ID()[0].getText()
        self.add_cuadruplo(Cuadruplo("end_class", class_name, "-", "-"))
        self.exit_scope()

    def enterFeature(self, ctx: YAPLParser.FeatureContext):

        if ctx.OBJECT_ID() and ctx.COLON() and not ctx.LPAREN():
            var_name = ctx.OBJECT_ID().getText()
            print("Variable declaration detected: ", var_name)
            self.scopes[self.current_scope][var_name] = None
            # No generamos cuadruplo de inicialización aquí.

        elif ctx.OBJECT_ID() and ctx.LPAREN() and ctx.RPAREN():
            func_name = ctx.OBJECT_ID().getText()
            print("Function declaration detected: ", func_name)
            self.enter_scope(func_name)
            self.add_cuadruplo(Cuadruplo("begin_method", func_name, "-", "-"))

    def exitFeature(self, ctx: YAPLParser.FeatureContext):
        if ctx.OBJECT_ID() and ctx.LPAREN():
            func_name = ctx.OBJECT_ID().getText()
            self.add_cuadruplo(Cuadruplo("end_method", func_name, "-", "-"))
            self.exit_scope()

    def enterExpressionStatement(self, ctx: YAPLParser.UserMethodCallContext):
        statement_key = (ctx.start.line, ctx.start.column, ctx.getText())

        if statement_key not in self.processed_statements:
            var_name = ctx.OBJECT_ID().getText()
            value = self.process_expression(ctx.expression())
            self.add_cuadruplo(Cuadruplo("=", value, None, var_name))
            self.processed_statements.add(statement_key)
            # Liberar la variable temporal utilizada en esta expresión, si es aplicable.
            self.release_temp(value)

    def enterReturnStatement(self, ctx: YAPLParser.ReturnStatementContext):
        value = self.process_expression(ctx.expression())
        self.add_cuadruplo(Cuadruplo("return", value, None, None))

    def add_cuadruplo(self, cuadruplo: Cuadruplo):
        calling_function_name = inspect.stack()[1].function
        # print(f"In {calling_function_name}: Adding quadruple -> {cuadruplo}")

        if not self.cuadruplos:
            self.cuadruplos.append(cuadruplo)
        elif all(c != cuadruplo for c in self.cuadruplos):
            self.cuadruplos.append(cuadruplo)
        else:
            print(f"Skipping quadruple: {cuadruplo} - already exists.")

    def has_else_block(self, ctx):
        return any(child.getText() == "else" for child in ctx.getChildren())

    def is_else_block(self, ctx):
        parent = ctx.parentCtx
        return (
            parent.getChildCount() > ctx.invokingState + 1
            and parent.getChild(ctx.invokingState + 1).getText() == "else"
        )


    def enterStatement(self, ctx: YAPLParser.StatementContext):
        # Evitar el procesamiento repetido de statements
        if ctx in self.processed_statements:
            return
        self.processed_statements.add(ctx)

        first_child = ctx.getChild(0).getText()

        if first_child == "if":
            # Procesar la condición y generar cuádruplos
            condition = self.process_expression(ctx.expression())
            label_else = self.new_label()
            label_end = self.new_label()

            self.add_cuadruplo(Cuadruplo("if_false", condition, None, label_else))
            
            # Procesar el bloque 'then'
            self.process_statement_block(ctx.block(0),True)

            if self.has_else_block(ctx):
                # Si hay un bloque 'else', saltar al final después del bloque 'then'
                self.add_cuadruplo(Cuadruplo("goto", None, None, label_end))
                # Iniciar el bloque 'else'
                self.add_cuadruplo(Cuadruplo("label", label_else, "-", "-"))
                # Procesar el bloque 'else'
                self.process_statement_block(ctx.block(1),False)
            else:
                # Si no hay bloque 'else', solo agregar la etiqueta de 'else'
                self.add_cuadruplo(Cuadruplo("label", label_else, "-", "-"))
            
            # Etiqueta de fin del if-else
            self.add_cuadruplo(Cuadruplo("label", label_end, "-", "-"))

        elif first_child == "while":
            # Procesar la condición y generar cuádruplos para while
            label_start = self.new_label()
            label_end = self.new_label()

            self.add_cuadruplo(Cuadruplo("label", label_start, "-", "-"))
            condition = self.process_expression(ctx.expression())
            self.add_cuadruplo(Cuadruplo("if_false", condition, None, label_end))

            # Procesar el bloque del bucle while
            #self.process_statement_block(ctx.block(0))
            self.add_cuadruplo(Cuadruplo("goto", label_start, "-", "-"))
            self.add_cuadruplo(Cuadruplo("label", label_end, "-", "-"))

        else:
            # Manejar otros tipos de statements, especialmente asignaciones
            for assignment_context in ctx.getTypedRuleContexts(YAPLParser.AssignmentContext):
                self.enterAssignment(assignment_context)

    
    # Método auxiliar para procesar un bloque de statements, con un flag para saber si es 'then' o 'else'
    def process_statement_block(self, block_ctx, is_then_block):
        for statement in block_ctx.statement():
            if isinstance(statement, YAPLParser.AssignmentContext):
                self.enterAssignment(statement, is_then_block)
            else:
                self.enterStatement(statement)


    def enterIoClassDef(self, ctx: YAPLParser.IoClassDefContext):
        class_name = "IO"
        self.enter_scope(class_name)
        # Añadir cuádruplos específicos para iniciar la clase IO, si es necesario
        # Por ejemplo, si hay alguna inicialización específica para la clase IO
        self.add_cuadruplo(Cuadruplo("init_io_class", class_name, None, None))


    def exitIoClassDef(self, ctx: YAPLParser.IoClassDefContext):
        class_name = ctx.IO().getText()
        self.exit_scope()
        # Aquí, puedes manejar el fin de la definición de la clase IO

    def enterIoFeature(self, ctx: YAPLParser.IoFeatureContext):
        method_name = ctx.getChild(0).getText()  # Obtiene el nombre del método IO
        # Aquí, podrías generar cuádruplos específicos para cada método IO
        # Por ejemplo:
        if method_name == "PROMPT_BOOL":
            # Generar cuádruplos para leer un valor booleano del usuario
            self.add_cuadruplo(Cuadruplo("input_bool", None, None, None))
        elif method_name == "PROMPT_STRING":
            # Análogamente para un string
            self.add_cuadruplo(Cuadruplo("input_string", None, None, None))
        # Continuar para otros métodos IO


    def enterIoMethodCall(self, ctx: YAPLParser.IoMethodCallContext, var_name=None):
        method_name = ctx.getChild(0).getText()
        argument = self.process_expression(ctx.expression())
        #print('method_name ',method_name)
        #print('argument ',argument)
        print(f"Procesando llamada IO: {method_name}, Argumento: {argument}, Variable de destino: {var_name}")

        if method_name in ["promptBool", "promptString", "promptInt"]:
            temp_reg = self.new_temp()

            # Revisar si el argumento es una cadena literal
            prompt_var = None
            if argument.startswith('"') and argument.endswith('"'):
                if argument not in self.prompt_variables:
                    # Crear una nueva variable 'prompt'
                    prompt_var = f"prompt{self.prompt_counter}"
                    self.prompt_counter += 1
                    self.prompt_variables[argument] = prompt_var
                    # Asignar la cadena a la nueva variable 'prompt'
                    self.add_cuadruplo(Cuadruplo("assign", argument, None, prompt_var))
                    # Imprimir la cadena solo si se crea una nueva variable 'prompt'
                    self.add_cuadruplo(Cuadruplo("load_string", prompt_var, "$a0", None))
                    self.add_cuadruplo(Cuadruplo("syscall_print_string", None, None, None))
                else:
                    # Reutilizar la variable 'prompt' existente
                    prompt_var = self.prompt_variables[argument]

            # Ahora, argument es la variable 'prompt', no la cadena literal
            argument = prompt_var if prompt_var else argument

            if method_name in ["promptInt", "promptBool"]:
                if var_name is not None:  # Solo añadir syscall_read_int si var_name no es None
                    self.add_cuadruplo(Cuadruplo("syscall_read_int", None, None, None))
                    self.add_cuadruplo(Cuadruplo("input", "$v0", var_name, None))
            elif method_name == "promptString":
                # Aquí se manejaría la lectura de una cadena para promptString
                pass
                
            # Mover el valor leído solo si hay una variable de destino
            # if var_name is not None:
                # self.add_cuadruplo(Cuadruplo("move", "$v0", var_name, None))
                    

        elif method_name == "printString":
            # Cambio de 'print_string' a 'load_string' y agregado de 'syscall_print_string'.
            self.add_cuadruplo(Cuadruplo("load_string", argument, "$a0", None))
            self.add_cuadruplo(Cuadruplo("syscall_print_string", None, None, None))
        elif method_name == "printInt":
            # Cambio de 'print_int' a 'load_int' y agregado de 'syscall_print_int'.
            self.add_cuadruplo(Cuadruplo("load_int", argument, "$a0", None))
            self.add_cuadruplo(Cuadruplo("syscall_print_int", None, None, None))
        else:
            # Manejar otros posibles métodos IO si existen.
            pass
        




    def enterUserMethodCall(self, ctx: YAPLParser.UserMethodCallContext, temp_var=None):
        method_name = ctx.OBJECT_ID().getText()
        arguments = [self.process_expression(expr) for expr in ctx.expressionList().expression()]
        
        # Primero generar los cuádruplos para los parámetros
        for arg in arguments:
            self.add_cuadruplo(Cuadruplo("param", arg, None, None))
        
        # Luego generar el cuádruplo para invocar la función
        self.add_cuadruplo(Cuadruplo("invoke_function", method_name, len(arguments), temp_var))


            


    def enterAssignment(self, ctx: YAPLParser.AssignmentContext, is_then_block=None):
        statement_key = (ctx.start.line, ctx.start.column, ctx.getText())
        if statement_key in self.processed_statements:
            return
        self.processed_statements.add(statement_key)

        var_name = ctx.OBJECT_ID().getText()
        expr_ctx = ctx.expression()

        # Verifica si la expresión es una llamada a método de usuario para evitar asignación directa.
        if isinstance(expr_ctx, YAPLParser.ExpressionContext) and expr_ctx.methodCall():
            method_call_ctx = expr_ctx.methodCall()
            if method_call_ctx.userMethodCall():
                temp_var = self.new_temp()  # Obtener una nueva variable temporal para el resultado
                self.enterUserMethodCall(method_call_ctx.userMethodCall(), temp_var)  # Procesar la llamada al método
                self.add_cuadruplo(Cuadruplo("assign", temp_var, None, var_name))  # Asignar el resultado a la variable
                if is_then_block:
                    label_end = self.new_label()
                    self.add_cuadruplo(Cuadruplo("goto", None, None, label_end))
                    self.add_cuadruplo(Cuadruplo("label", label_end, "-", "-"))
                return  # Finaliza este método para evitar procesar como asignación normal


        # Verifica si la expresión contiene una llamada a método de IO para asignación.
        if isinstance(expr_ctx, YAPLParser.ExpressionContext) and expr_ctx.methodCall():
            method_call_ctx = expr_ctx.methodCall()
            if method_call_ctx.ioMethodCall():
                io_method_call = method_call_ctx.ioMethodCall()
                self.enterIoMethodCall(io_method_call, var_name)
                return  # Finaliza este método para evitar procesar como asignación normal.

        # Si no es una llamada a IO ni una llamada a método de usuario, procesa como una asignación normal.
        value = self.process_expression(expr_ctx)
        self.add_cuadruplo(Cuadruplo("assign", value, None, var_name))



    
    def process_expression(self, ctx: YAPLParser.ExpressionContext):
        operation = ctx.getText()

        # Si es una expresión simple, simplemente retorna su texto
        if ctx.getChildCount() == 1:
            return ctx.getText()

        # Operación unaria
        elif ctx.getChildCount() == 2:
            operator = ctx.getChild(0).getText()
            operand = self.process_expression(ctx.expression(0))
            temp = self.new_temp()
            if self.is_temporary_in_use(temp):
                self.processed_temporaries.add(temp)
            if operator == "-":
                self.add_cuadruplo(Cuadruplo("menos", operand, None, temp))
            # Liberar la variable temporal utilizada en esta expresión
            self.release_temp(operand)
            return temp

        # Llamada a función
        elif ctx.LPAREN():
            function_name = ctx.OBJECT_ID().getText()
            temp = self.new_temp()
            if self.is_temporary_in_use(temp):
                self.processed_temporaries.add(temp)
            arguments = [self.process_expression(expr) for expr in ctx.expression()]

            # Utilizar instrucciones 'param' para cada argumento
            for arg in arguments:
                self.add_cuadruplo(Cuadruplo("param", arg, None, None))

            # Instrucción 'call' para la llamada a la función
            self.add_cuadruplo(
                Cuadruplo("invoke_function", function_name, len(arguments), temp)
            )

            return temp

        # Operación binaria
        else:
            left_expr = self.process_expression(ctx.expression(0))
            right_expr = self.process_expression(ctx.expression(1))
            operator = ctx.getChild(1).getText()
            temp = self.new_temp()
            if self.is_temporary_in_use(temp):
                self.processed_temporaries.add(temp)
            self.add_cuadruplo(Cuadruplo(operator, left_expr, right_expr, temp))
            # Importante: liberar las temporales después de usarlas
            self.release_temp(left_expr)
            self.release_temp(right_expr)
            return temp

    def get_codigo_intermedio(self):
        return "\n".join(str(cuad) for cuad in self.cuadruplos)

    def imprimir_codigo_intermedio(self):
        print(f"{'':<15}{'Operador':<15}{'Arg 1':<15}{'Arg 2':<15}{'Resultado'}")
        print("-" * 80)
        for i, cuad in enumerate(self.cuadruplos):
            print(
                f"{i:<15}{cuad.operador:<15}{cuad.arg1 if cuad.arg1 is not None else '':<15}"
                f"{cuad.arg2 if cuad.arg2 is not None else '':<15}{cuad.destino if cuad.destino is not None else ''}"
            )




# -------------------------Fin Generador codigo intermedio---------------------------------------------

# -------------------------Traductor a lenguaje ensamblador MIPS---------------------------------------------


class RegisterManager:
    def __init__(self):
        self.registers = ["$t" + str(i) for i in range(10)]
        self.in_use = set()

    def get_register(self):
        for reg in self.registers:
            if reg not in self.in_use:
                self.in_use.add(reg)
                return reg
        raise Exception("All temporary registers in use!")

    def release_register(self, reg):
        if reg in self.in_use:
            self.in_use.remove(reg)


class IntermediateToMIPS():
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.output_code = []
        self.data_section = []
        self.strings_counter = 0
        self.labels = set()
        self.stack_pointer_init_val = (
            10000  # Un valor arbitrario para el inicio de la pila.
        )
        self.strings = {}
        self.register_manager = RegisterManager()
        self.ordered_variables = []  # Lista para mantener las variables en orden
        self.string_variables = []
        self.integer_variables = []

    def add_string_to_data(self, string, label=None):
        # Solo crea una etiqueta y agrega la cadena si se proporciona una etiqueta válida
        if label is not None and self.is_valid_variable_name(label):
            # Agrega la cadena a la sección de datos con la etiqueta
            self.data_section.append(f'{label}: .asciiz "{string}"')
            return label
        
    def find_data_label_for_variable(self, variable_name):
        # Busca en la sección .data la etiqueta correspondiente a la variable
        for data_line in self.data_section:
            if data_line.startswith(variable_name + ":"):
                return variable_name  # Retorna la etiqueta si la encuentra
        return None  # O maneja el caso en que la etiqueta no se encuentre

    def is_valid_variable_name(self, token):
        # Verifica si un token es un nombre de variable válido
        if token.startswith("$") or token.isdigit() or token.startswith('"'):
            return False  # No es una variable si es un registro, número o cadena
        if any(char in token for char in "+-*/:()"):
            return False  # No es una variable si contiene operadores o dos puntos
        if token in ["None", "main", "label", "goto", "if_false", "return", "param", "invoke_function"]:
            return False  # Palabras clave específicas que no son variables
        if token.startswith("L") and token[1:].isdigit():
            return False  # Excluir etiquetas como L1, L2, etc.
        if token.endswith("_class") or token.endswith("_method"):
            return False  # Excluir nombres de clases y métodos
        return True  # Si no se cumple ninguna de las condiciones anteriores, es una variable

    def detect_variables(self, intermediate_code):
        # Esta función detecta las variables y las agrega a la sección .data

        lines = intermediate_code.strip().split("\n")
        declared_variables = set()
        variable_values = {}  # Almacenar valores para las variables

        for line in lines:
            tokens = line.split()

            # Detectar asignaciones en el código intermedio
            if tokens[0] == "assign" and len(tokens) > 3:
                variable_name = tokens[-1]  # Usar el último token como el nombre de la variable
                # Buscar una cadena de texto entre comillas
                match = re.search(r'"([^"]*)"', line)
                if match:
                    string_value = match.group(1)
                    variable_values[variable_name] = string_value.replace('_', ' ') + '\\n'

            for token in tokens:
                # Solo considera tokens que son nombres de variables válidos
                if self.is_valid_variable_name(token) and token not in declared_variables:
                    # Verificar si el token es una variable "prompt"
                    if token.startswith("prompt") and token[len("prompt"):].isdigit():
                        # Si es una variable "prompt", manejar como una nueva variable string
                        self.string_variables.append(token)
                        string_value = variable_values.get(token, "")
                        self.add_string_to_data(string_value, token)
                        declared_variables.add(token)
                    # Buscar el símbolo en la tabla de símbolos para obtener el tipo
                    symbol = next((s for s in self.symbol_table.symbols if s.name == token), None)
                    if symbol:
                        declared_variables.add(token)  # Marcar la variable como declarada
                        self.ordered_variables.append(token)  # Agregar la variable a la lista en orden
                        # Detectado símbolo y su tipo, procede según el tipo semántico
                        if symbol.symbol_type == SymbolType.VARIABLE:
                            if symbol.semantic_type == "Int":
                                self.data_section.append(f"{token}: .word 0")
                                self.integer_variables.append(token)
                            elif symbol.semantic_type == "String":
                                self.string_variables.append(token)  # Agregar la variable a la lista de variables string
                                #print('variables que se van agregando al array:',self.string_variables)
                                string_value = variable_values.get(token, "")
                                #self.data_section.append(f'{token}: .asciiz "{string_value}"')
                                self.add_string_to_data(string_value,token)
                                declared_variables.add(variable_name)
                                #print(variable_name)
                            elif symbol.semantic_type == "Bool":
                                self.data_section.append(f"{token}: .word 1")  # True por defecto
                        # ... otros tipos de símbolos ...
                    else:
                        #print(f"El símbolo no se encontró en la tabla de símbolos: {token}")
                        pass



    def push_to_stack(self, register):
        self.output_code.append(f"    subu $sp, $sp, 4")
        self.output_code.append(f"    sw {register}, 0($sp)")

    def pop_from_stack(self, register):
        self.output_code.append(f"    lw {register}, 0($sp)")
        self.output_code.append(f"    addu $sp, $sp, 4")

    def handle_params(self, param_list):
        # Asumimos que los parámetros se pasan mediante los registros $a0-$a3
        for i, param in enumerate(param_list[:4]):  # Máximo 4 parámetros
            register = f"$a{i}"
            if param.startswith('"'):
                # Manejo de cadenas
                string_label = self.add_string_to_data(param.strip('"'))
                self.output_code.append(f"    la {register}, {string_label}")
            elif param.isdigit():
                # Valores inmediatos
                self.output_code.append(f"    li {register}, {param}")
            else:
                # Carga desde memoria omitida, se asume que el valor ya está en el registro correcto
                pass

    def get_operand_register(self, operand, is_dest=False):
        if operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
            # Es un valor inmediato
            temp_reg = self.register_manager.get_register()
            self.output_code.append(f"    li {temp_reg}, {operand}")
            return temp_reg
        elif operand.startswith("$"):
            # Es un registro
            return operand
        elif is_dest:
            # Es un registro de destino para el resultado
            return self.register_manager.get_register()
        else:
            # Es una variable, cargar desde la memoria
            temp_reg = self.register_manager.get_register()
            self.output_code.append(f"    lw {temp_reg}, {operand}")
            return temp_reg

    def generate_code(self, intermediate_code):
        
        self.detect_variables(intermediate_code)
        lines = intermediate_code.strip().split("\n")
        current_function = None
        param_index = 0  # Inicialización de param_index
        current_string = None  # Variable para almacenar la última cadena cargada
        current_int = None  # Variable para almacenar la última cadena cargada

        for line in lines:
            tokens = line.split()
            if not tokens:
                continue

            cmd = tokens[0]

            if cmd == "begin_method":
                current_function = tokens[1]
                self.output_code.append(f"{current_function}:")
            # elif cmd == "end_method":
            #     self.output_code.append("    jr $ra")
            #     current_function = None
            elif cmd in ["+", "-", "*", "/"]:
                # Determinar los operandos
                reg1 = self.get_operand_register(tokens[1])
                reg2 = self.get_operand_register(tokens[2])
                result_reg = self.register_manager.get_register()  # Obtener un registro para el resultado

                # Generar la operación aritmética
                operation = {"+": "add", "-": "sub", "*": "mul", "/": "div"}[cmd]
                if cmd == "/":
                    self.output_code.append(f"    {operation} {reg1}, {reg2}")
                    self.output_code.append(f"    mflo {result_reg}")
                else:
                    self.output_code.append(f"    {operation} {result_reg}, {reg1}, {reg2}")

                # Almacenar el resultado en el registro indicado
                self.output_code.append(f"    move {tokens[3]}, {result_reg}")

                # Liberar los registros utilizados
                self.register_manager.release_register(result_reg)
                self.register_manager.release_register(reg1)
                self.register_manager.release_register(reg2)

            elif cmd == "assign":
                # Verifica si el lado izquierdo de la asignación es un registro y el derecho una variable
                if tokens[1].startswith("$"):
                    source_reg = tokens[1]
                    target_var = tokens[3]
                    self.output_code.append(f"    sw {source_reg}, {target_var}")

                    # Liberar el registro si es necesario
                    if source_reg.startswith("$t"):
                        self.register_manager.release_register(source_reg)
                # Manejar otras asignaciones (como cadenas) de manera diferente
                elif tokens[1].startswith('"'):
                    # Aquí podrías manejar asignaciones de cadenas, si es necesario
                    pass

            # elif cmd == "assign" and tokens[1].startswith('"'):
            #     # Asignación de una cadena a una variable
            #     string_value = tokens[1].strip('"') + '\\n'  # Elimina las comillas y añade el salto de línea
            #     variable_name = tokens[3]
            #     variable_values[variable_name] = string_value
            #     print('dentro odel assign:',variable_values)

            elif cmd == "=":
                source_reg = (
                    tokens[1]
                    if tokens[1].startswith("$t")
                    else self.register_manager.get_register()
                )

                if not tokens[1].startswith("$t"):
                    if tokens[1].isdigit():
                        self.output_code.append(f"    li {source_reg}, {tokens[1]}")
                    else:
                        self.output_code.append(f"    lw {source_reg}, {tokens[1]}")

                self.output_code.append(f"    sw {source_reg}, {tokens[3]}")

                if not tokens[1].startswith("$t"):
                    self.register_manager.release_register(source_reg)

            elif cmd == "if_false":
                self.output_code.append(f"    lw {tokens[1]}, {tokens[1]}")
                self.output_code.append(f"    beqz {tokens[1]}, {tokens[3]}")

            elif cmd == "goto":
                self.output_code.append(f"    j {tokens[3]}")

            elif cmd == "label":
                self.labels.add(tokens[3])
                self.output_code.append(f"{tokens[3]}:")

            elif cmd == "return":
                if tokens[1].startswith('"'):
                    string_label = self.add_string_to_data(tokens[1].strip('"'))
                    self.output_code.append(f"    la $v0, {string_label}")
                elif tokens[1] != "None":
                    self.output_code.append(f"    lw $v0, {tokens[1]}")  # Load the variable into $v0
                self.output_code.append("    jr $ra")

            elif cmd == "param":
                param = tokens[1]
                register = f"$a{param_index}"
                if param.isdigit() or (param.startswith('-') and param[1:].isdigit()):
                    self.output_code.append(f"    li {register}, {param}")
                elif param.startswith('"'):
                    string_label = self.add_string_to_data(param.strip('"'))
                    self.output_code.append(f"    la {register}, {string_label}")
                param_index += 1  # Incrementa param_index para el próximo parámetro

            elif cmd == "invoke_function":
                function_name = tokens[1]
                self.output_code.append(f"    jal {function_name}")
                result_reg = tokens[3]
                if result_reg != "None":
                    self.output_code.append(f"    sw $v0, {result_reg}")

            elif cmd == "load_string":
                current_string = tokens[1]  # Almacena la variable actual que contiene la cadena
                #print('current_string_load', current_string)

            elif cmd == "load_int":
                current_int = tokens[1]  # Almacena la variable actual que contiene el int a imprimir

            elif cmd == "syscall_print_string":
                #print('variables dentro de syscall',self.ordered_variables)
                # En lugar de buscar el nombre de la variable, usa la lista en orden
                #print('data section', self.data_section)
                #print('string_variables',self.string_variables)
                current_string_stripped = current_string.strip()
                #print('current_string_stripped', current_string_stripped)
                if current_string_stripped in self.string_variables:
                    # Sacamos la primera variable en la lista
                    #next_variable = self.string_variables.pop(0)
                    #print('current_string:',current_string)
                    data_label = self.find_data_label_for_variable(current_string)
                    #print('data label:', data_label)
                    # Load syscall number for print_str into $v0
                    self.output_code.append("    li $v0, 4")
                    # Load address of the string into $a0
                    self.output_code.append(f"    la $a0, {data_label}")
                     # Make syscall to print the string
                    self.output_code.append("    syscall\n")
                    # Reinicia current_string para evitar impresiones duplicadas
                    current_string = None

            elif cmd == "syscall_print_int":
                #print('integer_variables',self.integer_variables)
                if current_int in self.integer_variables:
                    data_label = self.find_data_label_for_variable(current_int)
                    # Load syscall number for print_int into $v0
                    self.output_code.append("    li $v0, 1")
                    # Load the integer value into $a0
                    self.output_code.append(f"    lw $a0, {data_label}")
                    # Make syscall to print the integer
                    self.output_code.append("    syscall\n")
                    # Agrega un salto de línea después de imprimir el entero
                    self.output_code.append("    li $v0, 11")  # Syscall para imprimir carácter
                    self.output_code.append("    li $a0, 10")  # Código ASCII para salto de línea
                    self.output_code.append("    syscall\n")
                    # Reinicia current_int para evitar impresiones duplicadas
                    current_int = None

            elif cmd == "syscall_read_string":
                self.output_code.append("    li $v0, 8")  # Código syscall para leer cadena
                self.output_code.append("    la $a0, buffer")  # Suponiendo que 'buffer' es un espacio en memoria para la entrada
                self.output_code.append("    li $a1, 100")  # Tamaño del buffer
                self.output_code.append("    syscall\n")  # Realizar syscall


            elif cmd == "syscall_read_int":
                #se cambia el $v0 a 5 porque esta esperando un input Int
                self.output_code.append("    li $v0, 5")
                self.output_code.append("    syscall")

            
            elif cmd == "input":
                # Obtiene el nombre de la variable donde se debe almacenar el valor
                variable_name = tokens[2]
                # Genera el código para almacenar el valor de $v0 en la variable
                self.output_code.append(f"    sw $v0, {variable_name}")


        final_code = (
            ".data\n"
            + "\n".join(self.data_section)
            + "\n.text\n"
            + ".globl main\n"
            + "\n".join(self.output_code)
            #ultimas dos lineas son para indicar el "exit" del programa
            # Load syscall number for exit into $v0
            + "\n    li $v0, 10\n"
            # Make syscall to exit the program
            + "    syscall"
        )
        return final_code

    def save_mips_to_file(self, mips_code, filename="output_mips.txt"):
        with open(filename, "w") as file:
            file.write(mips_code)


def main():
    global text_editor

    # Inicializar la ventana principal
    root = tk.Tk()
    root.title("YAPL Validator GUI")
    root.geometry("600x800")

    # Agregar consola interna
    initialize_console(root)
    sys.stdout = IOWrapper(console)
    sys.stderr = IOWrapper(console)

    menu = tk.Menu(root)
    root.config(menu=menu)

    # Creando menu de acciones
    file_menu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)

    # Agregar acciones al menú File
    # Seleccionar un archivo
    file_menu.add_command(label="Open...", command=lambda: select_file(root))
    # Guardar el archivo
    file_menu.add_command(label="Guardar", command=save_file)
    # file_menu.add_command(label="Guardar como...", command=save_as)

    # Si hay cambios guardar al cerrar pestaña
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    # Se mantendra corriendo hasta que se cierre la ventana
    root.mainloop()


if __name__ == "__main__":
    main()

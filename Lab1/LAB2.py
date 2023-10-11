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
    input_stream = FileStream(file_path)

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

    try:
        tree = (
            parser.program()
        )  # Esto creará un árbol incluso si hay errores sintácticos.

        # print(Trees.toStringTree(tree, None, parser))

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

        # Guarda el código intermedio en un archivo
        save_to_file(codigo_intermedio)

    except Exception as e:  # Captura otras excepciones para asegurar una salida limpia

        # print(traceback.format_exc())
        print(f"Error: {e}")
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

    # ---------Imprimir Arbol de analisis sintactico-------
    # for pre, fill, node in RenderTree(root):
    #     print("%s%s" % (pre, node.displayed_label))

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


class SymbolTable:
    def __init__(self):
        self.symbols = []
        self.class_inheritance = (
            {}
        )  # Este diccionario mapeará una clase a su clase base, si es que hereda de alguna.

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    import os

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
            "Param Types",
            "Pass Method",
            "Parent Class",
            "Default Value",
            "Byte Size",
            # "Value",
        ]
        table_data = []
        for symbol in self.symbols:
            table_data.append(list(symbol.__dict__.values()))

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
        self.has_class = True
        type_ids = ctx.TYPE_ID() if isinstance(ctx.TYPE_ID(), list) else [ctx.TYPE_ID()]

        if len(type_ids) > 2:
            self.semantic_errors.append(
                f"Error en línea {ctx.start.line}: No se permite la herencia múltiple."
            )
            return

        class_name = ctx.TYPE_ID()[0].getText()
        self.current_scope = class_name  # Establecer current_scope una vez

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
            formals = ctx.formals()

            if formals:
                self.semantic_errors.append(
                    "Error: el método main en la clase Main no debe tener parámetros."
                )
                return

        for object_id, type_id in zip(object_ids, type_ids):
            object_id = object_id.getText()
            type_id = type_id.getText()

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
            line = ctx.start.line
            column = ctx.start.column
            # aqui ayudo a debuguear si estaba tomando bien los valores para hacerle las operaciones aritmeticas
            # print(f"[Línea {line}, Columna {column}] Operación: {ctx.getChild(1).getText()}, Izquierdo: {ctx.getChild(0).getText()}, Derecho: {ctx.getChild(2).getText()}")
            left_operand = ctx.getChild(0)
            operator = ctx.getChild(1).getText()
            right_operand = ctx.getChild(2)
            # Aquí comprobamos si la operación es aritmética
            if operator in ["+", "-", "*", "/"]:
                operands = [left_operand, right_operand]
                for operand in operands:
                    # Aquí asumimos que cada operand es otra ExpressionContext y tiene un método OBJECT_ID()
                    object_id = (
                        operand.OBJECT_ID().getText() if operand.OBJECT_ID() else None
                    )
                    if object_id:
                        # Obtiene el símbolo correspondiente al identificador
                        symbol = self.symbol_table.get_symbol(
                            object_id, self.current_scope
                        )
                        if symbol and symbol.semantic_type != "Int":
                            self.semantic_errors.append(
                                f"Error en línea {ctx.start.line}: El operando {object_id} debe ser de tipo Int para la operación {operator}."
                            )
                            return
                    elif operand.INT():  # Si el operando es un número entero literal
                        continue  # Este es válido, así que sigue adelante
                    else:
                        # Aquí puedes manejar otros tipos de operandos que podrían no ser válidos para operaciones aritméticas
                        self.semantic_errors.append(
                            f"Error en línea {ctx.start.line}: Operandos no válidos para la operación {operator}."
                        )
                        return
            # Comprobando operaciones de comparación
            elif operator in ["<", ">", "<=", ">=", "=", "!="]:
                operands = [left_operand, right_operand]
                types = []
                for operand in operands:
                    object_id = (
                        operand.OBJECT_ID().getText() if operand.OBJECT_ID() else None
                    )
                    if object_id:
                        symbol = self.symbol_table.get_symbol(
                            object_id, self.current_scope
                        )
                        if symbol:
                            types.append(symbol.semantic_type)
                    elif operand.INT():
                        types.append("Int")
                    # Aquí puedes añadir más tipos si lo necesitas
                    else:
                        self.semantic_errors.append(
                            f"Error en línea {ctx.start.line}: Operandos no válidos para la operación {operator}."
                        )
                        return

                if len(set(types)) > 1:
                    self.semantic_errors.append(
                        f"Error en línea {ctx.start.line}: Los operandos para el operador {operator} deben ser del mismo tipo o de clases heredadas de la misma clase."
                    )
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
        elif expression.getChildCount() == 3:
            left_operand = expression.getChild(0).getText()
            operator = expression.getChild(1).getText()
            right_operand = expression.getChild(2).getText()

            # Si ambos operandos son números, los evaluamos.
            if left_operand.isdigit() and right_operand.isdigit():
                left_value = int(left_operand)
                right_value = int(right_operand)

                if operator == "+":
                    result = left_value + right_value
                elif operator == "-":
                    result = left_value - right_value
                elif operator == "*":
                    result = left_value * right_value
                elif operator == "/":
                    result = left_value / right_value
                # Puedes añadir otros operadores si es necesario

                # Almacenamos el valor resultante para la variable.
                symbol.value = result  # Esta es la línea clave. Estamos asignando el valor calculado al símbolo en la tabla de símbolos.
                # print(f"Valor de {object_id}: {symbol.value}")  # Imprimimos el valor para verificación.
                # print(f"Evaluación: {left_value} {operator} {right_value} = {result}")

        # Verificar la compatibilidad de tipos
        if id_semantic_type != expr_semantic_type:
            # Caso especial para permitir el casteo implícito de Bool a Int
            if id_semantic_type == "Int" and expr_semantic_type == "Bool":
                pass
            # Caso especial para permitir el casteo implícito de Int a Bool
            elif id_semantic_type == "Bool" and expr_semantic_type == "Int":
                pass
            elif not self.symbol_table.is_subtype(expr_semantic_type, id_semantic_type):
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: El tipo de la expresión no coincide con el tipo declarado para {object_id}."
                )

    # Método auxiliar para obtener el tipo semántico de una expresión (esto es solo un ejemplo simplificado)
    def get_expression_type(self, expr_ctx):
        if expr_ctx is None:
            # manejar el caso en que expr_ctx es None
            return None
        if expr_ctx.INT():
            return "Int"
        elif expr_ctx.STRING():
            return "String"
        elif expr_ctx.TRUE() or expr_ctx.FALSE():
            return "Bool"

        # Manejo de operaciones aritméticas binarias
        elif expr_ctx.getChildCount() == 3:
            # Es una operación binaria (podría ser +, -, *, /, etc.)
            left_type = self.get_expression_type(expr_ctx.getChild(0))
            right_type = self.get_expression_type(expr_ctx.getChild(2))

            # Si ambos lados de la operación son del tipo Int, entonces el resultado es Int
            if left_type == "Int" and right_type == "Int":
                return "Int"

        # Añadir lógica para otros tipos de expresiones si es necesario.
        # Por ejemplo, si tienes otros tipos de datos o más operaciones complejas.

        else:
            # ... otros casos
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
        ]

        # --------Imprimir tabla de simbolos--------
        # print(tabulate(self.table, headers=headers, tablefmt="pretty"))


class Cuadruplo:
    def __init__(self, operador, arg1=None, arg2=None, destino=None):
        self.operador = operador
        self.arg1 = arg1
        self.arg2 = arg2
        self.destino = destino

    def __str__(self):
        return f"{self.operador} {self.arg1} {self.arg2} -> {self.destino}"


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

    def new_temp(self):
        if self.available_temporaries:
            return self.available_temporaries.pop()
        else:
            self.temp_counter += 1
            return f"t{self.temp_counter}"

    def release_temp(self, temporary):
        if temporary.startswith("t"):
            self.available_temporaries.append(temporary)

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
        if ctx.OBJECT_ID() and ctx.COLON():
            var_name = ctx.OBJECT_ID().getText()
            self.scopes[self.current_scope][var_name] = None
            # No generamos cuadruplo de inicialización aquí.
        elif ctx.OBJECT_ID() and ctx.LPAREN() and not ctx.RPAREN():
            func_name = ctx.OBJECT_ID().getText()
            self.enter_scope(func_name)
            self.add_cuadruplo(Cuadruplo("begin_method", func_name, "-", "-"))

    def exitFeature(self, ctx: YAPLParser.FeatureContext):
        if ctx.OBJECT_ID() and ctx.LPAREN():
            func_name = ctx.OBJECT_ID().getText()
            self.add_cuadruplo(Cuadruplo("end_method", func_name, "-", "-"))
            self.exit_scope()

    def enterExpressionStatement(self, ctx: YAPLParser.ExpressionStatementContext):
        statement_key = (ctx.start.line, ctx.start.column, ctx.getText())

        if statement_key not in self.processed_statements:
            var_name = ctx.OBJECT_ID().getText()
            value = self.process_expression(ctx.expression())
            self.add_cuadruplo(Cuadruplo("=", value, None, var_name))
            self.processed_statements.add(statement_key)

    def exitExpressionStatement(self, ctx: YAPLParser.ExpressionStatementContext):
        statement_key = (ctx.start.line, ctx.start.column, ctx.getText())

        if statement_key not in self.processed_statements:
            var_name = ctx.OBJECT_ID().getText()
            value = self.process_expression(ctx.expression())
            self.add_cuadruplo(Cuadruplo("=", value, None, var_name))
            self.processed_statements.add(statement_key)
            # Liberar la variable temporal utilizada en esta expresión
            self.release_temp(value)

    def enterReturnStatement(self, ctx: YAPLParser.ReturnStatementContext):
        value = ctx.expression().getText()
        self.add_cuadruplo(Cuadruplo("return", value, None, None))

    def has_else_block(self, ctx):
        return any(child.getText() == "else" for child in ctx.getChildren())

    def is_else_block(self, ctx):
        parent = ctx.parentCtx
        return (
            parent.getChildCount() > ctx.invokingState + 1
            and parent.getChild(ctx.invokingState + 1).getText() == "else"
        )

    def add_cuadruplo(self, cuadruplo: Cuadruplo):
        calling_function_name = inspect.stack()[1].function
        # print(f"In {calling_function_name}: Adding quadruple -> {cuadruplo}")

        # Si los cuádruplos están vacíos, simplemente añade el cuadruplo.
        if not self.cuadruplos:
            self.cuadruplos.append(cuadruplo)
            return

        # Verifica si el cuadruplo actual y el último añadido son asignaciones a la misma variable.
        last_cuadruplo = self.cuadruplos[-1]
        if (
            cuadruplo.operador == "="
            and last_cuadruplo.operador == "="
            and cuadruplo.destino == last_cuadruplo.destino
        ):
            # Si es así, reemplace el último cuadruplo con el nuevo.
            self.cuadruplos[-1] = cuadruplo
            # print(f"Replacing cuadruplo: {last_cuadruplo} -> {cuadruplo}")
        elif all(c != cuadruplo for c in self.cuadruplos):
            # Si el cuadruplo no está en la lista en absoluto, añádelo.
            self.cuadruplos.append(cuadruplo)
        else:
            print(f"Skipping cuadruplo: {cuadruplo} - already exists.")

    def process_statement_block(self, block_statement):
        for expression_statement in block_statement.getTypedRuleContexts(
            YAPLParser.ExpressionStatementContext
        ):
            if expression_statement not in self.processed_statements:
                self.processed_statements.add(expression_statement)
                self.enterExpressionStatement(expression_statement)
            else:
                print(
                    f"Skipping processed block statement: {expression_statement.getText()}"
                )

    def enterStatement(self, ctx: YAPLParser.StatementContext):

        # print(f"Attempting to enter statement: {ctx.getText()}")

        # Si el statement ya fue procesado, lo omitimos
        if ctx in self.processed_statements:
            # print(f"Skipping processed statement: {ctx.getText()}")
            # Marcar el statement como procesado
            self.processed_statements.add(ctx)
            return

        else:
            # Marcar el statement como procesado
            self.processed_statements.add(ctx)

            first_child = ctx.getChild(0).getText()

            if first_child == "if":
                self.inside_block = True
                temp = self.new_temp()
                condition = self.process_expression(ctx.expression())
                self.add_cuadruplo(Cuadruplo("=", condition, None, temp))

                label_else = self.new_label()
                label_end = self.new_label()
                self.add_cuadruplo(Cuadruplo("if_false", temp, None, label_else))

                self.process_statement_block(ctx.statement(0))

                if self.has_else_block(ctx):
                    self.add_cuadruplo(Cuadruplo("goto", None, None, label_end))
                    self.add_cuadruplo(Cuadruplo("label", None, None, label_else))
                    self.process_statement_block(ctx.statement(1))
                    self.add_cuadruplo(Cuadruplo("label", None, None, label_end))

                self.inside_block = False

            elif first_child == "while":
                self.inside_block = True
                label_start = self.new_label()
                self.add_cuadruplo(Cuadruplo("label", None, None, label_start))

                temp = self.new_temp()
                condition = self.process_expression(ctx.expression())
                self.add_cuadruplo(Cuadruplo("=", condition, None, temp))

                label_end = self.new_label()
                self.add_cuadruplo(Cuadruplo("if_false", temp, None, label_end))

                while_statement = ctx.statement(0)
                for expression_statement in while_statement.getTypedRuleContexts(
                    YAPLParser.ExpressionStatementContext
                ):
                    self.processed_statements.add(expression_statement)
                    self.enterExpressionStatement(expression_statement)

                self.add_cuadruplo(Cuadruplo("goto", None, None, label_start))
                self.add_cuadruplo(Cuadruplo("label", None, None, label_end))

                ctx.label_start = label_start
                ctx.label_end = label_end

                self.inside_block = False
            else:
                if not self.inside_block:
                    if ctx in self.processed_statements:
                        return
                    for expression_statement in ctx.getTypedRuleContexts(
                        YAPLParser.ExpressionStatementContext
                    ):
                        self.enterExpressionStatement(expression_statement)

            for statement in ctx.statement():
                self.processed_statements.add(statement)
                for expression_statement in statement.getTypedRuleContexts(
                    YAPLParser.ExpressionStatementContext
                ):
                    self.processed_statements.add(expression_statement)

    def process_expression(self, ctx: YAPLParser.ExpressionContext):
        # Verificar si la operación ya ha sido procesada
        operation = ctx.getText()
        if operation in self.processed_operations:
            return operation

        # Si la operación no se ha procesado aún, continuar con el procesamiento
        if ctx.getChildCount() == 1:
            return ctx.getText()
        elif ctx.getChildCount() == 2:
            operator = ctx.getChild(0).getText()
            operand = self.process_expression(ctx.expression(0))
            temp = self.new_temp()
            if operator == "-":
                self.add_cuadruplo(Cuadruplo("negate", operand, None, temp))
            self.processed_operations.add(
                operation
            )  # Marcar la operación como procesada
            return temp
        else:
            left_expr = self.process_expression(ctx.expression(0))
            right_expr = self.process_expression(ctx.expression(1))
            operator = ctx.getChild(1).getText()
            temp = self.new_temp()
            self.add_cuadruplo(Cuadruplo(operator, left_expr, right_expr, temp))
            self.processed_operations.add(
                operation
            )  # Marcar la operación como procesada
            return temp

    def get_codigo_intermedio(self):
        return "\n".join(str(cuad) for cuad in self.cuadruplos)

    def process_expression(self, ctx: YAPLParser.ExpressionContext):
        if ctx.getChildCount() == 1:
            return (
                ctx.getText()
            )  # Si es una expresión simple, simplemente retorna su texto
        elif ctx.getChildCount() == 2:
            operator = ctx.getChild(0).getText()
            operand = self.process_expression(ctx.expression(0))
            temp = self.new_temp()
            if operator == "-":
                self.add_cuadruplo(Cuadruplo("menos", operand, None, temp))
            # Liberar la variable temporal utilizada en esta expresión
            self.release_temp(operand)
            return temp
        else:
            left_expr = self.process_expression(ctx.expression(0))
            right_expr = self.process_expression(ctx.expression(1))
            operator = ctx.getChild(1).getText()
            temp = self.new_temp()
            self.add_cuadruplo(Cuadruplo(operator, left_expr, right_expr, temp))
            # Liberar las variables temporales utilizadas en esta expresión
            self.release_temp(left_expr)
            self.release_temp(right_expr)
            return temp

    def imprimir_codigo_intermedio(self):
        print(f"{'':<15}{'Operador':<15}{'Arg 1':<15}{'Arg 2':<15}{'Resultado'}")
        print("-" * 80)
        for i, cuad in enumerate(self.cuadruplos):
            print(
                f"{i:<15}{cuad.operador:<15}{cuad.arg1 if cuad.arg1 is not None else '':<15}"
                f"{cuad.arg2 if cuad.arg2 is not None else '':<15}{cuad.destino if cuad.destino is not None else ''}"
            )


# -------------------------Analisis Semantico---------------------------------------------
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

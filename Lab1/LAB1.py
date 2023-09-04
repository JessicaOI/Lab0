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

# ---------------------GUI------------------------------------------------------------
text_editor = None
console = None
# Se crear el el GUI el espacio del editor de texto
def initialize_text_editor(root, content):
    global text_editor

    # Crear el botón y agregarlo a la interfaz
    execute_button = tk.Button(
        root, text="Ejecutar Validaciones", command=execute_functions
    )
    execute_button.pack(pady=10)

    # Crear el editor de texto y llenarlo con el contenido del archivo
    text_editor = Text(root, wrap=tk.WORD)
    text_editor.insert(tk.END, content)
    text_editor.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    # Asegurarse de que el text_editor esté en estado editable
    text_editor.configure(state=tk.NORMAL)


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


# Se crea la consola del GUI
def initialize_console(root):
    global console
    console = tk.Text(root, bg="black", fg="white", wrap=tk.WORD)
    console.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)


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
    lexer = YAPLLexer(input_stream)
    stream = CommonTokenStream(lexer)

    error_listener = CustomErrorListener()

    parser = YAPLParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.program()  # Esto creará un árbol incluso si hay errores sintácticos.

    # print(Trees.toStringTree(tree, None, parser))

    plot_tree(parser, tree)

    # Camina por el árbol incluso si hay errores sintácticos
    listener = MyYAPLListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    # Ahora, al final, verifica e imprime todos los errores detectados
    if (
        parser.getNumberOfSyntaxErrors() > 0 or len(listener.semantic_errors) > 0
    ):  # Asumiendo que `semantic_errors` es una lista en tu listener
        print("Se detectaron los siguientes errores:")

        for error in error_listener.error_messages:
            print("Error Sintáctico: " + error)

        for error in listener.semantic_errors:
            print("Error Semántico: " + error)

        print("Finalizando el programa.")


# -------------------------------------Fin GUI------------------------------------

# ----------------------Analisis sintanctico--------------------------------------
# Mensajes de error personalizados
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
        default_value=None
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
        self.default_value = default_value


class SymbolTable:
    def __init__(self):
        self.symbols = []
        self.class_inheritance = (
            {}
        )  # Este diccionario mapeará una clase a su clase base, si es que hereda de alguna.

    def add_symbol(self, symbol):
        self.symbols.append(symbol)

    def print_table(self):
        headers = ["Name", "Type", "Scope", "Lexeme", "Token", "Memory Pos", "Line Num", "Line Pos", "Semantic Type", "Num Params", "Param Types", "Pass Method", "Default Value"]
        table_data = []

        for symbol in self.symbols:
            table_data.append(list(symbol.__dict__.values()))

        print(tabulate(table_data, headers=headers, tablefmt='pretty'))


    def symbol_exists(self, name, scope):
        return any(
            symbol.name == name and symbol.scope == scope for symbol in self.symbols
        )

    def add_inheritance(self, derived, base):
        self.class_inheritance[derived] = base

    def symbol_exists_with_inheritance(self, name, scope):
        # Verifica primero en el alcance dado
        if any(
            symbol.name == name and symbol.scope == scope for symbol in self.symbols
        ):
            return True

        # Verifica en clases base (si existen)
        while scope in self.class_inheritance:
            scope = self.class_inheritance[scope]
            if any(
                symbol.name == name and symbol.scope == scope for symbol in self.symbols
            ):
                return True

        return False

    def get_symbol(self, name, scope):
        for symbol in self.symbols:
            if symbol.name == name and symbol.scope == scope:
                return symbol
        return None  # Retorna None si no se encuentra el símbolo

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

    def enterClassDef(self, ctx):
        self.has_class = True
        type_ids = ctx.TYPE_ID() if isinstance(ctx.TYPE_ID(), list) else [ctx.TYPE_ID()]
        for type_id in type_ids:
            type_id = type_id.getText()
            class_name = ctx.TYPE_ID()[0].getText()
            self.current_scope = class_name
            if class_name == "Main":
                if ctx.INHERITS():  # Verifica si hay una cláusula INHERITS
                    parent_class_name = ctx.TYPE_ID(
                        1
                    ).getText()  # Nombre de la clase padre
                    self.semantic_errors.append(
                        f"Error en línea {ctx.start.line}: La clase Main no puede heredar de {parent_class_name}."
                    )
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

        class_name2 = ctx.TYPE_ID()[0].getText()
        # Si la clase tiene una clase padre (por la presencia de INHERITS)
        if ctx.INHERITS():
            parent_class_name = ctx.TYPE_ID(1).getText()

            # Añadir las variables y métodos de la clase base al alcance actual
            for symbol in self.symbol_table.symbols:
                if symbol.scope == parent_class_name:
                    inherited_symbol = deepcopy(symbol)
                    inherited_symbol.scope = class_name2
                    self.symbol_table.add_symbol(inherited_symbol)

            # Añadir la relación de herencia
            self.symbol_table.add_inheritance(class_name2, parent_class_name)

    def exitClassDef(self, ctx):
        self.current_scope = "global"

    def enterFeature(self, ctx):
        self.has_attribute = True
        object_ids = (
            ctx.OBJECT_ID() if isinstance(ctx.OBJECT_ID(), list) else [ctx.OBJECT_ID()]
        )

        type_ids = ctx.TYPE_ID() if isinstance(ctx.TYPE_ID(), list) else [ctx.TYPE_ID()]

        # ... (El resto del código original sigue igual)

        for object_id, type_id in zip(object_ids, type_ids):
            object_id = object_id.getText()
            type_id = type_id.getText()

            default_value = None  # Valor predeterminado
            if type_id == "Int":
                default_value = 0
            elif type_id == "String":
                default_value = ""
            elif type_id == "Bool":
                default_value = False

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
                default_value=default_value,  # Añadimos el valor predeterminado aquí
            )
            if self.symbol_table.symbol_exists(object_id, self.current_scope):
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: La variable {object_id} ya ha sido declarada en este ámbito."
                )
                return
            self.symbol_table.add_symbol(symbol)
            self.current_memory_position += 1
            self.table.append(list(symbol.__dict__.values()))
        # Verificación para asegurarse de que cualquier atributo utilizado ha sido declarado
        for object_id in object_ids:
            object_id = object_id.getText()
            if not self.symbol_table.symbol_exists(object_id, self.current_scope):
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: Uso del atributo {object_id} antes de su declaración."
                )
                return
        self.symbol_table.print_table()

    def enterExpression(self, ctx: YAPLParser.ExpressionContext):
        # Comprueba operaciones binarias, que tendrían tres hijos (e.g., expression '+' expression)
        if ctx.getChildCount() == 3:
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
        else:
            # Manejo para otras expresiones (no binarias)
            object_id = ctx.OBJECT_ID().getText() if ctx.OBJECT_ID() else None
            if object_id and not self.symbol_table.symbol_exists(
                object_id, self.current_scope
            ):
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

        # Verificar la compatibilidad de tipos
        if id_semantic_type != expr_semantic_type:
            # Añadir el caso especial para permitir el casteo implícito de Bool a Int
            if id_semantic_type == "Int" and expr_semantic_type == "Bool":
                # Aquí podrías hacer la conversión implícita, si es necesario
                pass
            # Añadir el caso especial para permitir el casteo implícito de Int a Bool
            elif id_semantic_type == "Bool" and expr_semantic_type == "Int":
                # Aquí podrías hacer la conversión implícita, si es necesario
                pass
            else:
                self.semantic_errors.append(
                    f"Error en línea {ctx.start.line}: Incompatibilidad de tipos. No se puede asignar un valor de tipo {expr_semantic_type} a una variable de tipo {id_semantic_type}."
                )

        # Aquí también puedes hacer verificaciones adicionales relacionadas con la compatibilidad de tipos entre el identificador y la expresión.

    # Método auxiliar para obtener el tipo semántico de una expresión (esto es solo un ejemplo simplificado)
    def get_expression_type(self, expr_ctx):
        if expr_ctx.INT():
            return "Int"
        elif expr_ctx.STRING():
            return "String"
        elif expr_ctx.TRUE() or expr_ctx.FALSE():
            return "Bool"
        else:
            # ... otros casos
            return "Unknown"

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
        #print(tabulate(self.table, headers=headers))


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

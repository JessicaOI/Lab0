import sys
from antlr4 import *
from antlr4.tree.Trees import Trees
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from antlr4.error.ErrorListener import ErrorListener
from graphviz import Digraph


class CustomErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Añade tu propia lógica aquí para manejar los errores
        print(f"Línea {line}:{column} {msg}")


def plot_tree(parser, tree):
    dot = Digraph()

    def plot_node(node, parent=None):
        name = f"{node}"
        dot.node(name, label=str(node))
        if parent is not None:
            dot.edge(parent, name)
        children = Trees.getChildren(node)
        print(f"Children of {node}: {children}")  # Imprimir los hijos para depuración
        for child in children:
            plot_node(child, parent=name)

    plot_node(tree)  # Only pass tree, not tree.tree
    dot.render("output.gv", view=True)


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = ExprLexer(input_stream)
    stream = CommonTokenStream(lexer)

    # Añadir el CustomErrorListener al lexer y parser
    lexer.removeErrorListeners()
    lexer.addErrorListener(CustomErrorListener())

    parser = ExprParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(CustomErrorListener())

    tree = parser.prog()

    # Imprimir la representación de texto del árbol
    print(Trees.toStringTree(tree, None, parser))

    # Dibujar el árbol de análisis
    plot_tree(parser, tree)


if __name__ == "__main__":
    main(sys.argv)

import sys
from antlr4 import *
from antlr4.tree.Trees import Trees
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from antlr4.error.ErrorListener import ErrorListener


class CustomErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Añade tu propia lógica aquí para manejar los errores
        print(f"Línea {line}:{column} {msg}")


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

    # Exportar el árbol en formato DOT
    with open("tree.dot", "w") as file:
        file.write(Trees.toStringTree(tree, None, parser))


if __name__ == "__main__":
    main(sys.argv)

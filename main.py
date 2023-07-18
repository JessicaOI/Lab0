import sys
import graphviz
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Trees import Trees


class CustomErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Añade tu propia lógica aquí para manejar los errores
        print(f"Línea {line}:{column} {msg}")


class DotExport(ParseTreeListener):
    def __init__(self):
        self._graph = graphviz.Digraph(format="pdf")
        self._node_id = 0

    def enterEveryRule(self, ctx):
        self._node_id += 1
        node_text = Trees.getNodeText(ctx, ruleNames=ctx.parser.ruleNames)
        self._graph.node(str(self._node_id), label=node_text)
        if ctx.parentCtx is not None:
            parent_id = ctx.parentCtx.invokingState
            self._graph.edge(str(parent_id), str(self._node_id))

    def visitTerminal(self, node):
        self._node_id += 1
        self._graph.node(str(self._node_id), label=node.symbol.text)
        if node.parentCtx is not None:
            parent_id = node.parentCtx.invokingState
            self._graph.edge(str(parent_id), str(self._node_id))

    def export(self, filename):
        self._graph.render(filename)


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
    exporter = DotExport()
    walker = ParseTreeWalker()
    walker.walk(exporter, tree)

    exporter.export("tree")


if __name__ == "__main__":
    main(sys.argv)

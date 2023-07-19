import sys
import os
from antlr4 import *
from antlr4.tree.Trees import Trees
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from antlr4.error.ErrorListener import ErrorListener
from antlr4.RuleContext import RuleContext
from anytree import Node, RenderTree
from anytree.exporter import DotExporter


class CustomErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print(f"Line {line}:{column} {msg}")


def id_generator():
    id = 0
    while True:
        yield id
        id += 1


def plot_tree(parser, tree):
    ids = id_generator()

    def build_node(node, parent=None):
        node_type = type(node).__name__
        if isinstance(node, TerminalNode):
            if node.symbol.type == Token.EOF:
                return None  # Ignore EOF
            if node.symbol.type == ExprParser.NEWLINE:
                return None  # Ignore newlines
            label = str(node)
        elif node_type.endswith("Context"):
            label = node_type.split('Context')[0]
            if label == "Expr":
                label += f" {next(ids)}"
        else:
            label = f"{next(ids)}: {node_type} - {str(node)}"
            
        any_node = Node(label, parent=parent)
        if isinstance(node, RuleContext):
            for i in range(node.getChildCount()):
                child = node.getChild(i)
                build_node(child, any_node)
        return any_node



    root = build_node(tree)
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

    # Export to .dot file
    DotExporter(root).to_dotfile("tree.dot")

    # Render the tree to an image using Graphviz
    os.system('dot -Tpng tree.dot -o tree.png')





def main(argv):
    input_stream = FileStream(argv[1])
    lexer = ExprLexer(input_stream)
    stream = CommonTokenStream(lexer)

    lexer.removeErrorListeners()
    lexer.addErrorListener(CustomErrorListener())

    parser = ExprParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(CustomErrorListener())

    tree = parser.prog()

    print(Trees.toStringTree(tree, None, parser))

    plot_tree(parser, tree)


if __name__ == "__main__":
    main(sys.argv)


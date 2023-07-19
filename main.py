import sys
import os
from antlr4 import *
from antlr4.tree.Trees import Trees
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser
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
                return  # Ignore EOF
            label = str(node)
        elif node_type.endswith("Context"):
            label = node_type.split("Context")[0]
            if label in ["Expr", "Atom", "ID", "STRING"]:
                label += f" {next(ids)}"
        else:
            label = f"{next(ids)}: {node_type} - {str(node)}"

        # For recursive rules, use the existing parent node
        if node_type in ["program", "statement", "condition", "expression"]:
            any_node = parent
        else:
            any_node = Node(label, parent=parent)

        if isinstance(node, RuleContext):
            for i in range(node.getChildCount()):
                child = node.getChild(i)
                child_node = build_node(child, any_node)  # store returned node

                # check if child node is None (for EOF case),
                # if so, continue to the next iteration without adding child
                if child_node is None:
                    continue

        return any_node

    root = build_node(tree)
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

    # Export to .dot file
    DotExporter(root).to_dotfile("tree.dot")

    # Render the tree to an image using Graphviz
    os.system("dot -Tpng tree.dot -o tree.png")


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = YAPLLexer(input_stream)
    stream = CommonTokenStream(lexer)

    lexer.removeErrorListeners()
    lexer.addErrorListener(CustomErrorListener())

    parser = YAPLParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(CustomErrorListener())

    tree = (
        parser.program()
    )  # Reemplazado 'prog()' por 'program()', como definido en la gramática YAPL

    print(Trees.toStringTree(tree, None, parser))

    plot_tree(parser, tree)


if __name__ == "__main__":
    main(sys.argv)

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
    def build_node(node, parent=None):
        node_type = type(node).__name__

        if isinstance(node, TerminalNode):
            if node.symbol.type == Token.EOF:
                return  # Ignore EOF
            label = str(node)
        elif node_type.endswith("Context"):
            # Append last 4 digits of id to make nodes distinguishable
            label = f"{node_type.split('Context')[0]}_{str(id(node))[-4:]}"
        else:
            label = f"{node_type} - {str(node)}"

        if " - []" in label:
            label = label.replace(" - []", "")  # Remove empty tags

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

    # Open the .dot file and add graph attributes for layout
    with open("tree.dot", "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write("digraph tree {\n")
        f.write("rankdir=TB;\n")  # Direction top-to-bottom
        f.write("nodesep=0.6;\n")  # Increase horizontal node separation
        f.write("ranksep=0.8;\n")  # Increase vertical rank separation
        f.write(content)
        f.write("\n}")

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

    tree = parser.program()

    print(Trees.toStringTree(tree, None, parser))

    plot_tree(parser, tree)


if __name__ == "__main__":
    main(sys.argv)

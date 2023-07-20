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

class CustomErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print(f"Line {line}:{column} {msg}")

def plot_tree(parser, tree):
    def build_node(node, parent=None):
        node_type = type(node).__name__

        if isinstance(node, TerminalNode):
            label = Trees.getNodeText(node, parser)
        else:
            label = node_type.split("Context")[0] if node_type.endswith("Context") else node_type

        # Ignore empty nodes
        if label.strip() == "":
            return None

        # Prepare label for Graphviz
        label = label.replace('"', '\\"').replace(' ', '_')

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
        root, nodeattrfunc=lambda node: 'label="%s"' % node.displayed_label.replace(' ', '_')
    ).to_dotfile("tree.dot")

    with open("tree.dot", "r") as f:
        content = f.readlines()

    attributes = ["rankdir=TB;\n", "nodesep=0.6;\n", "ranksep=0.8;\n"]
    content[1:1] = attributes

    with open("tree.dot", "w") as f:
        f.writelines(content)

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

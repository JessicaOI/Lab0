from antlr4.tree.Tree import ParseTreeListener
from graphviz import Digraph


class TreePrinterListener(ParseTreeListener):
    def __init__(self):
        self.dot = Digraph()
        self.node_id = 0

    def enterEveryRule(self, ctx):
        parent_node_id = id(ctx.parentCtx) if ctx.parentCtx else None
        node_id = id(ctx)

        self.dot.node(str(node_id), label=str(ctx.__class__.__name__))

        if parent_node_id:
            self.dot.edge(str(parent_node_id), str(node_id))

    def get_dot(self):
        return self.dot

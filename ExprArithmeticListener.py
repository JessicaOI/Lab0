# Generated from ExprArithmetic.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .ExprArithmeticParser import ExprArithmeticParser
else:
    from ExprArithmeticParser import ExprArithmeticParser

# This class defines a complete listener for a parse tree produced by ExprArithmeticParser.
class ExprArithmeticListener(ParseTreeListener):

    # Enter a parse tree produced by ExprArithmeticParser#prog.
    def enterProg(self, ctx:ExprArithmeticParser.ProgContext):
        pass

    # Exit a parse tree produced by ExprArithmeticParser#prog.
    def exitProg(self, ctx:ExprArithmeticParser.ProgContext):
        pass


    # Enter a parse tree produced by ExprArithmeticParser#exprMultDiv.
    def enterExprMultDiv(self, ctx:ExprArithmeticParser.ExprMultDivContext):
        pass

    # Exit a parse tree produced by ExprArithmeticParser#exprMultDiv.
    def exitExprMultDiv(self, ctx:ExprArithmeticParser.ExprMultDivContext):
        pass


    # Enter a parse tree produced by ExprArithmeticParser#exprParen.
    def enterExprParen(self, ctx:ExprArithmeticParser.ExprParenContext):
        pass

    # Exit a parse tree produced by ExprArithmeticParser#exprParen.
    def exitExprParen(self, ctx:ExprArithmeticParser.ExprParenContext):
        pass


    # Enter a parse tree produced by ExprArithmeticParser#exprAddSub.
    def enterExprAddSub(self, ctx:ExprArithmeticParser.ExprAddSubContext):
        pass

    # Exit a parse tree produced by ExprArithmeticParser#exprAddSub.
    def exitExprAddSub(self, ctx:ExprArithmeticParser.ExprAddSubContext):
        pass


    # Enter a parse tree produced by ExprArithmeticParser#numberExpr.
    def enterNumberExpr(self, ctx:ExprArithmeticParser.NumberExprContext):
        pass

    # Exit a parse tree produced by ExprArithmeticParser#numberExpr.
    def exitNumberExpr(self, ctx:ExprArithmeticParser.NumberExprContext):
        pass


    # Enter a parse tree produced by ExprArithmeticParser#idExpr.
    def enterIdExpr(self, ctx:ExprArithmeticParser.IdExprContext):
        pass

    # Exit a parse tree produced by ExprArithmeticParser#idExpr.
    def exitIdExpr(self, ctx:ExprArithmeticParser.IdExprContext):
        pass



del ExprArithmeticParser
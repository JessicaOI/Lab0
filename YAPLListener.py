# Generated from YAPL.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .YAPLParser import YAPLParser
else:
    from YAPLParser import YAPLParser

# This class defines a complete listener for a parse tree produced by YAPLParser.
class YAPLListener(ParseTreeListener):

    # Enter a parse tree produced by YAPLParser#prog.
    def enterProg(self, ctx:YAPLParser.ProgContext):
        pass

    # Exit a parse tree produced by YAPLParser#prog.
    def exitProg(self, ctx:YAPLParser.ProgContext):
        pass


    # Enter a parse tree produced by YAPLParser#printExpr.
    def enterPrintExpr(self, ctx:YAPLParser.PrintExprContext):
        pass

    # Exit a parse tree produced by YAPLParser#printExpr.
    def exitPrintExpr(self, ctx:YAPLParser.PrintExprContext):
        pass


    # Enter a parse tree produced by YAPLParser#assign.
    def enterAssign(self, ctx:YAPLParser.AssignContext):
        pass

    # Exit a parse tree produced by YAPLParser#assign.
    def exitAssign(self, ctx:YAPLParser.AssignContext):
        pass


    # Enter a parse tree produced by YAPLParser#declare.
    def enterDeclare(self, ctx:YAPLParser.DeclareContext):
        pass

    # Exit a parse tree produced by YAPLParser#declare.
    def exitDeclare(self, ctx:YAPLParser.DeclareContext):
        pass


    # Enter a parse tree produced by YAPLParser#ifStatement.
    def enterIfStatement(self, ctx:YAPLParser.IfStatementContext):
        pass

    # Exit a parse tree produced by YAPLParser#ifStatement.
    def exitIfStatement(self, ctx:YAPLParser.IfStatementContext):
        pass


    # Enter a parse tree produced by YAPLParser#ifStat.
    def enterIfStat(self, ctx:YAPLParser.IfStatContext):
        pass

    # Exit a parse tree produced by YAPLParser#ifStat.
    def exitIfStat(self, ctx:YAPLParser.IfStatContext):
        pass


    # Enter a parse tree produced by YAPLParser#parens.
    def enterParens(self, ctx:YAPLParser.ParensContext):
        pass

    # Exit a parse tree produced by YAPLParser#parens.
    def exitParens(self, ctx:YAPLParser.ParensContext):
        pass


    # Enter a parse tree produced by YAPLParser#addSub.
    def enterAddSub(self, ctx:YAPLParser.AddSubContext):
        pass

    # Exit a parse tree produced by YAPLParser#addSub.
    def exitAddSub(self, ctx:YAPLParser.AddSubContext):
        pass


    # Enter a parse tree produced by YAPLParser#id.
    def enterId(self, ctx:YAPLParser.IdContext):
        pass

    # Exit a parse tree produced by YAPLParser#id.
    def exitId(self, ctx:YAPLParser.IdContext):
        pass


    # Enter a parse tree produced by YAPLParser#int.
    def enterInt(self, ctx:YAPLParser.IntContext):
        pass

    # Exit a parse tree produced by YAPLParser#int.
    def exitInt(self, ctx:YAPLParser.IntContext):
        pass


    # Enter a parse tree produced by YAPLParser#mulDiv.
    def enterMulDiv(self, ctx:YAPLParser.MulDivContext):
        pass

    # Exit a parse tree produced by YAPLParser#mulDiv.
    def exitMulDiv(self, ctx:YAPLParser.MulDivContext):
        pass



del YAPLParser
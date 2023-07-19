# Generated from YAPL.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .YAPLParser import YAPLParser
else:
    from YAPLParser import YAPLParser

# This class defines a complete listener for a parse tree produced by YAPLParser.
class YAPLListener(ParseTreeListener):

    # Enter a parse tree produced by YAPLParser#program.
    def enterProgram(self, ctx:YAPLParser.ProgramContext):
        pass

    # Exit a parse tree produced by YAPLParser#program.
    def exitProgram(self, ctx:YAPLParser.ProgramContext):
        pass


    # Enter a parse tree produced by YAPLParser#statement.
    def enterStatement(self, ctx:YAPLParser.StatementContext):
        pass

    # Exit a parse tree produced by YAPLParser#statement.
    def exitStatement(self, ctx:YAPLParser.StatementContext):
        pass


    # Enter a parse tree produced by YAPLParser#expression.
    def enterExpression(self, ctx:YAPLParser.ExpressionContext):
        pass

    # Exit a parse tree produced by YAPLParser#expression.
    def exitExpression(self, ctx:YAPLParser.ExpressionContext):
        pass


    # Enter a parse tree produced by YAPLParser#condition.
    def enterCondition(self, ctx:YAPLParser.ConditionContext):
        pass

    # Exit a parse tree produced by YAPLParser#condition.
    def exitCondition(self, ctx:YAPLParser.ConditionContext):
        pass



del YAPLParser
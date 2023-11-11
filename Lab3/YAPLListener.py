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


    # Enter a parse tree produced by YAPLParser#classDef.
    def enterClassDef(self, ctx:YAPLParser.ClassDefContext):
        pass

    # Exit a parse tree produced by YAPLParser#classDef.
    def exitClassDef(self, ctx:YAPLParser.ClassDefContext):
        pass


    # Enter a parse tree produced by YAPLParser#ioClassDef.
    def enterIoClassDef(self, ctx:YAPLParser.IoClassDefContext):
        pass

    # Exit a parse tree produced by YAPLParser#ioClassDef.
    def exitIoClassDef(self, ctx:YAPLParser.IoClassDefContext):
        pass


    # Enter a parse tree produced by YAPLParser#ioFeature.
    def enterIoFeature(self, ctx:YAPLParser.IoFeatureContext):
        pass

    # Exit a parse tree produced by YAPLParser#ioFeature.
    def exitIoFeature(self, ctx:YAPLParser.IoFeatureContext):
        pass


    # Enter a parse tree produced by YAPLParser#feature.
    def enterFeature(self, ctx:YAPLParser.FeatureContext):
        pass

    # Exit a parse tree produced by YAPLParser#feature.
    def exitFeature(self, ctx:YAPLParser.FeatureContext):
        pass


    # Enter a parse tree produced by YAPLParser#formalList.
    def enterFormalList(self, ctx:YAPLParser.FormalListContext):
        pass

    # Exit a parse tree produced by YAPLParser#formalList.
    def exitFormalList(self, ctx:YAPLParser.FormalListContext):
        pass


    # Enter a parse tree produced by YAPLParser#formal.
    def enterFormal(self, ctx:YAPLParser.FormalContext):
        pass

    # Exit a parse tree produced by YAPLParser#formal.
    def exitFormal(self, ctx:YAPLParser.FormalContext):
        pass


    # Enter a parse tree produced by YAPLParser#statement.
    def enterStatement(self, ctx:YAPLParser.StatementContext):
        pass

    # Exit a parse tree produced by YAPLParser#statement.
    def exitStatement(self, ctx:YAPLParser.StatementContext):
        pass


    # Enter a parse tree produced by YAPLParser#block.
    def enterBlock(self, ctx:YAPLParser.BlockContext):
        pass

    # Exit a parse tree produced by YAPLParser#block.
    def exitBlock(self, ctx:YAPLParser.BlockContext):
        pass


    # Enter a parse tree produced by YAPLParser#returnStatement.
    def enterReturnStatement(self, ctx:YAPLParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by YAPLParser#returnStatement.
    def exitReturnStatement(self, ctx:YAPLParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by YAPLParser#expressionList.
    def enterExpressionList(self, ctx:YAPLParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by YAPLParser#expressionList.
    def exitExpressionList(self, ctx:YAPLParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by YAPLParser#expression.
    def enterExpression(self, ctx:YAPLParser.ExpressionContext):
        pass

    # Exit a parse tree produced by YAPLParser#expression.
    def exitExpression(self, ctx:YAPLParser.ExpressionContext):
        pass


    # Enter a parse tree produced by YAPLParser#assignment.
    def enterAssignment(self, ctx:YAPLParser.AssignmentContext):
        pass

    # Exit a parse tree produced by YAPLParser#assignment.
    def exitAssignment(self, ctx:YAPLParser.AssignmentContext):
        pass


    # Enter a parse tree produced by YAPLParser#methodCall.
    def enterMethodCall(self, ctx:YAPLParser.MethodCallContext):
        pass

    # Exit a parse tree produced by YAPLParser#methodCall.
    def exitMethodCall(self, ctx:YAPLParser.MethodCallContext):
        pass


    # Enter a parse tree produced by YAPLParser#ioMethodCall.
    def enterIoMethodCall(self, ctx:YAPLParser.IoMethodCallContext):
        pass

    # Exit a parse tree produced by YAPLParser#ioMethodCall.
    def exitIoMethodCall(self, ctx:YAPLParser.IoMethodCallContext):
        pass


    # Enter a parse tree produced by YAPLParser#userMethodCall.
    def enterUserMethodCall(self, ctx:YAPLParser.UserMethodCallContext):
        pass

    # Exit a parse tree produced by YAPLParser#userMethodCall.
    def exitUserMethodCall(self, ctx:YAPLParser.UserMethodCallContext):
        pass



del YAPLParser
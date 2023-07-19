# Generated from YAPL.g4 by ANTLR 4.13.0
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,15,62,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,4,0,10,8,0,11,0,12,
        0,11,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,
        28,8,1,1,1,1,1,3,1,32,8,1,1,2,1,2,1,2,1,2,1,2,1,2,3,2,40,8,2,1,3,
        1,3,1,3,1,3,1,3,1,3,1,3,3,3,49,8,3,1,3,1,3,1,3,1,3,1,3,1,3,5,3,57,
        8,3,10,3,12,3,60,9,3,1,3,0,1,6,4,0,2,4,6,0,2,1,0,3,4,1,0,5,6,67,
        0,9,1,0,0,0,2,31,1,0,0,0,4,33,1,0,0,0,6,48,1,0,0,0,8,10,3,2,1,0,
        9,8,1,0,0,0,10,11,1,0,0,0,11,9,1,0,0,0,11,12,1,0,0,0,12,13,1,0,0,
        0,13,14,5,0,0,1,14,1,1,0,0,0,15,16,3,6,3,0,16,17,5,8,0,0,17,32,1,
        0,0,0,18,19,5,13,0,0,19,20,5,7,0,0,20,21,3,6,3,0,21,22,5,8,0,0,22,
        32,1,0,0,0,23,24,5,12,0,0,24,27,5,13,0,0,25,26,5,7,0,0,26,28,3,6,
        3,0,27,25,1,0,0,0,27,28,1,0,0,0,28,29,1,0,0,0,29,32,5,8,0,0,30,32,
        3,4,2,0,31,15,1,0,0,0,31,18,1,0,0,0,31,23,1,0,0,0,31,30,1,0,0,0,
        32,3,1,0,0,0,33,34,5,9,0,0,34,35,3,6,3,0,35,36,5,10,0,0,36,39,3,
        2,1,0,37,38,5,11,0,0,38,40,3,2,1,0,39,37,1,0,0,0,39,40,1,0,0,0,40,
        5,1,0,0,0,41,42,6,3,-1,0,42,49,5,13,0,0,43,49,5,14,0,0,44,45,5,1,
        0,0,45,46,3,6,3,0,46,47,5,2,0,0,47,49,1,0,0,0,48,41,1,0,0,0,48,43,
        1,0,0,0,48,44,1,0,0,0,49,58,1,0,0,0,50,51,10,5,0,0,51,52,7,0,0,0,
        52,57,3,6,3,6,53,54,10,4,0,0,54,55,7,1,0,0,55,57,3,6,3,5,56,50,1,
        0,0,0,56,53,1,0,0,0,57,60,1,0,0,0,58,56,1,0,0,0,58,59,1,0,0,0,59,
        7,1,0,0,0,60,58,1,0,0,0,7,11,27,31,39,48,56,58
    ]

class YAPLParser ( Parser ):

    grammarFileName = "YAPL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'*'", "'/'", "'+'", "'-'", 
                     "'='", "';'", "'if'", "'then'", "'else'", "'var'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "MUL", "DIV", 
                      "ADD", "SUB", "EQ", "SEMI", "IF", "THEN", "ELSE", 
                      "VAR", "ID", "INT", "WS" ]

    RULE_prog = 0
    RULE_stat = 1
    RULE_ifStat = 2
    RULE_expr = 3

    ruleNames =  [ "prog", "stat", "ifStat", "expr" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    MUL=3
    DIV=4
    ADD=5
    SUB=6
    EQ=7
    SEMI=8
    IF=9
    THEN=10
    ELSE=11
    VAR=12
    ID=13
    INT=14
    WS=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(YAPLParser.EOF, 0)

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(YAPLParser.StatContext)
            else:
                return self.getTypedRuleContext(YAPLParser.StatContext,i)


        def getRuleIndex(self):
            return YAPLParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)




    def prog(self):

        localctx = YAPLParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 9 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 8
                self.stat()
                self.state = 11 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 29186) != 0)):
                    break

            self.state = 13
            self.match(YAPLParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return YAPLParser.RULE_stat

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class DeclareContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a YAPLParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VAR(self):
            return self.getToken(YAPLParser.VAR, 0)
        def ID(self):
            return self.getToken(YAPLParser.ID, 0)
        def SEMI(self):
            return self.getToken(YAPLParser.SEMI, 0)
        def EQ(self):
            return self.getToken(YAPLParser.EQ, 0)
        def expr(self):
            return self.getTypedRuleContext(YAPLParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclare" ):
                listener.enterDeclare(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclare" ):
                listener.exitDeclare(self)


    class IfStatementContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a YAPLParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ifStat(self):
            return self.getTypedRuleContext(YAPLParser.IfStatContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)


    class PrintExprContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a YAPLParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(YAPLParser.ExprContext,0)

        def SEMI(self):
            return self.getToken(YAPLParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrintExpr" ):
                listener.enterPrintExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrintExpr" ):
                listener.exitPrintExpr(self)


    class AssignContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a YAPLParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(YAPLParser.ID, 0)
        def EQ(self):
            return self.getToken(YAPLParser.EQ, 0)
        def expr(self):
            return self.getTypedRuleContext(YAPLParser.ExprContext,0)

        def SEMI(self):
            return self.getToken(YAPLParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssign" ):
                listener.enterAssign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssign" ):
                listener.exitAssign(self)



    def stat(self):

        localctx = YAPLParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stat)
        self._la = 0 # Token type
        try:
            self.state = 31
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = YAPLParser.PrintExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 15
                self.expr(0)
                self.state = 16
                self.match(YAPLParser.SEMI)
                pass

            elif la_ == 2:
                localctx = YAPLParser.AssignContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 18
                self.match(YAPLParser.ID)
                self.state = 19
                self.match(YAPLParser.EQ)
                self.state = 20
                self.expr(0)
                self.state = 21
                self.match(YAPLParser.SEMI)
                pass

            elif la_ == 3:
                localctx = YAPLParser.DeclareContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 23
                self.match(YAPLParser.VAR)
                self.state = 24
                self.match(YAPLParser.ID)
                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 25
                    self.match(YAPLParser.EQ)
                    self.state = 26
                    self.expr(0)


                self.state = 29
                self.match(YAPLParser.SEMI)
                pass

            elif la_ == 4:
                localctx = YAPLParser.IfStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 30
                self.ifStat()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(YAPLParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(YAPLParser.ExprContext,0)


        def THEN(self):
            return self.getToken(YAPLParser.THEN, 0)

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(YAPLParser.StatContext)
            else:
                return self.getTypedRuleContext(YAPLParser.StatContext,i)


        def ELSE(self):
            return self.getToken(YAPLParser.ELSE, 0)

        def getRuleIndex(self):
            return YAPLParser.RULE_ifStat

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStat" ):
                listener.enterIfStat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStat" ):
                listener.exitIfStat(self)




    def ifStat(self):

        localctx = YAPLParser.IfStatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_ifStat)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self.match(YAPLParser.IF)
            self.state = 34
            self.expr(0)
            self.state = 35
            self.match(YAPLParser.THEN)
            self.state = 36
            self.stat()
            self.state = 39
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.state = 37
                self.match(YAPLParser.ELSE)
                self.state = 38
                self.stat()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return YAPLParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ParensContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a YAPLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(YAPLParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParens" ):
                listener.enterParens(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParens" ):
                listener.exitParens(self)


    class AddSubContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a YAPLParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(YAPLParser.ExprContext)
            else:
                return self.getTypedRuleContext(YAPLParser.ExprContext,i)

        def ADD(self):
            return self.getToken(YAPLParser.ADD, 0)
        def SUB(self):
            return self.getToken(YAPLParser.SUB, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddSub" ):
                listener.enterAddSub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddSub" ):
                listener.exitAddSub(self)


    class IdContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a YAPLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(YAPLParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterId" ):
                listener.enterId(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitId" ):
                listener.exitId(self)


    class IntContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a YAPLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(YAPLParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInt" ):
                listener.enterInt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInt" ):
                listener.exitInt(self)


    class MulDivContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a YAPLParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(YAPLParser.ExprContext)
            else:
                return self.getTypedRuleContext(YAPLParser.ExprContext,i)

        def MUL(self):
            return self.getToken(YAPLParser.MUL, 0)
        def DIV(self):
            return self.getToken(YAPLParser.DIV, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMulDiv" ):
                listener.enterMulDiv(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMulDiv" ):
                listener.exitMulDiv(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = YAPLParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [13]:
                localctx = YAPLParser.IdContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 42
                self.match(YAPLParser.ID)
                pass
            elif token in [14]:
                localctx = YAPLParser.IntContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 43
                self.match(YAPLParser.INT)
                pass
            elif token in [1]:
                localctx = YAPLParser.ParensContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 44
                self.match(YAPLParser.T__0)
                self.state = 45
                self.expr(0)
                self.state = 46
                self.match(YAPLParser.T__1)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 58
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 56
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
                    if la_ == 1:
                        localctx = YAPLParser.MulDivContext(self, YAPLParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 50
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 51
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==3 or _la==4):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 52
                        self.expr(6)
                        pass

                    elif la_ == 2:
                        localctx = YAPLParser.AddSubContext(self, YAPLParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 53
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 54
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==5 or _la==6):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 55
                        self.expr(5)
                        pass

             
                self.state = 60
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[3] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 4)
         





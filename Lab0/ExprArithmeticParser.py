# Generated from ExprArithmetic.g4 by ANTLR 4.13.0
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
        4,1,9,27,2,0,7,0,2,1,7,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,
        14,8,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,22,8,1,10,1,12,1,25,9,1,1,1,0,
        1,2,2,0,2,0,2,1,0,5,6,1,0,3,4,28,0,4,1,0,0,0,2,13,1,0,0,0,4,5,3,
        2,1,0,5,1,1,0,0,0,6,7,6,1,-1,0,7,8,5,7,0,0,8,9,3,2,1,0,9,10,5,8,
        0,0,10,14,1,0,0,0,11,14,5,1,0,0,12,14,5,2,0,0,13,6,1,0,0,0,13,11,
        1,0,0,0,13,12,1,0,0,0,14,23,1,0,0,0,15,16,10,5,0,0,16,17,7,0,0,0,
        17,22,3,2,1,6,18,19,10,4,0,0,19,20,7,1,0,0,20,22,3,2,1,5,21,15,1,
        0,0,0,21,18,1,0,0,0,22,25,1,0,0,0,23,21,1,0,0,0,23,24,1,0,0,0,24,
        3,1,0,0,0,25,23,1,0,0,0,3,13,21,23
    ]

class ExprArithmeticParser ( Parser ):

    grammarFileName = "ExprArithmetic.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "'+'", "'-'", 
                     "'*'", "'/'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "ID", "NUMBER", "PLUS", "MINUS", "TIMES", 
                      "DIV", "LPAREN", "RPAREN", "WHITESPACE" ]

    RULE_prog = 0
    RULE_expr = 1

    ruleNames =  [ "prog", "expr" ]

    EOF = Token.EOF
    ID=1
    NUMBER=2
    PLUS=3
    MINUS=4
    TIMES=5
    DIV=6
    LPAREN=7
    RPAREN=8
    WHITESPACE=9

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

        def expr(self):
            return self.getTypedRuleContext(ExprArithmeticParser.ExprContext,0)


        def getRuleIndex(self):
            return ExprArithmeticParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)




    def prog(self):

        localctx = ExprArithmeticParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 4
            self.expr(0)
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
            return ExprArithmeticParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class ExprMultDivContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprArithmeticParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExprArithmeticParser.ExprContext)
            else:
                return self.getTypedRuleContext(ExprArithmeticParser.ExprContext,i)

        def TIMES(self):
            return self.getToken(ExprArithmeticParser.TIMES, 0)
        def DIV(self):
            return self.getToken(ExprArithmeticParser.DIV, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprMultDiv" ):
                listener.enterExprMultDiv(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprMultDiv" ):
                listener.exitExprMultDiv(self)


    class ExprParenContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprArithmeticParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(ExprArithmeticParser.LPAREN, 0)
        def expr(self):
            return self.getTypedRuleContext(ExprArithmeticParser.ExprContext,0)

        def RPAREN(self):
            return self.getToken(ExprArithmeticParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprParen" ):
                listener.enterExprParen(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprParen" ):
                listener.exitExprParen(self)


    class ExprAddSubContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprArithmeticParser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExprArithmeticParser.ExprContext)
            else:
                return self.getTypedRuleContext(ExprArithmeticParser.ExprContext,i)

        def PLUS(self):
            return self.getToken(ExprArithmeticParser.PLUS, 0)
        def MINUS(self):
            return self.getToken(ExprArithmeticParser.MINUS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprAddSub" ):
                listener.enterExprAddSub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprAddSub" ):
                listener.exitExprAddSub(self)


    class NumberExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprArithmeticParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(ExprArithmeticParser.NUMBER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumberExpr" ):
                listener.enterNumberExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumberExpr" ):
                listener.exitNumberExpr(self)


    class IdExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprArithmeticParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(ExprArithmeticParser.ID, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdExpr" ):
                listener.enterIdExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdExpr" ):
                listener.exitIdExpr(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ExprArithmeticParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7]:
                localctx = ExprArithmeticParser.ExprParenContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 7
                self.match(ExprArithmeticParser.LPAREN)
                self.state = 8
                self.expr(0)
                self.state = 9
                self.match(ExprArithmeticParser.RPAREN)
                pass
            elif token in [1]:
                localctx = ExprArithmeticParser.IdExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 11
                self.match(ExprArithmeticParser.ID)
                pass
            elif token in [2]:
                localctx = ExprArithmeticParser.NumberExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 12
                self.match(ExprArithmeticParser.NUMBER)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 23
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 21
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = ExprArithmeticParser.ExprMultDivContext(self, ExprArithmeticParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 15
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 16
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==5 or _la==6):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 17
                        self.expr(6)
                        pass

                    elif la_ == 2:
                        localctx = ExprArithmeticParser.ExprAddSubContext(self, ExprArithmeticParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 18
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 19
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==3 or _la==4):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 20
                        self.expr(5)
                        pass

             
                self.state = 25
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

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
        self._predicates[1] = self.expr_sempred
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
         





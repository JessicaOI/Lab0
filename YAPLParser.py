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
        4,1,20,71,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,4,0,10,8,0,11,0,12,
        0,11,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,25,8,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,4,1,34,8,1,11,1,12,1,35,1,1,1,1,3,1,40,8,
        1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,49,8,2,1,2,1,2,1,2,5,2,54,8,2,
        10,2,12,2,57,9,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,69,
        8,3,1,3,0,1,4,4,0,2,4,6,0,2,1,0,10,11,1,0,14,16,78,0,9,1,0,0,0,2,
        39,1,0,0,0,4,48,1,0,0,0,6,68,1,0,0,0,8,10,3,2,1,0,9,8,1,0,0,0,10,
        11,1,0,0,0,11,9,1,0,0,0,11,12,1,0,0,0,12,1,1,0,0,0,13,14,5,1,0,0,
        14,40,3,4,2,0,15,16,5,18,0,0,16,17,5,2,0,0,17,40,3,4,2,0,18,19,5,
        3,0,0,19,20,3,6,3,0,20,21,5,4,0,0,21,24,3,2,1,0,22,23,5,5,0,0,23,
        25,3,2,1,0,24,22,1,0,0,0,24,25,1,0,0,0,25,40,1,0,0,0,26,27,5,6,0,
        0,27,28,3,6,3,0,28,29,5,7,0,0,29,30,3,2,1,0,30,40,1,0,0,0,31,33,
        5,8,0,0,32,34,3,2,1,0,33,32,1,0,0,0,34,35,1,0,0,0,35,33,1,0,0,0,
        35,36,1,0,0,0,36,37,1,0,0,0,37,38,5,9,0,0,38,40,1,0,0,0,39,13,1,
        0,0,0,39,15,1,0,0,0,39,18,1,0,0,0,39,26,1,0,0,0,39,31,1,0,0,0,40,
        3,1,0,0,0,41,42,6,2,-1,0,42,49,5,19,0,0,43,49,5,18,0,0,44,45,5,12,
        0,0,45,46,3,4,2,0,46,47,5,13,0,0,47,49,1,0,0,0,48,41,1,0,0,0,48,
        43,1,0,0,0,48,44,1,0,0,0,49,55,1,0,0,0,50,51,10,2,0,0,51,52,7,0,
        0,0,52,54,3,4,2,3,53,50,1,0,0,0,54,57,1,0,0,0,55,53,1,0,0,0,55,56,
        1,0,0,0,56,5,1,0,0,0,57,55,1,0,0,0,58,59,3,4,2,0,59,60,7,1,0,0,60,
        61,3,4,2,0,61,69,1,0,0,0,62,63,5,17,0,0,63,69,3,6,3,0,64,65,5,12,
        0,0,65,66,3,6,3,0,66,67,5,13,0,0,67,69,1,0,0,0,68,58,1,0,0,0,68,
        62,1,0,0,0,68,64,1,0,0,0,69,7,1,0,0,0,7,11,24,35,39,48,55,68
    ]

class YAPLParser ( Parser ):

    grammarFileName = "YAPL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'print'", "'='", "'if'", "'then'", "'else'", 
                     "'while'", "'do'", "'{'", "'}'", "'+'", "'-'", "'('", 
                     "')'", "'=='", "'<'", "'>'", "'not'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "ID", "INT", "WS" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_expression = 2
    RULE_condition = 3

    ruleNames =  [ "program", "statement", "expression", "condition" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    ID=18
    INT=19
    WS=20

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(YAPLParser.StatementContext)
            else:
                return self.getTypedRuleContext(YAPLParser.StatementContext,i)


        def getRuleIndex(self):
            return YAPLParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = YAPLParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 9 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 8
                self.statement()
                self.state = 11 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 262474) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(YAPLParser.ExpressionContext,0)


        def ID(self):
            return self.getToken(YAPLParser.ID, 0)

        def condition(self):
            return self.getTypedRuleContext(YAPLParser.ConditionContext,0)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(YAPLParser.StatementContext)
            else:
                return self.getTypedRuleContext(YAPLParser.StatementContext,i)


        def getRuleIndex(self):
            return YAPLParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)




    def statement(self):

        localctx = YAPLParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.state = 39
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 13
                self.match(YAPLParser.T__0)
                self.state = 14
                self.expression(0)
                pass
            elif token in [18]:
                self.enterOuterAlt(localctx, 2)
                self.state = 15
                self.match(YAPLParser.ID)
                self.state = 16
                self.match(YAPLParser.T__1)
                self.state = 17
                self.expression(0)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 3)
                self.state = 18
                self.match(YAPLParser.T__2)
                self.state = 19
                self.condition()
                self.state = 20
                self.match(YAPLParser.T__3)
                self.state = 21
                self.statement()
                self.state = 24
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                if la_ == 1:
                    self.state = 22
                    self.match(YAPLParser.T__4)
                    self.state = 23
                    self.statement()


                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 4)
                self.state = 26
                self.match(YAPLParser.T__5)
                self.state = 27
                self.condition()
                self.state = 28
                self.match(YAPLParser.T__6)
                self.state = 29
                self.statement()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 5)
                self.state = 31
                self.match(YAPLParser.T__7)
                self.state = 33 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 32
                    self.statement()
                    self.state = 35 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 262474) != 0)):
                        break

                self.state = 37
                self.match(YAPLParser.T__8)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(YAPLParser.INT, 0)

        def ID(self):
            return self.getToken(YAPLParser.ID, 0)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(YAPLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(YAPLParser.ExpressionContext,i)


        def getRuleIndex(self):
            return YAPLParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = YAPLParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_expression, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [19]:
                self.state = 42
                self.match(YAPLParser.INT)
                pass
            elif token in [18]:
                self.state = 43
                self.match(YAPLParser.ID)
                pass
            elif token in [12]:
                self.state = 44
                self.match(YAPLParser.T__11)
                self.state = 45
                self.expression(0)
                self.state = 46
                self.match(YAPLParser.T__12)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 55
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = YAPLParser.ExpressionContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                    self.state = 50
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 51
                    _la = self._input.LA(1)
                    if not(_la==10 or _la==11):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 52
                    self.expression(3) 
                self.state = 57
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(YAPLParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(YAPLParser.ExpressionContext,i)


        def condition(self):
            return self.getTypedRuleContext(YAPLParser.ConditionContext,0)


        def getRuleIndex(self):
            return YAPLParser.RULE_condition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondition" ):
                listener.enterCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondition" ):
                listener.exitCondition(self)




    def condition(self):

        localctx = YAPLParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_condition)
        self._la = 0 # Token type
        try:
            self.state = 68
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 58
                self.expression(0)
                self.state = 59
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 114688) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 60
                self.expression(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 62
                self.match(YAPLParser.T__16)
                self.state = 63
                self.condition()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 64
                self.match(YAPLParser.T__11)
                self.state = 65
                self.condition()
                self.state = 66
                self.match(YAPLParser.T__12)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[2] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         





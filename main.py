import sys
from antlr4 import *
from CalculatorLexer import CalculatorLexer
from CalculatorParser import CalculatorParser

def main():
    lexer = CalculatorLexer(InputStream(input('? ')))
    stream = CommonTokenStream(lexer)
    parser = CalculatorParser(stream)
    tree = parser.prog()

if __name__ == '__main__':
    main()

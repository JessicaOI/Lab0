grammar Expr;

@header {
    import sys
    from antlr4 import *
    if sys.version_info[0] >= 3:
        raw_input = input     # Python 3 compatibility
}

prog:   (expr NEWLINE)* ;

expr:   expr ('*'|'/') expr
    |   expr ('+'|'-') expr
    |   INT
    |   '(' expr ')'
    ;

INT :   [0-9]+ ;
NEWLINE:'\r'? '\n' ;
WS  :   [ \t]+ -> skip ;

grammar Expr;

prog:   expr (NEWLINE expr)* NEWLINE? ;


expr:   expr ('*'|'/') expr
    |   expr ('+'|'-') expr
    |   atom
    |   '(' expr ')'
    ;

atom: INT
    | ID
    | STRING
    ;

ID: LETTER (LETTER | [0-9])* ;
STRING: '"' ( ~["\r\n\\] | '\\' . )* '"' ;
INT :   [0-9]+ ;
LETTER: [a-zA-Z] ;
NEWLINE:'\r'? '\n' ;
WS  :   [ \t]+ -> skip ;

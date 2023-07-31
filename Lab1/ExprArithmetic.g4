grammar ExprArithmetic;

// Parser rules
prog: expr ;
expr: expr op=('*' | '/') expr # exprMultDiv
    | expr op=('+' | '-') expr # exprAddSub
    | '(' expr ')'             # exprParen
    | ID                       # idExpr
    | NUMBER                   # numberExpr
    ;

// Lexer rules
ID: LETTER (LETTER | DIGIT)* ;
NUMBER: DIGIT+ ('.' DIGIT+)? ('+' | '-')? DIGIT+ ;
PLUS: '+' ;
MINUS: '-' ;
TIMES: '*' ;
DIV: '/' ;
LPAREN: '(' ;
RPAREN: ')' ;
WHITESPACE: [ \t\r\n]+ -> skip ;  // add this line

// Fragments
fragment LETTER: 'A'..'Z' | 'a'..'z' ;
fragment DIGIT: '0'..'9' ;

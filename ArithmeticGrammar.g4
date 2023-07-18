grammar ArithmeticGrammar;

// Parser Rules

expression:
    expression PLUS term
  | expression MINUS term
  | term
;

term:
    term TIMES factor
  | term DIV factor
  | factor
;

factor:
    LPAREN expression RPAREN
  | ID
  | NUMBER
;

// Lexer Rules

WS : [ \t\r\n]+ -> skip ; // Ignore all whitespaces

ID : [A-Za-z][A-Za-z0-9]* ;

NUMBER : [0-9]+ ('.' [0-9]+)? ('E' [+-]? [0-9]+)? ;

PLUS : '+' ;

MINUS : '-' ;

TIMES : '*' ;

DIV : '/' ;

LPAREN : '(' ;

RPAREN : ')' ;
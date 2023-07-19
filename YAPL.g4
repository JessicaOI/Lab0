grammar YAPL;

// Parser rules
program: statement+;

statement: 
      'print' expression
    | ID '=' expression
    | 'if' condition 'then' statement ('else' statement)?
    | 'while' condition 'do' statement
    | '{' statement+ '}'
    ;

expression: 
      INT
    | ID
    | expression ('+' | '-') expression
    | '(' expression ')'
    ;

condition:
      expression ('==' | '<' | '>') expression
    | 'not' condition
    | '(' condition ')'
    ;

// Lexer rules
ID  : [a-zA-Z_][a-zA-Z_0-9]* ;
INT : [0-9]+ ;
WS  : [ \r\n\t]+ -> skip ;

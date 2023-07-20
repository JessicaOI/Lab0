grammar YAPL;

// Parser rules
program: classDef+;

classDef: CLASS TYPE_ID (INHERITS TYPE_ID)? openBrace feature* closeBrace SEMI;

feature: 
    OBJECT_ID COLON TYPE_ID SEMI
    | OBJECT_ID LPAREN formals? RPAREN COLON TYPE_ID openBrace statement* closeBrace
;

statement: 
    'if' expression 'then' statement 'else' statement 'fi'  
    | 'while' expression 'loop' statement 'pool' 
    | openBrace statement* closeBrace 
    | expressionStatement SEMI
    | returnStatement SEMI
;

expressionStatement:
    | OBJECT_ID '<-' expression 
    | expression 
;

returnStatement: 
    'return' expression
;

formals: formal (',' formal)*;
formal: OBJECT_ID ':' TYPE_ID;

expression
    : INT 
    | OBJECT_ID 
    | STRING
    | TRUE
    | FALSE
    | ISVOID expression
    | OBJECT_ID '(' expression (',' expression)* ')' 
    | expression '@' TYPE_ID '.' OBJECT_ID '(' expression (',' expression)* ')' 
    | expression '.' OBJECT_ID '(' expression (',' expression)* ')'
    | 'new' TYPE_ID
    | expression ('*' | '/') expression
    | expression ('+' | '-') expression
    | expression ('<=' | '<' | '=') expression
    | '(' expression ')'
    | NOT expression
    | TILDE expression
;

openBrace: LCURLY;
closeBrace: RCURLY;

// Lexer rules
CLASS: 'class';
INHERITS: 'inherits';
TRUE: 'true';
FALSE: 'false';
ISVOID: 'isvoid';
NOT: 'not';
OBJECT_ID: [a-z][a-zA-Z0-9_]*;
TYPE_ID: [A-Z][a-zA-Z0-9_]*;
STRING: '"' (~["\r\n\\] | '\\' ["\\/bfnrt])* '"';
INT: [0-9]+;
TILDE: '~';
WS: [ \t\r\n\f]+ -> skip;
LINE_COMMENT: '--' .*? '\n' -> skip;
BLOCK_COMMENT: '(*' .*? '*)' -> skip;
LCURLY: '{';
RCURLY: '}';
SEMI: ';';
LPAREN: '(';
RPAREN: ')';
ASSIGN: '<-';
COLON: ':';

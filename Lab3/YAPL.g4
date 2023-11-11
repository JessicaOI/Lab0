grammar YAPL;

// Parser rules
program: classDef+;

classDef: CLASS TYPE_ID (INHERITS TYPE_ID)? '{' feature* '}' ';' | ioClassDef;

ioClassDef: IO '{' ioFeature* '}' ';';
ioFeature: 
    'promptBool' LPAREN STRING_TYPE RPAREN COLON BOOL '{' '/* implementation */' '}' ';' |
    'promptString' LPAREN STRING_TYPE RPAREN COLON STRING_TYPE '{' '/* implementation */' '}' ';' |
    'promptInt' LPAREN STRING_TYPE RPAREN COLON INT_TYPE '{' '/* implementation */' '}' ';' |
    'printInt' LPAREN INT_TYPE RPAREN COLON 'SELF_TYPE' '{' '/* implementation */' '}' ';' |
    'printString' LPAREN STRING_TYPE RPAREN COLON 'SELF_TYPE' '{' '/* implementation */' '}' ';'
;

feature: 
    OBJECT_ID COLON TYPE_ID ';' |
    OBJECT_ID LPAREN formals? RPAREN COLON TYPE_ID '{' statement* '}' ';'
;

statement: 
    'if' expression 'then' statement 'else' statement |
    'while' expression 'loop' statement 'pool' ';' |
    '{' statement* '}' ';' |
    expressionStatement ';' |
    returnStatement ';'
;

expressionStatement: OBJECT_ID ASSIGN expression;

returnStatement: 'return' expression;

formals: formal (',' formal)*;
formal: OBJECT_ID ':' TYPE_ID;

expression:
    INT |
    OBJECT_ID |
    STRING_LITERAL |
    TRUE |
    FALSE |
    OBJECT_ID '(' expression (',' expression)* ')' |
    expression ('*' | '/' | '+' | '-' | '<=' | '<' | '=') expression |
    '(' expression ')' |
    NOT expression |
    TILDE expression |
    ioExpression |
    assignment
;

assignment: OBJECT_ID ASSIGN expression;

ioExpression:
    OBJECT_ID '.' OBJECT_ID '(' expression? (',' expression)* ')' 
;

// Lexer rules
CLASS: 'class';
INHERITS: 'inherits';
TRUE: 'true';
FALSE: 'false';
ISVOID: 'isvoid';
NOT: 'not';
OBJECT_ID: [a-z][a-zA-Z0-9_]*;
TYPE_ID: [A-Z][a-zA-Z0-9_]*;
STRING_LITERAL: '"' (~["\r\n\\] | '\\' ["\\/bfnrt])* '"';
INT: [0-9]+;
TILDE: '~';
WS: [ \t\r\n\f]+ -> skip;
LINE_COMMENT: '--' .*? '\n' -> skip;
BLOCK_COMMENT: '(*' .*? '*)' -> skip;
LPAREN: '(';
RPAREN: ')';
ASSIGN: '<-';
COLON: ':';
IO: 'IO';
SELF_TYPE: 'SELF_TYPE';
BOOL: 'Bool';
STRING_TYPE: 'String';
INT_TYPE: 'Int';

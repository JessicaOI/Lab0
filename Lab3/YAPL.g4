grammar YAPL;

// Parser rules
program: classDef+;

classDef: CLASS TYPE_ID (INHERITS TYPE_ID)? '{' feature* '}' ';' | ioClassDef;

ioClassDef: IO '{' ioFeature* '}' ';';
ioFeature: 
    PROMPT_BOOL '(' ')' COLON BOOL '{' '/* implementation */' '}' ';' |
    PROMPT_STRING '(' ')' COLON STRING_TYPE '{' '/* implementation */' '}' ';' |
    PROMPT_INT '(' ')' COLON INT_TYPE '{' '/* implementation */' '}' ';' |
    'printInt' '(' INT_TYPE ')' COLON 'SELF_TYPE' '{' '/* implementation */' '}' ';' |
    'printString' '(' STRING_TYPE ')' COLON 'SELF_TYPE' '{' '/* implementation */' '}' ';'
;

feature: 
    OBJECT_ID COLON TYPE_ID ';' |
    OBJECT_ID '(' formalList? ')' COLON TYPE_ID '{' statement* '}' ';'
;

formalList: formal (',' formal)*;
formal: OBJECT_ID ':' TYPE_ID;

statement: 
    'if' expression 'then' block 'else' block |
    'while' expression 'loop' block 'pool' |
    assignment ';' |
    methodCall ';' |
    returnStatement
;

block: '{' statement* '}';

returnStatement: 'return' expression ';';

expressionList: expression (',' expression)*;

expression:
    INT |
    OBJECT_ID |
    STRING_LITERAL |
    TRUE |
    FALSE |
    methodCall |
    expression ('*' | '/') expression |
    expression ('+' | '-') expression |
    expression ('<=' | '<' | '=') expression |
    '(' expression ')' |
    NOT expression |
    TILDE expression |
    assignment
;

assignment: OBJECT_ID ASSIGN expression;

methodCall
    :   OBJECT_ID '.' (ioMethodCall | userMethodCall) // Distinguish IO and user method calls
    ;

ioMethodCall
    :   (PROMPT_BOOL | PROMPT_STRING | PROMPT_INT | 'printInt' | 'printString') '(' expression? ')' 
    ;

userMethodCall
    :   OBJECT_ID '(' expressionList? ')' // User defined method calls
    ;

// Lexer rules
PROMPT_BOOL: 'promptBool';
PROMPT_STRING: 'promptString';
PROMPT_INT: 'promptInt';
CLASS: 'class';
INHERITS: 'inherits';
TRUE: 'true';
FALSE: 'false';
ISVOID: 'isvoid';
NOT: 'not';
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
OBJECT_ID: [a-z][a-zA-Z0-9_]*; // El patrón original para los identificadores

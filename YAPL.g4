grammar YAPL;

prog: stat+ EOF;

stat: expr ';'                 # printExpr
    | ID '=' expr ';'          # assign
    | 'var' ID ('=' expr)? ';' # declare
    | ifStat                   # ifStatement
    ;

ifStat: 'if' expr 'then' stat ('else' stat)?;

expr: expr op=('*'|'/') expr  # mulDiv
    | expr op=('+'|'-') expr  # addSub
    | ID                      # id
    | INT                     # int
    | '(' expr ')'            # parens
    ;

MUL : '*';
DIV : '/';
ADD : '+';
SUB : '-';
EQ  : '=';
SEMI: ';';

IF  : 'if';
THEN: 'then';
ELSE: 'else';
VAR : 'var';

ID  : [a-zA-Z]+ ;
INT : [0-9]+ ;
WS  : [ \t\n\r]+ -> skip ; // ignora espacios en blanco, tabulaciones y saltos de línea

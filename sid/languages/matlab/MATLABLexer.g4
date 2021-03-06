lexer grammar MATLABLexer;

// Keywords
FUNCTION : 'function' ;

CLASSDEF : 'classdef' ;

PROPERTIES : 'properties' ;

METHODS : 'methods' ; 

END : 'end' ;

IF  : 'if' ;

ELSEIF : 'elseif' ;

ELSE : 'else' ;

WHILE : 'while' ;

FOR : 'for' ;

SWITCH : 'switch' ;

CASE : 'case' ; 

OTHERWISE : 'otherwise' ;

BREAK : 'break' ;

CONTINUE : 'continue' ;

RETURN : 'return' ;

CLEAR : 'clear' ;

// Symbols
EQUALS : '=' ;

EQUALTO : '==' ;

NOTEQUALTO : '~=' ;

GT : '>' ;

LT : '<' ;

GE : '>=' ;

LE : '<=' ;

PLUS : '+' ;

MINUS : '-' ;

DOT : '.' ;

VECAND : '&' ;

VECOR : '|' ;

SCALAND : '&&' ;

SCALOR : '||' ;

LPAREN : '(' ;

RPAREN : ')' ;

LBRACE : '{' ;

// RBRACE : '}' ;

LBRACK : '[' ;

// RBRACK : ']' ;

MTIMES : '*' ;

TIMES : '.*' ;

RDIVIDE : '/' ;

LDIVIDE : '\\' ;

MRDIVIDE : './' ;

MLDIVIDE : '.\\' ;

POW : '.^' ;

MPOW : '^' ;

NOT : '~' ;

COLON : ':' ;

TRANS : '.\'' ;

CTRANS : '\'' ;

FUNC_HANDLE : '@' ;

// General rules
NL  : '\r'?'\n' ;

fragment
LINECONTINUE
    : '...' ;

COMMENT
    : ('%' | LINECONTINUE) .*? NL -> skip ;

fragment
LETTER  : [a-zA-Z] ; 
fragment
DIGIT   : [0-9] ; 
fragment
ESC : '\'\'' ;

INT : DIGIT+;

FLOAT : DIGIT+ '.' DIGIT*
      | '.' DIGIT+
      ;

SCI : (INT|FLOAT) 'e' INT ;

ID  : LETTER (LETTER|DIGIT|'_')* ;
STRING : '\'' (ESC|.)*? '\'' ;

RBRACK : ']' ;
RBRACE : '}' ;

// HCAT : (COMMA); // | SPACE ) ;

// VCAT : (SEMI | NL ) ;

// ARRAYELSEP : (HCAT| VCAT ) ; // SPACE+ ;

COMMA : ',' ;

SEMI  : ';' ;

WS  : SPACE+ -> skip ;

fragment
SPACE : [ \t] ;

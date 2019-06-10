parser grammar MATLABParser;

// base from https://github.com/mattmcd/ParseMATLAB
// adapted some rules from https://github.com/antlr/grammars-v4/tree/master/matlab

options { tokenVocab=MATLABLexer;}

fileDecl  
    : (functionDecl | classDecl)? (functionDecl* | partialFunctionDecl*)
    | partialFunctionDecl+
    | statBlock+ // Script
    | EOF
    ;

endStat
    : (NL|COMMA|SEMI) NL*
    ;

endStatNL 
    : NL+
    ;

// Function declaration without the closing end
partialFunctionDecl
    : FUNCTION outArgs? ID inArgs? endStat statBlock* 
    ; 

// Normal function declaration including closing end
functionDecl
    : partialFunctionDecl END endStatNL NL*
    ;

// Functions inside method blocks can be comma or semi separated 
methodDecl
    : partialFunctionDecl END endStat
    ;

classDecl
    : CLASSDEF ID endStat 
      (propBlockDecl|methodBlockDecl)* 
      END (EOF|endStat) NL*
    ;

propBlockDecl
    : PROPERTIES endStat prop* END endStat
    ;

methodBlockDecl
    : METHODS endStat methodDecl* END endStat
    ;

outArgs
    : ID EQUALS
    | LBRACK ID (COMMA ID)* RBRACK EQUALS
    ;

inArgs
    : LPAREN ID (COMMA ID)* RPAREN
    | LPAREN RPAREN
    ;

prop
    : ID (EQUALS expr)? endStat
    ;

dotRef
    : ID (DOT ID)*
    ;

statBlock
    : (stat endStat)
    ;

ifStat
    : IF expr endStat statBlock* 
      (ELSEIF expr endStat statBlock*)* 
      (ELSE endStat? statBlock*)?
      END
    ;

whileStat
    : WHILE expr endStat statBlock* END
    ;

forStat
    : FOR ID EQUALS expr endStat statBlock* END
    | FOR LPAREN ID EQUALS expr RPAREN statBlock* END
    ;

switchStat
    : SWITCH expr endStat 
      caseStat*
      otherwiseStat?
      END
    ;

caseStat
    : CASE expr endStat statBlock*
    ;

otherwiseStat
    : OTHERWISE endStat statBlock*
    ;

jumpStat
   : BREAK endStat
   | CONTINUE endStat
   | RETURN endStat
   ;

stat
    : dotRef EQUALS expr
    | ifStat
    | whileStat
    | forStat
    | switchStat
    | jumpStat
    | expr 
    | NL
    ;

expr
// https://uk.mathworks.com/help/matlab/matlab_prog/operator-precedence.html
    : exprList
    | LPAREN exprList RPAREN
    | expr LPAREN exprList RPAREN
    ;

exprList
    : listExpr (',' listExpr)*
    ;

listExpr
    : arrayExpr
    | cellExpr
    | logicExpr
    ;

arrayExpr
    : LBRACK exprArrayList RBRACK
    | LBRACK RBRACK
    ;

cellExpr
    : LBRACE exprArrayList RBRACE
    | LBRACE RBRACE
    ;

logicExpr
    : compExpr ((VECAND|VECOR|SCALAND|SCALOR) compExpr)*
    ;

compExpr
    : colonExpr ((NOT|EQUALTO|GT|LT|GE|LE) colonExpr)*
    ;

colonExpr
    : additiveExpr (COLON additiveExpr)*
    ;

additiveExpr
    : multiplicativeExpr ((PLUS|MINUS) multiplicativeExpr)*
    ;

multiplicativeExpr
    : signExpr ((MTIMES|TIMES|MLDIVIDE|LDIVIDE|MRDIVIDE|RDIVIDE) signExpr)*
    ;

signExpr
    : (PLUS|MINUS|NOT)? powExpr
    ;

powExpr
    : transposeExpr ((MPOW|POW) transposeExpr)*
    ;

transposeExpr
    : basicExpr (TRANS|CTRANS)?
    ;

basicExpr
    : dotRef
    | INT | FLOAT | SCI
    | STRING
    ;

exprArrayList
    : expr (COMMA? exprArrayList)*    #hcat
    | expr ((SEMI|NL) exprArrayList)* #vcat
    ;

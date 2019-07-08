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
    : FUNC_HANDLE? ID (DOT ID)* (LBRACE expr RBRACE)?
    | LBRACK ID (COMMA ID)* RBRACK
    | END // can be a valid token in some cases
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

clearStat
    : CLEAR ID ID*
    ;

stat
    : dotRef EQUALS expr
    | funcExpr EQUALS expr
    | ifStat
    | whileStat
    | forStat
    | switchStat
    | jumpStat
    | clearStat
    | expr 
    | NL
    ;

expr
// https://uk.mathworks.com/help/matlab/matlab_prog/operator-precedence.html
    : exprList
    ;

funcExpr
    : dotRef exprList
    ;

exprList
    : LPAREN listExpr (COMMA listExpr)* RPAREN
    | LPAREN RPAREN
    | listExpr (COMMA listExpr)*
    ;

listExpr
    : arrayExpr
    | cellExpr
    | logicExpr
    ;

arrayExpr
    : LBRACK exprArrayList? RBRACK
    ;

cellExpr
    : LBRACE exprArrayList? RBRACE
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
    : funcExpr
    | dotRef
    | INT | FLOAT | SCI
    | STRING
    ;

exprArrayList
    : expr (COMMA? exprArrayList)*    #hcat
    | expr ((SEMI|NL) exprArrayList)* #vcat
    ;

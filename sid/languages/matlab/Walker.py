from antlr4 import *

from sid.languages.matlab.MATLABParserListener import MATLABParserListener
from sid.languages.matlab.MATLABParser import MATLABParser
from sid.languages.matlab.Tokens import *
from sid.languages.errors import UnknownSymbolError


class SIDMatlabWalker(MATLABParserListener):
    """Class extends matlabListener (generated by ANTLR) to register parse 
        tokens encountered during processing of source code. This class 
        overrides methods that are expected to emit tokens which correspond to 
        methods defining logic in the source code.
    """
    
    def __init__(self, *args, **kwargs):
        """Method creates a new instance of SIDMatlabWalker, and creates empty 
            lists for the tokens generated.
        """
        super().__init__(*args, **kwargs)

        self.symbols = []
        self.tokens = []


    def add_token(self, symbol, token):
        """Method records a found token that will be essential for 
            distinguishing logic in a program. This method does not return 
            anything, but formats the found token and saves it in the 
            appropriate lists.
        
        :param symbol: The identifier for a found symbol, that represents a 
            program control structure (built-in identifier)
        :type symbol: int
        :param token: ANTLR token that contains information about recorded 
            symbol's location in the original source file
        :type token: antlr4.Token.Token
        """
        self.symbols.append(symbol)
        self.tokens.append({
            'line': token.line,
            'col': token.column
        })

    
    def format(self, symbol):
        """Method maps a single Matlab Language token onto human readable 
            string. Each token is mapped to a string without any spaces to be 
            able to distinguish tokens.
        
        :param symbol: The symbol constant to be analysed
        :type symbol: int
        :raises UnknownSymbolError: If the symbol received is not known in this 
            language, an exception is raised
        :return: Human readable representation of the symbol
        :rtype: str
        """
        mapping = {
            APPLY: "APPLY",
            ARRAY: "ARRAY",
            ASSIGN: "ASSIGN",
            BREAK: "BREAK",
            CASE: "CASE",
            CLASS_BEGIN: "CLASS_BEGIN",
            CLASS_END: "CLASS_END",
            CONTINUE: "CONTINUE",
            FOR_BEGIN: "FOR_BEGIN",
            FOR_END: "FOR_END",
            FUNC_BEGIN: "FUNC_BEGIN",
            FUNC_END: "FUNC_END",
            IF_BEGIN: "IF_BEGIN",
            IF_END: "IF_END",
            RETURN: "RETURN",
            SWITCH_BEGIN: "SWITCH_BEGIN",
            SWITCH_END: "SWITCH_END",
            TRANSPOSE: "TRANSPOSE",
            WHILE_BEGIN: "WHILE_BEGIN",
            WHILE_END: "WHILE_END"
        }

        if symbol not in mapping:
            raise UnknownSymbolError
        
        return mapping[symbol]


    def str_symbols(self):
        """Method computes a string representation of the full parsed text by 
            converting each symbol from integer to char representation in ASCII. 
            This is useful if fingerprinting engine expects text instead of 
            integer list, since the integer list will be converted to string 
            with each character representing one symbol from parsed source code.
        
        :return: Character sequence corresponding to parsed source code
        :rtype: str
        """
        s = ""
        for symbol in self.symbols:
            s += chr(symbol)

        return s


    def __str__(self):
        """Method creates a string representation of SIDMatlabWalker instance 
            by creating a human readable representation of the parsed source 
            code. This representation is abstract and identical to that seen by 
            fingerprinting algorithm (with string constants replaced by single 
            characters when using fingerprinter).
        
        :return: The human readable representation of parsed source code
        :rtype: str
        """
        s = ""
        for symbol in self.symbols:
            if s != "": 
                s += " "
            s += self.format(symbol)
        
        return s


    def visitTerminal(self, node:TerminalNode):
        # TODO: modify comment and source
        """Method implements functionality that will be invoked when visiting 
            terminal nodes of program AST. Currently, only two cases of final 
            nodes are considered (as implemented in JPlag: 
            https://github.com/jplag/jplag/blob/9e6b2ba0c7532a0acaf9f88f4aa8b723d77a19c3/jplag.frontend.python-3/src/main/java/jplag/python3/JPlagPython3Listener.java ).
        
        :param node: The terminal node as parsed by ANTLR
        :type node: antlr4.tree.Tree.TerminalNode
        """
        if node.getText() == "=":
            self.add_token(ASSIGN, node.getSymbol())


    """The following methods override matlabListener methods that are called 
        when entering or exiting program tree nodes.
    """


    # Enter a parse tree produced by MATLABParser#fileDecl.
    def enterFileDecl(self, ctx:MATLABParser.FileDeclContext):
        pass

    # Exit a parse tree produced by MATLABParser#fileDecl.
    def exitFileDecl(self, ctx:MATLABParser.FileDeclContext):
        pass


    # Enter a parse tree produced by MATLABParser#endStat.
    def enterEndStat(self, ctx:MATLABParser.EndStatContext):
        pass

    # Exit a parse tree produced by MATLABParser#endStat.
    def exitEndStat(self, ctx:MATLABParser.EndStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#endStatNL.
    def enterEndStatNL(self, ctx:MATLABParser.EndStatNLContext):
        pass

    # Exit a parse tree produced by MATLABParser#endStatNL.
    def exitEndStatNL(self, ctx:MATLABParser.EndStatNLContext):
        pass


    # Enter a parse tree produced by MATLABParser#partialFunctionDecl.
    def enterPartialFunctionDecl(self, ctx:MATLABParser.PartialFunctionDeclContext):
        self.add_token(FUNC_BEGIN, ctx.start)

    # Exit a parse tree produced by MATLABParser#partialFunctionDecl.
    def exitPartialFunctionDecl(self, ctx:MATLABParser.PartialFunctionDeclContext):
        self.add_token(FUNC_END, ctx.start)


    # Enter a parse tree produced by MATLABParser#functionDecl.
    def enterFunctionDecl(self, ctx:MATLABParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by MATLABParser#functionDecl.
    def exitFunctionDecl(self, ctx:MATLABParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by MATLABParser#methodDecl.
    def enterMethodDecl(self, ctx:MATLABParser.MethodDeclContext):
        pass

    # Exit a parse tree produced by MATLABParser#methodDecl.
    def exitMethodDecl(self, ctx:MATLABParser.MethodDeclContext):
        pass


    # Enter a parse tree produced by MATLABParser#classDecl.
    def enterClassDecl(self, ctx:MATLABParser.ClassDeclContext):
        self.add_token(CLASS_BEGIN, ctx.start)

    # Exit a parse tree produced by MATLABParser#classDecl.
    def exitClassDecl(self, ctx:MATLABParser.ClassDeclContext):
        self.add_token(CLASS_END, ctx.start)


    # Enter a parse tree produced by MATLABParser#propBlockDecl.
    def enterPropBlockDecl(self, ctx:MATLABParser.PropBlockDeclContext):
        pass

    # Exit a parse tree produced by MATLABParser#propBlockDecl.
    def exitPropBlockDecl(self, ctx:MATLABParser.PropBlockDeclContext):
        pass


    # Enter a parse tree produced by MATLABParser#methodBlockDecl.
    def enterMethodBlockDecl(self, ctx:MATLABParser.MethodBlockDeclContext):
        pass

    # Exit a parse tree produced by MATLABParser#methodBlockDecl.
    def exitMethodBlockDecl(self, ctx:MATLABParser.MethodBlockDeclContext):
        pass


    # Enter a parse tree produced by MATLABParser#outArgs.
    def enterOutArgs(self, ctx:MATLABParser.OutArgsContext):
        pass

    # Exit a parse tree produced by MATLABParser#outArgs.
    def exitOutArgs(self, ctx:MATLABParser.OutArgsContext):
        pass


    # Enter a parse tree produced by MATLABParser#inArgs.
    def enterInArgs(self, ctx:MATLABParser.InArgsContext):
        pass

    # Exit a parse tree produced by MATLABParser#inArgs.
    def exitInArgs(self, ctx:MATLABParser.InArgsContext):
        pass


    # Enter a parse tree produced by MATLABParser#prop.
    def enterProp(self, ctx:MATLABParser.PropContext):
        pass

    # Exit a parse tree produced by MATLABParser#prop.
    def exitProp(self, ctx:MATLABParser.PropContext):
        pass


    # Enter a parse tree produced by MATLABParser#dotRef.
    def enterDotRef(self, ctx:MATLABParser.DotRefContext):
        if ctx.DOT() is not None and ctx.DOT() != []:
            self.add_token(APPLY, ctx.start)
            # TODO: maybe `APPLY` should represent `(`

    # Exit a parse tree produced by MATLABParser#dotRef.
    def exitDotRef(self, ctx:MATLABParser.DotRefContext):
        pass


    # Enter a parse tree produced by MATLABParser#statBlock.
    def enterStatBlock(self, ctx:MATLABParser.StatBlockContext):
        pass

    # Exit a parse tree produced by MATLABParser#statBlock.
    def exitStatBlock(self, ctx:MATLABParser.StatBlockContext):
        pass


    # Enter a parse tree produced by MATLABParser#ifStat.
    def enterIfStat(self, ctx:MATLABParser.IfStatContext):
        self.add_token(IF_BEGIN, ctx.start)

    # Exit a parse tree produced by MATLABParser#ifStat.
    def exitIfStat(self, ctx:MATLABParser.IfStatContext):
        self.add_token(IF_END, ctx.start)


    # Enter a parse tree produced by MATLABParser#whileStat.
    def enterWhileStat(self, ctx:MATLABParser.WhileStatContext):
        self.add_token(WHILE_BEGIN, ctx.start)

    # Exit a parse tree produced by MATLABParser#whileStat.
    def exitWhileStat(self, ctx:MATLABParser.WhileStatContext):
        self.add_token(WHILE_END, ctx.start)


    # Enter a parse tree produced by MATLABParser#forStat.
    def enterForStat(self, ctx:MATLABParser.ForStatContext):
        self.add_token(FOR_BEGIN, ctx.start)

    # Exit a parse tree produced by MATLABParser#forStat.
    def exitForStat(self, ctx:MATLABParser.ForStatContext):
        self.add_token(FOR_END, ctx.start)


    # Enter a parse tree produced by MATLABParser#switchStat.
    def enterSwitchStat(self, ctx:MATLABParser.SwitchStatContext):
        self.add_token(SWITCH_BEGIN, ctx.start)

    # Exit a parse tree produced by MATLABParser#switchStat.
    def exitSwitchStat(self, ctx:MATLABParser.SwitchStatContext):
        self.add_token(SWITCH_END, ctx.start)


    # Enter a parse tree produced by MATLABParser#caseStat.
    def enterCaseStat(self, ctx:MATLABParser.CaseStatContext):
        self.add_token(CASE, ctx.start)

    # Exit a parse tree produced by MATLABParser#caseStat.
    def exitCaseStat(self, ctx:MATLABParser.CaseStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#otherwiseStat.
    def enterOtherwiseStat(self, ctx:MATLABParser.OtherwiseStatContext):
        self.add_token(CASE, ctx.start)

    # Exit a parse tree produced by MATLABParser#otherwiseStat.
    def exitOtherwiseStat(self, ctx:MATLABParser.OtherwiseStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#jumpStat.
    def enterJumpStat(self, ctx:MATLABParser.JumpStatContext):
        if ctx.BREAK() is not None:
            self.add_token(BREAK, ctx.start)
        elif ctx.CONTINUE() is not None:
            self.add_token(CONTINUE, ctx.start)
        elif ctx.RETURN() is not None:
            self.add_token(RETURN, ctx.start)

    # Exit a parse tree produced by MATLABParser#jumpStat.
    def exitJumpStat(self, ctx:MATLABParser.JumpStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#stat.
    def enterStat(self, ctx:MATLABParser.StatContext):
        return

    # Exit a parse tree produced by MATLABParser#stat.
    def exitStat(self, ctx:MATLABParser.StatContext):
        pass


    # Enter a parse tree produced by MATLABParser#arrayExpr.
    def enterArrayExpr(self, ctx:MATLABParser.ArrayExprContext):
        self.add_token(ARRAY, ctx.start)

    # Exit a parse tree produced by MATLABParser#arrayExpr.
    def exitArrayExpr(self, ctx:MATLABParser.ArrayExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#cellExpr.
    def enterCellExpr(self, ctx:MATLABParser.CellExprContext):
        self.add_token(ARRAY, ctx.start)

    # Exit a parse tree produced by MATLABParser#cellExpr.
    def exitCellExpr(self, ctx:MATLABParser.CellExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#basicExpr.
    def enterBasicExpr(self, ctx:MATLABParser.BasicExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#basicExpr.
    def exitBasicExpr(self, ctx:MATLABParser.BasicExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#listExpr.
    def enterListExpr(self, ctx:MATLABParser.ListExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#listExpr.
    def exitListExpr(self, ctx:MATLABParser.ListExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#logicExpr.
    def enterLogicExpr(self, ctx:MATLABParser.LogicExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#logicExpr.
    def exitLogicExpr(self, ctx:MATLABParser.LogicExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#compExpr.
    def enterCompExpr(self, ctx:MATLABParser.CompExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#compExpr.
    def exitCompExpr(self, ctx:MATLABParser.CompExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#colonExpr.
    def enterColonExpr(self, ctx:MATLABParser.ColonExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#colonExpr.
    def exitColonExpr(self, ctx:MATLABParser.ColonExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:MATLABParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:MATLABParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:MATLABParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:MATLABParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#signExpr.
    def enterSignExpr(self, ctx:MATLABParser.SignExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#signExpr.
    def exitSignExpr(self, ctx:MATLABParser.SignExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#powExpr.
    def enterPowExpr(self, ctx:MATLABParser.PowExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#powExpr.
    def exitPowExpr(self, ctx:MATLABParser.PowExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#transposeExpr.
    def enterTransposeExpr(self, ctx:MATLABParser.TransposeExprContext):
        if ctx.TRANS() is not None or ctx.CTRANS() is not None:
            self.add_token(TRANSPOSE, ctx.start)

    # Exit a parse tree produced by MATLABParser#transposeExpr.
    def exitTransposeExpr(self, ctx:MATLABParser.TransposeExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#exprList.
    def enterExprList(self, ctx:MATLABParser.ExprListContext):
        pass

    # Exit a parse tree produced by MATLABParser#exprList.
    def exitExprList(self, ctx:MATLABParser.ExprListContext):
        pass


    # Enter a parse tree produced by MATLABParser#expr.
    def enterExpr(self, ctx:MATLABParser.ExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#expr.
    def exitExpr(self, ctx:MATLABParser.ExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#hcat.
    def enterHcat(self, ctx:MATLABParser.HcatContext):
        pass

    # Exit a parse tree produced by MATLABParser#hcat.
    def exitHcat(self, ctx:MATLABParser.HcatContext):
        pass


    # Enter a parse tree produced by MATLABParser#vcat.
    def enterVcat(self, ctx:MATLABParser.VcatContext):
        pass

    # Exit a parse tree produced by MATLABParser#vcat.
    def exitVcat(self, ctx:MATLABParser.VcatContext):
        pass

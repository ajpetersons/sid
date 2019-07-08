# Generated from MATLABParser.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MATLABParser import MATLABParser
else:
    from MATLABParser import MATLABParser

# This class defines a complete listener for a parse tree produced by MATLABParser.
class MATLABParserListener(ParseTreeListener):

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
        pass

    # Exit a parse tree produced by MATLABParser#partialFunctionDecl.
    def exitPartialFunctionDecl(self, ctx:MATLABParser.PartialFunctionDeclContext):
        pass


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
        pass

    # Exit a parse tree produced by MATLABParser#classDecl.
    def exitClassDecl(self, ctx:MATLABParser.ClassDeclContext):
        pass


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
        pass

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
        pass

    # Exit a parse tree produced by MATLABParser#ifStat.
    def exitIfStat(self, ctx:MATLABParser.IfStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#whileStat.
    def enterWhileStat(self, ctx:MATLABParser.WhileStatContext):
        pass

    # Exit a parse tree produced by MATLABParser#whileStat.
    def exitWhileStat(self, ctx:MATLABParser.WhileStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#forStat.
    def enterForStat(self, ctx:MATLABParser.ForStatContext):
        pass

    # Exit a parse tree produced by MATLABParser#forStat.
    def exitForStat(self, ctx:MATLABParser.ForStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#switchStat.
    def enterSwitchStat(self, ctx:MATLABParser.SwitchStatContext):
        pass

    # Exit a parse tree produced by MATLABParser#switchStat.
    def exitSwitchStat(self, ctx:MATLABParser.SwitchStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#caseStat.
    def enterCaseStat(self, ctx:MATLABParser.CaseStatContext):
        pass

    # Exit a parse tree produced by MATLABParser#caseStat.
    def exitCaseStat(self, ctx:MATLABParser.CaseStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#otherwiseStat.
    def enterOtherwiseStat(self, ctx:MATLABParser.OtherwiseStatContext):
        pass

    # Exit a parse tree produced by MATLABParser#otherwiseStat.
    def exitOtherwiseStat(self, ctx:MATLABParser.OtherwiseStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#jumpStat.
    def enterJumpStat(self, ctx:MATLABParser.JumpStatContext):
        pass

    # Exit a parse tree produced by MATLABParser#jumpStat.
    def exitJumpStat(self, ctx:MATLABParser.JumpStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#clearStat.
    def enterClearStat(self, ctx:MATLABParser.ClearStatContext):
        pass

    # Exit a parse tree produced by MATLABParser#clearStat.
    def exitClearStat(self, ctx:MATLABParser.ClearStatContext):
        pass


    # Enter a parse tree produced by MATLABParser#stat.
    def enterStat(self, ctx:MATLABParser.StatContext):
        pass

    # Exit a parse tree produced by MATLABParser#stat.
    def exitStat(self, ctx:MATLABParser.StatContext):
        pass


    # Enter a parse tree produced by MATLABParser#expr.
    def enterExpr(self, ctx:MATLABParser.ExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#expr.
    def exitExpr(self, ctx:MATLABParser.ExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#funcExpr.
    def enterFuncExpr(self, ctx:MATLABParser.FuncExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#funcExpr.
    def exitFuncExpr(self, ctx:MATLABParser.FuncExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#exprList.
    def enterExprList(self, ctx:MATLABParser.ExprListContext):
        pass

    # Exit a parse tree produced by MATLABParser#exprList.
    def exitExprList(self, ctx:MATLABParser.ExprListContext):
        pass


    # Enter a parse tree produced by MATLABParser#listExpr.
    def enterListExpr(self, ctx:MATLABParser.ListExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#listExpr.
    def exitListExpr(self, ctx:MATLABParser.ListExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#arrayExpr.
    def enterArrayExpr(self, ctx:MATLABParser.ArrayExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#arrayExpr.
    def exitArrayExpr(self, ctx:MATLABParser.ArrayExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#cellExpr.
    def enterCellExpr(self, ctx:MATLABParser.CellExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#cellExpr.
    def exitCellExpr(self, ctx:MATLABParser.CellExprContext):
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
        pass

    # Exit a parse tree produced by MATLABParser#transposeExpr.
    def exitTransposeExpr(self, ctx:MATLABParser.TransposeExprContext):
        pass


    # Enter a parse tree produced by MATLABParser#basicExpr.
    def enterBasicExpr(self, ctx:MATLABParser.BasicExprContext):
        pass

    # Exit a parse tree produced by MATLABParser#basicExpr.
    def exitBasicExpr(self, ctx:MATLABParser.BasicExprContext):
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



#!/usr/bin/python3

import os
import sys
sys.path.insert(0, os.path.join("..", "turtparse"))

from turtparse.tlangParser import tlangParser
from turtparse.tlangVisitor import tlangVisitor

from kast import kachuaAST


class astGenPass(tlangVisitor):

    def __init__(self):
        self.repeatInstrCount = 0 # keeps count for no of 'repeat' instructions

    def visitStart(self, ctx:tlangParser.StartContext):
        stmtList = self.visit(ctx.instruction_list())
        return stmtList

    def visitInstruction_list(self, ctx:tlangParser.Instruction_listContext):
        instrList = []
        for instr in ctx.instruction():
            instrList.extend(self.visit(instr))

        return instrList

    def visitStrict_ilist(self, ctx:tlangParser.Strict_ilistContext):
	# TODO: code refactoring. visitInstruction_list and visitStrict_ilist have same body
        instrList = []
        for instr in ctx.instruction():
            visvalue = self.visit(instr)
            instrList.extend(visvalue)

        return instrList


    def visitAssignment(self, ctx:tlangParser.AssignmentContext):
        lval = kachuaAST.Var(ctx.VAR().getText())
        rval = self.visit(ctx.expression())
        return [(kachuaAST.AssignmentCommand(lval, rval), 1)]


    def visitIfConditional(self, ctx:tlangParser.IfConditionalContext):
        condObj = kachuaAST.ConditionCommand(self.visit(ctx.condition()))
        thenInstrList = self.visit(ctx.strict_ilist())
        return [(condObj, len(thenInstrList) + 1)] + thenInstrList

    def visitIfElseConditional(self, ctx:tlangParser.IfElseConditionalContext):
        condObj = kachuaAST.ConditionCommand(self.visit(ctx.condition()))
        thenInstrList = self.visit(ctx.strict_ilist(0))
        elseInstrList = self.visit(ctx.strict_ilist(1))
        jumpOverElseBlock = [(kachuaAST.ConditionCommand(kachuaAST.BoolFalse()), len(elseInstrList) + 1)]
        return [(condObj, len(thenInstrList) + 2)] + thenInstrList + jumpOverElseBlock + elseInstrList

    def visitGotoCommand(self, ctx:tlangParser.GotoCommandContext):
        xcor = self.visit(ctx.expression(0))
        ycor = self.visit(ctx.expression(1))
        return [(kachuaAST.GotoCommand(xcor, ycor), 1)]
    
    def visitExpression(self, ctx:tlangParser.ExpressionContext):
        if ctx.value():
            return self.visit(ctx.value())

        if ctx.unaryArithOp():
            expr1 = self.visit(ctx.expression(0))
            if ctx.unaryArithOp().MINUS():
                return kachuaAST.UMinus(expr1)
        
        if ctx.binArithOp():
            binOpCtx = ctx.binArithOp()
            expr1 = self.visit(ctx.expression(0))
            expr2 = self.visit(ctx.expression(1))
            if binOpCtx.PLUS():
                return kachuaAST.Sum(expr1, expr2)
            elif binOpCtx.MINUS():
                return kachuaAST.Diff(expr1, expr2)
            elif binOpCtx.PRODUCT():
                return kachuaAST.Mult(expr1, expr2)
            elif binOpCtx.DIV():
                return kachuaAST.Div(expr1, expr2)

        if ctx.expression():
            # expression in paranthesis
            return self.visit(ctx.expression(0))

        return self.visitChildren(ctx)

    def visitCondition(self, ctx:tlangParser.ConditionContext):
        if ctx.PENCOND():
            return kachuaAST.PenStatus();        

        if ctx.NOT():
            expr1 = self.visit(ctx.condition(0))        
            return kachuaAST.NOT(expr1)


        if ctx.logicOp():
            expr1 = self.visit(ctx.condition(0))
            expr2 = self.visit(ctx.condition(1))
            logicOpCtx = ctx.logicOp()

            if logicOpCtx.AND():
                return kachuaAST.AND(expr1, expr2)
            elif logicOpCtx.OR():
                return kachuaAST.OR(expr1, expr2)

        
        if ctx.binCondOp():
            expr1 = self.visit(ctx.expression(0))
            expr2 = self.visit(ctx.expression(1))
            binOpCtx = ctx.binCondOp()

            if binOpCtx.LT():
                return kachuaAST.LT(expr1, expr2)
            elif binOpCtx.GT():
                return kachuaAST.GT(expr1, expr2)
            elif binOpCtx.EQ():
                return kachuaAST.EQ(expr1, expr2)
            elif binOpCtx.NEQ():
                return kachuaAST.NEQ(expr1, expr2)
            elif binOpCtx.LTE():
                return kachuaAST.LTE(expr1, expr2)
            elif binOpCtx.GTE():
                return kachuaAST.GTE(expr1, expr2)

        if ctx.condition():
            # condition is inside paranthesis
            return self.visit(ctx.condition(0))
            
        return self.visitChildren(ctx)

    def visitValue(self, ctx:tlangParser.ValueContext):
        if ctx.NUM():
            return kachuaAST.Num(ctx.NUM().getText())
        elif ctx.VAR():
            return kachuaAST.Var(ctx.VAR().getText())

    def visitLoop(self, ctx:tlangParser.LoopContext):
        # insert counter variable in IR for tracking repeat count
        self.repeatInstrCount += 1
        repeatNum = self.visit(ctx.value())
        counterVar = kachuaAST.Var(":__rep_counter_" + str(self.repeatInstrCount))
        counterVarInitInstr = kachuaAST.AssignmentCommand(counterVar, repeatNum)
        constZero = kachuaAST.Num(0)
        constOne = kachuaAST.Num(1)
        loopCond = kachuaAST.ConditionCommand(kachuaAST.NEQ(counterVar, constZero))
        counterVarDecrInstr = kachuaAST.AssignmentCommand(counterVar, kachuaAST.Diff(counterVar, constOne))
        
        thenInstrList = []
        for instr in ctx.strict_ilist().instruction():
            temp = self.visit(instr)
            thenInstrList.extend(temp)
                
        boolFalse = kachuaAST.ConditionCommand(kachuaAST.BoolFalse())
        return [(counterVarInitInstr, 1), (loopCond, len(thenInstrList) + 3)] + thenInstrList +\
            [(counterVarDecrInstr, 1), (boolFalse, -len(thenInstrList) - 2)]

    def visitMoveCommand(self, ctx:tlangParser.MoveCommandContext):
        mvcommand = ctx.moveOp().getText()
        mvexpr = self.visit(ctx.expression())
        return [(kachuaAST.MoveCommand(mvcommand, mvexpr), 1)]

    def visitPenCommand(self, ctx:tlangParser.PenCommandContext):
        return [(kachuaAST.PenCommand(ctx.getText()), 1)]

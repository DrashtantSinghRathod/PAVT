import copy
import math
import sys
from typing import overload

sys.path.insert(0, "../KachuaCore/")

import cfg.kachuaCFG as cfgK
import cfg.cfgBuilder as cfgB
from interfaces.abstractInterpretationInterface import  *
import kast.kachuaAST as kachuaAST
import abstractInterpretation as AI

'''
    Class for interval domain
'''
class Interval(abstractValueBase):

    '''Initialize abstract value'''
    def __init__(self, data):
        pass

    '''To display abstract values'''
    def __str__(self):
        pass

    '''To check whether abstract value is bot or not'''
    def isBot(self):
        pass

    '''To check whether abstract value is Top or not'''
    def isTop(self):
        pass

    '''Implement the meet operator'''
    def meet(self, other):
        pass

    '''Implement the join operator'''
    def join(self, other):
        pass

    '''partial order with the other abstract value'''
    def __le__(self, other):
        pass

    '''equality check with other abstract value'''
    def __eq__(self, other):
        pass

    '''
        Add here required abstract transformers
    '''
    pass


class ForwardAnalysis():
    def __init__(self):
        pass

    '''
        This function is to initialize in of the basic block currBB
        Returns a dictinary {varName -> abstractValues}
        isStartNode is a flag for stating whether currBB is start basic block or not
    '''
    def initialize(self, currBB, isStartNode):
        val = {}
        #Your additional initialisation code if any
        return val

    #just a dummy equallity check function for dictionary
    def isEqual(self, dA, dB):
        for i in dA.keys():
            if i not in dB.keys():
                return False
            if dA[i] != dB[i]:
                return False
        return True

    '''
        Transfer function for basic block 'currBB' 
        args: In val for currBB, currBB
        Returns newly calculated values in a form of list
    '''
    def transferFunction(self, currBBIN, currBB):
        #implement your transfer function here
        outVal = []
        return outVal

    '''
        Define the meet operation
        Returns a dictinary {varName -> abstractValues}
    '''
    def meet(self, predList):
        assert isinstance(predList, list)
        meetVal = {}

        return meetVal

def analyzeUsingAI(ir, filename):
    '''
        get the cfg outof IR
        each basic block consists of single statement
    '''
    cfg = cfgB.buildCFG(ir, "cfg", True)
    cfgB.dumpCFG(cfg, "x")

    # call worklist and get the in/out values of each basic block
    bbIn, bbOut = AI.worklistAlgorithm(cfg)

    #implement your analysis according to the questions on each basic blocks
    pass

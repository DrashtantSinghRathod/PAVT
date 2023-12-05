import copy
import math
import sys
from typing import overload

sys.path.insert(0, "../KachuaCore/")

import cfg.kachuaCFG as cfgK
import cfg.cfgBuilder as cfgB
from interfaces.dataFlowAnalysisInterface import  *
import kast.kachuaAST as kachuaAST
import dataFlowAnalysis as DFA


'''
    Class to work with lattice elements.
    Implement these functions as required.
'''
class latticeValue(latticeValueBase):

    '''Initialize lattice value'''
    def __init__(self, data):
        pass

    '''To display lattice values'''
    def __str__(self):
        pass

    '''To check whether lattice value is bot or not'''
    def isBot(self):
        pass

    '''To check whether lattice value is Top or not'''
    def isTop(self):
        pass

    '''Implement the meet operator'''
    def meet(self, other):
        pass

    '''Implement the join operator'''
    def join(self, other):
        pass

    '''partial order with the other lattice value'''
    def __le__(self, other):
        pass

    '''equality check with other lattice value'''
    def __eq__(self, other):
        pass

    '''
        Add here required lattice operations
    '''
    pass


class ForwardAnalysis():
    def __init__(self):
        pass

    '''
        This function is to initialize in of the basic block currBB
        Returns a dictinary {varName -> latticeValues}
        isStartNode is a flag for stating whether currBB is start basic block or not
    '''
    def initialize(self, currBB, isStartNode):
        val = {}
        #Your additional initialisation code if any
        return val

    # just a dummy equallity check function for dictionary
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
        Define the meet operation. 
        Implement this function as required.
        Returns a dictinary {varName -> latticeValues}
    '''
    def meet(self, predList):
        assert isinstance(predList, list)
        meetVal = {}

        return meetVal

def analyzeUsingDFA(ir):
    '''
        get the cfg out of IR
        each basic block consists of single statement
    '''
    # Create a list single statement basic blocks. 
    cfg = cfgB.buildCFG(ir, "cfg", True)
    # Dump the CFG diagram to a file 'cfgView.png'.  
    cfgB.dumpCFG(cfg, "cfgView")

    # call worklist and get the in/out values of each basic block
    bbIn, bbOut = DFA.worklistAlgorithm(cfg)


    # NOTE: Implement your code below. Do not change anything above this line.
    # Implement your analysis according to the questions on each basic block

    
    
    # TODO: Return the optimized IR in optIR
    optIR = ir
    return optIR

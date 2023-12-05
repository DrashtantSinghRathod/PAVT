'''
    This file implements the worklist algorithm.
    WorkList class is the class for worklist queue
    and necessary functions to operate on the worklist.
    worklistAlgorithm actually implements the worklist algorithm.
'''

from queue import Queue
import sys
import cfg.cfgBuilder as cfgB
import cfg.kachuaCFG as cfgK

sys.path.insert(0, '../Submission/')
from submissionDFA import *

class WorkList():
    '''
        initialize the worklist with the basic blocks list
    '''
    def __init__(self, BBList):
        self.worklist = Queue(maxsize = 0)
        for i in BBList:
            if i.name == "END": continue
            self.worklist.put(i)

    def enQueue(self, obj):
        if not isinstance(obj, cfgK.BasicBlock):
            raise ValueError("Enqueue Basic Block only")
        if self.worklist.full():
            print("Worklist is full")
            raise ValueError("Worklist is full")
        self.worklist.put(obj)
    
    def deQueue(self):
        if self.worklist.empty():
            print("Worklist is empty")
            return None
        obj = self.worklist.get()
        return obj

    def isEmpty(self):
        return self.worklist.empty()
    
    def getSize(self):
        return self.worklist.qsize()
    

#just a dummy equallity check function
def isDifferent(dA, dB):
    for i in dA.keys():
        if i not in dB.keys():
            return True
        if dA[i] != dB[i]:
            return True
    return False


'''
    return True if newOut is different than their older values(oldOut)
    before calling to the TransferFunction
'''
def isChanged(newOut, oldOut):
    assert isinstance(newOut, list)
    assert isinstance(oldOut, list)
    if len(newOut) != len(oldOut):
        return True
    flag = False
    for i in range(len(newOut)):
        flag = (flag or isDifferent(newOut[i], oldOut[i]))

    return flag


def worklistAlgorithm(cfg):
    BBlist = cfg.nodes()
    '''
        initializing the worklist with the basic block list
    '''
    wList = WorkList(BBlist)

    fa = ForwardAnalysis()

    '''
        It is an map from name of the BB to the in and out info of program states
    '''
    bbIn = {}
    bbOut = {}

    '''
        initialise in/out of entry/exit point
    '''
    for i in BBlist:
        bbIn[i.name] = fa.initialize(i, i.name == "START")
        bbOut[i.name] = []

    while not wList.isEmpty():
        currBB = wList.deQueue()
        oldOut = bbOut[currBB.name]

        predList = [p for p in cfg.predecessors(currBB)]
        
        # cumulate the out of the pred list
        inlist = []
        for pred in predList:
            label = cfg.get_edge_label(pred, currBB)
            if bbOut[pred.name]:
                inlist.append(bbOut[pred.name][0])
               
        # calling meet operation over inlist
        if inlist:
            currInVal = fa.meet(inlist)
            assert isinstance(currInVal, dict)
            #assign the returned value to the in of currBB
            bbIn[currBB.name] = currInVal

        #calling transfer function
        currBBOutVal = fa.transferFunction(bbIn[currBB.name], currBB)

        '''
            1) type(currBBOutVal) = list
            2) len(currBBOutVal)  = 1
        '''

        assert isinstance(currBBOutVal, list)
        bbOut[currBB.name] = currBBOutVal

        if isChanged(bbOut[currBB.name], oldOut):
            nextBBList = cfg.successors(currBB)
            for i in nextBBList:
                wList.enQueue(i)

    #print("Worklist empty")
    return bbIn, bbOut




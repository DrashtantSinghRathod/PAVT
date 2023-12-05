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
import irgen as irg


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
        #print("init")
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
        outVal = []
        
        print(currBB.irID)
        if(currBB.irID=="END"):
             return []
        #print(currBB.instrlist[0][0])
       
        
        if not (bool(currBBIN)):
             if(isinstance(currBB.instrlist[0][0],kachuaAST.MoveCommand)):
          
                 pass
                 #print(currBB.instrlist[0][0].direction)
                 #print(currBB.instrlist[0][0].expr)
             if(isinstance(currBB.instrlist[0][0],kachuaAST.PenCommand)):
                
                 outVal.append({currBB.irID:currBB.instrlist[0][0].status})
        else:
            if(isinstance(currBB.instrlist[0][0],kachuaAST.MoveCommand)):
          
               
                 #print(currBB.instrlist[0][0].direction)
                 #print(currBB.instrlist[0][0].expr)
                 for virid in currBBIN.values():
                      cv=virid
                 outVal.append({currBB.irID:cv})
            if(isinstance(currBB.instrlist[0][0],kachuaAST.PenCommand)):
                for pr in currBBIN.values():
                    
                  if(pr=="pendown" and str(currBB.instrlist[0][0].status)=="penup"):
                         outVal.append({currBB.irID:currBB.instrlist[0][0].status})  
                  elif(pr=="penup" and (currBB.instrlist[0][0].status)=="pendown"):
                         outVal.append({currBB.irID:currBB.instrlist[0][0].status})  
                  else :
                     outVal.append({currBB.irID:currBB.instrlist[0][0].status}) 
            
               
               
        #implement your transfer function here

        

        print("out",outVal)
        return outVal

    '''
        Define the meet operation. 
        Implement this function as required.
        Returns a dictinary {varName -> latticeValues}
    '''
    def meet(self, predList):
        
        assert isinstance(predList, list)
        meetVal = {}
        
        for pk,pv in predList[0].items():
            if(str(pv)=="pendown") :
                 for pr in predList[0].keys():
                   meetVal[pr]="pendown"
            else :
                  for pr in predList[0].keys():
                   meetVal[pr]="penup"
               
        print("meet",meetVal)
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
    #print(ir.instrlist[0][0])
    print("BBIN->  ",bbIn)
    print("BBOUT->  ",bbOut)
  
    
    #print(type(ir[0]))
    #print(ir[0][0])
    #print(type(ir[0][0]))
    flag=0
    x=0
    y=0
    
    #print(type(bbOut['1'][0]))
    xydata=[]
    for i in ir:
    
         
         y=y+1
         if(flag==0):
          if(isinstance(i[0],kachuaAST.PenCommand)):
             if(str(i[0].status)=="pendown"):
               
               
               continue
          if(isinstance(i[0],kachuaAST.MoveCommand)):
               continue
          if(isinstance(i[0],kachuaAST.PenCommand)):
             if(str(i[0].status)=="penup"):
               
               flag=1
              
               continue
         if(flag==1):
         
             
           
           if(isinstance(i[0],kachuaAST.MoveCommand)):
             irg.removeInstruction(ir,y-1)
             #print("movein")
             if(str(i[0].direction)=="forward"):
                   x=x+int(str(i[0].expr))
             if(str(i[0].direction)=="backward"):
                   x=x-int(str(i[0].expr))
             #print(x)
            
           if(isinstance(i[0],kachuaAST.PenCommand)):
             
             if(str(i[0].status)=="pendown"):
           
              xydata.append((x,y))
              x=0
              flag=0
           if(isinstance(i[0],kachuaAST.PenCommand)):
            
             if(str(i[0].status)=="penup"):
           
              xydata.append((x,y))
              x=0
              flag=0
           
    t=2
    for m in xydata:
     t=t-1
     #print(m[0])
     irg.addInstruction(ir,kachuaAST.MoveCommand("forward",m[0]),m[1]-t)
     
         
    
           
       
              
   # for i in ir:
       
    #   if(isinstance(i[0],kachuaAST.PenCommand)):
     #     if(i[0].status=="penup"):
      #       print("true")
           
       #if(isinstance(i[0],kachuaAST.MoveCommand)):
        #      irg.removeInstruction(ir,y)
       #       x=x+int(str(i[0].expr))
      #  y=y+1
    #irg.addInstruction(ir,kachuaAST.MoveCommand("forward",x),y-1)
    #addInstruction(ir, kachuaAST.AssignmentCommand(kachuaAST.Var(":vara"), kachuaAST.Num(5)), 11)
           
     #removeInstruction(ir, 11)         
                    
                
   
    
    # TODO: Return the optimized IR in optIR
    optIR = ir
    return optIR

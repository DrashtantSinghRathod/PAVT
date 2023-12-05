import copy
import math
from z3 import *
import argparse
import json
import numbers

import sys
from typing import overload

sys.path.insert(0, "../KachuaCore/")

import cfg.kachuaCFG as cfgK
import cfg.cfgBuilder as cfgB
from interfaces.abstractInterpretationInterface import  *
import kast.kachuaAST as kachuaAST
import abstractInterpretation as AI
import irgen as irg

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
        x=0
        y=0
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
        print("transferv function")
        #implement your transfer function here
        outVal=[]
        
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
            
               
        return outVal

    '''
        Define the meet operation
        Returns a dictinary {varName -> abstractValues}
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
    print("BBIN->  ",bbIn)
    print("BBOUT->  ",bbOut)
    print(filename)  
    
    #print(type(ir[0]))
    #print(ir[0][0])
    #print(type(ir[0][0]))
    
    x=[0,0]
    y=[0,0]
    invar=[-50,50]
    #print(type(bbOut['1'][0]))
    xydata=[]
    z=0
    varr={}
    flag=1
    fbit=0
    for i in ir:
      if(flag>1):
              flag=flag-1
              #print(flag)
              continue
      
      if(flag==1):
           
           m=0
           
           
           if(isinstance(i[0],kachuaAST.AssignmentCommand)):   
                varr[str(i[0].lvar)]=int(str(i[0].rexpr))
                print(varr)
           if(isinstance(i[0],kachuaAST.ConditionCommand)):
               st=str(i[0].cond)
               if(eval(st)):
                 #print("true")
                 flag=1
                 #print(flag)
               if(st=='False'):
                 #print("true")
                 flag=i[1]-1
                 #print(flag)
               continue
                      
          
              
                
           
           if(isinstance(i[0],kachuaAST.MoveCommand)):

             

             if(str(i[0].direction)=="forward"):
                   #print(i[0].expr)
                   string=""
                   string=str(i[0].expr)
                   
                      
                   if (string[0]==':'):
                       fbit=1

                       for k,v in varr.items():
                          if(k==string):
                            #print(v)
                            fbit=0
                            m=m+v
                           
                   #if(isinstance(int(str(i[0].expr)),numbers.Number)):
                       #print("rghnjmnvbnybhvgbnynjbgvgbnyt")
                      
                   else:
                           m=m+int(str(i[0].expr))

                   
             if(str(i[0].direction)=="left"):
                   z=z+int(str(i[0].expr))
             if(str(i[0].direction)=="right"):
                   z=z-int(str(i[0].expr))
             
             if(str(i[0].direction)=="backward"):
                   string=""
                   string=str(i[0].expr)
                   
                   if (string[0]==':'):
                           fbit=1
                           for k,v in varr.items():
                             if(k==string):
                               #print(v)
                               fbit=0
                               m=m-v
                           
                   #if(isinstance(int(str(i[0].expr)),numbers.Number)):
                       #print("rghnjmnvbnybhvgbnynjbgvgbnyt")
                      
                   else:
                          m=m-int(str(i[0].expr))            

                   
             
            
           if(isinstance(i[0],kachuaAST.PenCommand)):
             
              continue
           if(fbit==1):
            fbit=0
            if(z%360==0):
               x[0]=x[0]+invar[0]
               x[1]=x[1]+invar[1]
               
            if(z%360==90):
               y[0]=y[0]+invar[0]
               y[1]=y[1]+invar[1]
            if(z%360==180):
              x[0]=x[0]-invar[1]
              x[1]=x[1]-invar[0]
            if(z%360==270):
               y[0]=y[0]+invar[0]
               y[1]=y[1]+invar[1]
            continue
           if(fbit==0):               
            if(z%360==0):
              # if(x[0]+m<x[0]):
                   x[0]=x[0]+m
               #if(x[1]+m>x[1]):
                   x[1]=x[1]+m
               
            if(z%360==90):
               #if(y[0]+m<y[0]):
                   y[0]=y[0]+m
               #if(y[1]+m>x[1]):
                   y[1]=y[1]+m
            if(z%360==180):
               #if(x[0]-m<x[0]):
                   x[0]=x[0]-m
               #if(x[1]-m>x[1]):
                   x[1]=x[1]-m
            if(z%360==270):
               #if(y[0]-m<y[0]):
                   y[0]=y[0]-m
               #if(y[1]-m>x[1]):
                   y[1]=y[1]-m
              
    print(x)
    print(y)
    file2 = open("../KachuaCore/"+filename.replace('.tl','.json'),"r+")
    testData=json.loads(file2.read())
    file2.close()
    #testData = convertTestData(testData)
    from collections import namedtuple
    Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

    ra = Rectangle(testData['reg'][0][0],testData['reg'][1][0], testData['reg'][0][1],testData['reg'][1][1])
    rb = Rectangle(x[0],y[0],x[1],y[1])
# intersection here is (3, 3, 4, 3.5), or an area of 1*.5=.5

    def area(a, b):  # returns None if rectangles don't intersect
       dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
       dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
       if (dx>=0) and (dy>=0):
          return dx*dy

    areaa=area(ra, rb)
    
      
    if(areaa==None):
         print("SAFE")
    else:
         print("UNSAFE")
    
           
   
    #implement your analysis according to the questions on each basic blocks
    

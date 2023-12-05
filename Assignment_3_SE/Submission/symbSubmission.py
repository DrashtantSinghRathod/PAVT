from z3 import *
import argparse
import json
import sys

sys.path.insert(0, '../KachuaCore/')

from sExecutionInterface import *
import z3solver as zs
from irgen import *
from interpreter import *
import ast

def example(s):
    # To add symbolic variable x to solver
    s.addSymbVar('x')
    s.addSymbVar('y')
    # To add constraint in form of string
    s.addConstraint('x==5+y')
    s.addConstraint('And(x==y,x>5)')
    # s.addConstraint('Implies(x==4,y==x+8')
    # To access solvers directly use s.s.<function of z3>()
    print("constraints added till now",s.s.assertions())
    # To assign z=x+y
    s.addAssignment('z','x+y')
    # To get any variable assigned
    print("variable assignment of z =",s.getVar('z'))

def checkEq(args,ir):

    file1 = open("../Submission/testData.json","r+")
    testData=json.loads(file1.read())
    file1.close()
    s = zs.z3Solver()
    s1=zs.z3Solver()
    s2=zs.z3Solver()
    testData = convertTestData(testData)
    print("sdgdbgzdrbnsdtdztnndyrymrsmntgyiitnbuymttymmminyuiyubyyynbtbbttdfurrqnweheuduvntyfcjvflnk")
    print(testData)
    # output = args.output
    # example(s)
    # TODO: write code to check equivalence
    
    

    #*****************
    
    file2 = open("../Submission/testData1.json","r+")
    testData1=json.loads(file2.read())
    file2.close()
    # s = zs.z3Solver()
    testData1 = convertTestData(testData1)
    print()
    print("***testdata1.json***")
    print(testData1)
    print("***testdata1.json***")
    print()
    
    
    
    
    for i in testData['1']['params']:
        print(i)
        s.addSymbVar(i)

    for i in testData:
       #st=[]
       for j in testData1: 
        
        fbit=1
        
        for var in args.output:
            if((testData[i]['params'][var])==(testData1[j]['params'][var])):
                fbit=fbit
            else:
                flag=0
        if fbit:
            string=testData[i]['symbEnc'][var]+"=="+testData1[i]['symbEnc'][var]
            #st.append(testData[i]['symbEnc'][var]+"=="+testData1[i]['symbEnc'][var])
            s.addConstraint(string)
            
            #print(testData[i]["constraints"])
        
         #   print(st)
      # for s11 in st:
      #    s1.addConstraint(s11)
      # for s12 in testData[i]["constraints"]:
      #    s2.addConstraint(s12)
       
     #  strn=str(s1.s.assertions())
      # strn2=str(s2.s.assertions())
      # print(strn)
      # print(strn2)
      # s.addConstraint('Implies(And('+strn2+'),And('+strn+'))')
                   
    print(s.s.check())
    print(s.s.model())



if __name__ == '__main__':
    cmdparser = argparse.ArgumentParser(
        description='symbSubmission for assignment Program Synthesis using Symbolic Execution')
    cmdparser.add_argument('progfl')
    cmdparser.add_argument(
        '-b', '--bin', action='store_true', help='load binary IR')
    cmdparser.add_argument(
        '-e', '--output', default=list(), type=ast.literal_eval,
                               help="pass variables to kachua program in python dictionary format")
    args = cmdparser.parse_args()
    ir = loadIR(args.progfl)
    checkEq(args,ir)
    exit()

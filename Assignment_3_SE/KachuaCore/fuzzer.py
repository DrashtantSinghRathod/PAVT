## Coverage Guided Fuzzing
 
"""
This file implements the main fuzzer loop.
Pick an input using a distribution, mutate it 
run the program with the mutated input and return 
coverage metric and compare to previous metric to 
check if we found any improvement due to the mutation. 

This loop continues until time limit is exhausted or we
ran out of inputs inorder to continue mutations for the 
fuzzer loop.
"""

import sys
import time
import random
import copy
import uuid
from interpreter import *
sys.path.insert(0, '../Submission/')
from fuzzSubmission import *

corpus = []

class InputObject():
    def __init__(self, data):
        self.id = str(uuid.uuid4())
        self.data = data
        # Flag to check if ever picked
        # for mutation or not.
        self.pickedOnce = False
        
class Executor():
    # Execute the program using the input from mutator
    def __init__(self):
        pass

    def execute(self, ir, inputList={}, end=0):
        coverage = []
        inptr = ConcreteInterpreter(ir)
        terminated = False
        inptr.initProgramContext(inputList)
        coverage.append(inptr.pc)
        # The maximum time for one execution of the 
        # fuzzed program must be less than end time.
        while time.time() <= end:
            terminated = inptr.interpret()
            # List of PC values -> Execution Trace -> Stmts Hit!
            coverage.append(inptr.pc)
            if terminated:
                break
        if time.time() >= end:
            print(f"[fuzz] Program took too long to execute. Terminated")
        else:
            print("[fuzz] Program Ended.")
        return list(set(coverage))

def populateCorpusDummy(corpus, varsList):
    # HonggFuzz starts with a buffer of atleast 
    # four elements. Lets start with 8 say.
    for test in range(8):
        inputDict = {}
        for variable in varsList:
            inputDict[variable] = random.randint(-10, 10)
        input_i = InputObject(data=inputDict)
        corpus.append(input_i)
    # print([x.data for x in corpus])
    # sys.exit(-1)

def fuzzMain(ir, params, timeLimit=0) :
    """[summary]

    Args:
        ir (List): List of program IR statments 
        params (dict): Mapped variables with initial assignments. 
        timeLimit (float/int): Total time(sec) to run the fuzzer loop for.

    Returns:
        tuple (coverageInfo, corpus) : Return coverage information and corpus of inputs.
    """

    # If Dummy List needed.
    # varList = []
    # for key, val in params.items():
    #     variable = key.replace(":", "").strip()
    #     varList.append(variable)
    # populateCorpusDummy(corpus, varList)

    # get the variables used in the program.
    executor = Executor()
    mutationOperator = CustomMutator() # From submission
    coverageInfo = CustomCoverageMetric() # From submission

    print(f"[fuzz] Starting Fuzzer : init args -> {params}")

    # Initial Seed values from user.
    temp_input = InputObject(data=params)
    corpus.append(temp_input)

    start_time = time.time()
    # Fuzzing ends at this timestamp.
    endTime = time.time() + timeLimit
    
    # Either supply dummy corpus
    # or use user-provided inputs.
    while True:
        # Initialize current coverage to empty as loop starts.
        coverageInfo.curr_metric = []
        
        # Pick a random input and choose it for mutation.
        pickedInput = random.choice(corpus)

        # Set this flag since the input is picked once now.
        pickedInput.pickedOnce = True
        print(f"[fuzz] Fuzzing with Input ID : {pickedInput.id}")
        pickInputRandom = copy.deepcopy(pickedInput)

        pickInputRandom.pickedOnce = False
        mutated_input = mutationOperator.mutate(pickInputRandom, coverageInfo, ir)

        # Get new coverage from execution.
        # The maximum time for one execution of the 
        # fuzzed program must be less than end time.
        coverageInfo.curr_metric = executor.execute(ir, mutated_input.data, end=endTime)
        # Print the coverage : Representational
        print(f"[fuzz] Coverge for execution : {coverageInfo.curr_metric}")

        # Check if coverage improved.
        if coverageInfo.compareCoverage(coverageInfo.curr_metric, coverageInfo.total_metric):
            mutated_input.id = str(uuid.uuid4())
            mutated_input.pickedOnce = False
            coverageInfo.total_metric = coverageInfo.updateTotalCoverage(coverageInfo.curr_metric, coverageInfo.total_metric)
            # Add mutated input if coverage improved.
            corpus.append(mutated_input)
        
        exhaustedBudget = True if time.time() >= endTime else False
        if exhaustedBudget:
            time_delta = time.time() - start_time
            print(f"[fuzz] Time Exhausted : {time_delta}")
            break
            
    print(f"[fuzz] Terminating Fuzzer Loop.")
    # Return coverage information and corpus of inputs.
    return (coverageInfo.total_metric, corpus)

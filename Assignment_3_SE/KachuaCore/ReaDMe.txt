
#Program Synthesis using Symbolic Execution:

#We have given two programs P1 and P2, we have to find values of constant assignments to variables in P1 (given using -c flag) such that it becomes semantically equivalent to P2.

#checkEq() function is to be implemented:
This function must returns assignments to constparams stored in testData.json such that the two programs equal for given test case

#Installations:

sudo apt-get install graphviz graphviz-dev
pip install pygraphviz

pip install numpy
pip install networkx
pip install z3

#Running the program:
cd KachuaCore

#Run the symbolic execution on both eqtest1.tl and eqtest2.tl:

./kachua.py -t 100 -se example/eqtest1.tl -d '{":x": 5, ":y": 100}' -c '{":c1": 1, ":c2": 1}'
#Optimize the program test.tl and generate an optimized IR (in binary form) called "optimized.kw"
./kachua.py -dfa example/eqtest2.tl

#Running checkEq() : (from Submission folder)
$ python3 symbSubmission.py -b eqtest2.kw -e '["x", "y"]'

#Tried for Constraint also 
I tried for the constraint also but the Output value of c1 and c2 are not coming Correct.

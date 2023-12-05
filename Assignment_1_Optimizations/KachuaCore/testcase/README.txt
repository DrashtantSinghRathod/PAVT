We had made a code for "kachua code optimization"
for which we have a proper code implemented from initial and 
we only have to implement 
                  1. Transfer function 
                  2. Meet Function
                  3. and Done optimization in AnalyzeusingDFA function

we had done optimization in a way,
                           that whenever there is a penup in IR from that 
to next pendown we optimizr all move commands
Used class function are :
                .status :{shows status of pen command}
                .expr :{shows value given to movestatement}
                .direction :{shows the direction of move command}
                .instrlist[0][0] :{shows the whole command in Basic Block}
                .irID :{shows the IrId of IR }

initialize: Define the lattice by initializing the
lattice values and the meet operator.

transferFunction: With the help of current INs of basic block,
 calculates the Outs of the Basic Block.

meet: Meet operation
      penup v penup  --> penup
      pendown v pendown  --> pendown
      penup v  pendown --> pendown

After defining the above functions, the code for 
optimization is written in analyzeUsingDFA function.

Installations:
pip install numpy
pip install z3
pip install networkx
sudo apt-get install graphviz graphviz-dev
pip install graph viz



Running the program to Optimize IR:
In KachuaCore-

1) Optimize the program testcase1.tl and generate an optimized IR (in binary form) called "optimized.kw".
./kachua.py -dfa testcase/testcase1.tl
2) Load the optimized IR (in binary form) and run it.
./kachua.py -b -r ./optimized.kw

3)Kachua can be run on the original program as well:
./kachua.py -r example/test.tl


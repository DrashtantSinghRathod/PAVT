# Program Analysis with Kachua

### Installing Dependencies

```bash
pip install antlr4-python3-runtime==4.7.2
pip install networkx
sudo apt-get install python3-tk 
```
### Running an example
The main directory for source files is `KachuaCore`.

  ```bash
  $ cd KachuaCore
  $ ./kachua.py -r ./example/test.tl
  ```

### See help for other command line options
```bash
$ ./kachua.py --help

Kachua v5.3
------------
usage: kachua.py [-h] [-p] [-r] [-O] [-b] [-z] [-t TIMEOUT] [-d PARAMS] [-c CONSTPARAMS] [-se] [-ai] [-sbfl]
                 [-bg BUGGY] [-vars INPUTVARSLIST] [-nt NTESTS] [-pop POPSIZE] [-cp CXPB] [-mp MUTPB] [-ng NGEN]
                 [-vb VERBOSE]
                 progfl

Program Analysis Framework for Turtle.

positional arguments:
  progfl

optional arguments:
  -h, --help            show this help message and exit
  -p, --ir              pretty printing
  -r, --run             execute program
  -O, --opt             optimize
  -b, --bin             load binary IR
  -z, --fuzz            Run fuzzer on a turtle program (seed values with '-d' or '--params' flag needed.)
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout Parameter for Analysis (in secs)
  -d PARAMS, --params PARAMS
                        pass variable values to kachua program in python dictionary format
  -c CONSTPARAMS, --constparams CONSTPARAMS
                        pass variable(for which you have to find values using circuit equivalence) values to kachua
                        program in python dictionary format
  -se, --symbolicExecution
                        Run Symbolic Execution on a turtle program (seed values with '-d' or '--params' flag needed)
                        to generate test cases along all possible paths.
  -ai, --abstractInterpretation
                        Run abstract interpretation
  -sbfl, --SBFL         Run Spectrum-basedFault localizer on turtle program
  -bg BUGGY, --buggy BUGGY
                        buggy turtle program path
  -vars INPUTVARSLIST, --inputVarsList INPUTVARSLIST
                        A list of input variables of given turtle program
  -nt NTESTS, --ntests NTESTS
                        number of tests to generate
  -pop POPSIZE, --popsize POPSIZE
                        population size for Genetic Algorithm.
  -cp CXPB, --cxpb CXPB
                        cross-over probability
  -mp MUTPB, --mutpb MUTPB
                        mutation probability
  -ng NGEN, --ngen NGEN
                        number of times Genetic Algorithm iterates
  -vb VERBOSE, --verbose VERBOSE
                        To display computation to Console
```

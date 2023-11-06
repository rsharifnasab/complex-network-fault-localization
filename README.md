# Fault localization with complex networkx

### What to do?
Analysis of correlation between centrality measures and fault locations. More info in `todo.pdf` (in Persian)

### What database?
The used database is `code4bench` project. More information is available in the MySQL directory.


### How to?
This project aims to use complex network techniques (centrality measures) to find program defects. At first, we collected some faulty codes with their test cases. Then we build different graphs, for example, PDG and test case coverage for each line of code. Then, we compare the correlation between a node being central and having faults in it.

### What tools?
I use various tools for the project, but the main ones are:
+ `angr` for binary analysis and extract DDG
+ `llvm` with `DG` project to extract CDG
+ `gcov` for measuring test case coverage of c/cpp codes
+ `networkx` for building and analyzing graphs
` code4bench` as dataset and `mysql` and  DBMS

### How to run?
To run, after running `setup.sh` in `mysql` and `DG` dir, run a MySQL instance on port 3306, and in the src folder, run `pipeline.sh`. That would gather hot questions from the database and then find faulty codes for each question. Then, run codes with question's test cases and measure each test case (rather failing or passing) coverage. Then, we build 3 types of graphs with three scripts.

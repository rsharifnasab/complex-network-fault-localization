# Fault localization with complex networkx

### What to do?
Analysis correlation between centrality measures and fault locations. more info in `todo.pdf` (persian)

### What database?
The used database is `code4bench` project. more information is available in mysql directory.


### How to?
This project aims to use complex network (centrality measures) to find program defects. At first we collect some faulty codes with their test cases. then we build different graph for example PDG and test case coverage for each line of code. then we compare correlation between a node being central and have fault in it.

### What tools?
I use various tools for the project but the main ones are:
+ `angr` for binary analysis and extract DDG
+ `llvm` with `DG` project to extract CDG
+ `gcov` for measure test case coverage of c/cpp codes
+ `networkx` for build and analysis graphs
` code4bench` as dataset and `mysql` and  DBMS

### How to run?
to run, after running `setup.sh` in `mysql` and `DG` dir, run a mysql instance on port 3306 and in the src folder, run `pipline.sh`. That would gather hot questions from database and then find some faulty codes for each question. then run codes with question's test cases and measure each test case (rather failing or passing) coverage. then we build 3 type of graphs with 3 scripts.

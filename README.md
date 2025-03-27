# OL-Grammar-Analyser

## How to use

1. Open a terminal in the root of the project ;
2. Run `make run` to start the compilation process and run the program ;
3. Put your grammar in a file inside the "input" folder ;
4. In the terminal, enter your file's name, and the delimiter you chose (by default, it's "`->`") ;
5. Your grammar will be parsed! The next steps will use its built-in structure to determine its properties (these are yet to come).

## Development steps

1. Build the classes to fully encode a grammar ;
2. Build a parser which takes a string or a file and builds the corresponding grammar ;
3. Build the analyser using TLA algorithms (maybe will need some built-in parsing table structure...?)
4. Write tests & verification.

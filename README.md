# Lexical analyser, Parser, AST to generate tokens for arithmatic expressions

Generates Tokens and represents in form of json
(shown in screenshot)

Arithmatic operations only on 8bit integers.

How to:
-------

put your Arithmatic expression in input.toy

python3 main.py

llc -filetype=obj output.ll

clang output.o -o output
(gcc works on ubuntu 16.04 but not in ubuntu 18.04)

Note: the idea of this project is to build a really simple parser and lexical analyser, so make sure all your code is easy to read (avoid too much code in 1 line).

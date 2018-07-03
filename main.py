from lexer import lex
from parser import Expression, TokenStack
from codegen import CodeGen
from llvmlite import ir

fname = "input.toy"
with open(fname) as f:
    text_input = f.read().strip('\n')
print(text_input)
codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf

tokens = lex(text_input)
#pg = Parser(module, builder)
parse = Expression(TokenStack(tokens), module, builder, printf).node.eval()
#print(codegen.builder.add)
#print(parse)


#codegen = CodeGen()
codegen.create_ir()
codegen.save_ir("output.ll")


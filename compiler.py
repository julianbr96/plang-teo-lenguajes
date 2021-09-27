from stages.lexing.lexer import Lexer
from stages.parsing.parser import Parser
from stages.coding.codegen import CodeGen

# Initialize code generator form LLVM
codegen = CodeGen()
module = codegen.module
builder = codegen.builder
outf = codegen.outf

print("-----First stage: get lexer and obtain tokens-----\n")
lexer = Lexer().get()
tokens = lexer.lex("main[1 * 3 + 2]")

input("Continue?")

print("-----Second stage: get parser and obtain Syntax tree-----\n")
pg = Parser(module, builder, outf)
parser = pg.get()
print(parser.parse(tokens))

input("Continue?")

print("-----Third stage: Create IR (internal representation) for LLVM-----\n")
codegen.create_ir()
codegen.save_ir("tac.llvm")

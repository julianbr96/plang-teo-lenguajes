from stages.lexing.lexer import Lexer
from stages.parsing.parser import Parser
from stages.coding.codegen import CodeGen
from pprint import pprint
import inquirer
from os import walk
from ctypes import CFUNCTYPE, c_int32
import warnings

warnings.filterwarnings("ignore")

print("----------Pre stage: Select file to compile/run----------\n")
file_names = next(walk("./jlang-sources"), (None, None, []))[2]
questions = [
    inquirer.List('file_name',
                  message="Select the file you want to compile: ",
                  choices=file_names
                  )
]

filename = inquirer.prompt(questions)["file_name"]

# Initialize code generator for LLVM
codegen = CodeGen()
module = codegen.module
builder = codegen.builder
engine = codegen.engine

# Open source code file
file = open(f"jlang-sources/{filename}", "r")
src = file.read()
print(f"\n\n----SOURCE CODE JLANG----\n\n{src}\n\n")

print("----------First stage: get lexer and obtain tokens----------\n")
lexer = Lexer().get()
tokens = lexer.lex(src)
print("Tokens obtained\n")

input("Continue?")

print("----------Second stage: get parser and obtain Syntax tree----------\n")
pg = Parser(module, builder)
parser = pg.get()
print(f"\n----SYNTAX TREE----\n")
pprint(parser.parse(tokens))
print(f"\n----SYMBOL TABLE----\n")
pprint(pg.symbol_table)
print("\n")
# print(f"\n\n----PRODUCTIONS----\n")
# pprint(pg.pg.__dict__['productions'])

input("Continue?")

print("----------Third stage: Create IR (internal representation) for LLVM----------\n")
generatedcode = codegen.create_ir()
print(f"\n\n----IR LLVM----\n\n{generatedcode}\n\n")
codegen.save_ir(f"./llvm-ir/{filename}.llvm")

input("Continue?")

print("----------Fourth stage: Compile and run (JIT) IR code----------\n")
pointer = engine.get_function_address("main")
callable_function = CFUNCTYPE(c_int32)(pointer)
print(f"\n\n----START PROGRAM----\n")
result = callable_function()
print(f"----END PROGRAM----\n")
print(f"\n----Returned value from program----")
print(result)
print("\nEND OF EXECUTION. EXITING...")

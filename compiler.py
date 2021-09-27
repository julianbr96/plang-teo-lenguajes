from stages.lexing.lexer import Lexer
from stages.parsing.parser import Parser

print("-----First stage: get lexer and obtain tokens-----\n")
lexer = Lexer().get()
tokens = lexer.lex("main[(1 * 3 + 2)]")

input("Continue?")

print("-----Second stage: get parser and obtain Syntax tree-----\n")
pg = Parser()
parser = pg.get()
print(parser.parse(tokens))

input("Continue?")

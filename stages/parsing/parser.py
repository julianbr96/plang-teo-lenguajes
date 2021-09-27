from rply import ParserGenerator
from .ast import Number, BinaryOp, Add, Sub, Mul, Div


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names, accepted by the parser.
            [
                "NUMBER",
                "OPEN_PAREN",
                "CLOSE_PAREN",
                "ADD",
                "RES",
                "MUL",
                "DIV",
                "LOG",
                "INPUT",
                "IF",
                "TRUE",
                "FALSE",
                "OPEN_BRACKET",
                "CLOSE_BRACKET",
                "MAIN"
            ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[("left", ["ADD", "RES"]), ("left", ["MUL", "DIV"])],
        )

    def parse(self):
        @self.pg.production('expression : MAIN OPEN_BRACKET expression CLOSE_BRACKET')
        def program(p):
            return print("Program: ", p[2].eval())

        @self.pg.production("expression : NUMBER")
        def expression_number(p):
            # p is a list of the pieces matched by the right hand side of the
            # rule
            return Number(int(p[0].getstr()))

        @self.pg.production("expression : OPEN_PAREN expression CLOSE_PAREN")
        def expression_parens(p):
            return p[1]

        @self.pg.production("expression : OPEN_BRACKET expression CLOSE_BRACKET")
        def expression_bracket(p):
            return p[1]

        @self.pg.production("expression : expression ADD expression")
        @self.pg.production("expression : expression RES expression")
        @self.pg.production("expression : expression MUL expression")
        @self.pg.production("expression : expression DIV expression")
        def expression_binop(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype() == "ADD":
                return Add(left, right)
            elif p[1].gettokentype() == "RES":
                return Sub(left, right)
            elif p[1].gettokentype() == "MUL":
                return Mul(left, right)
            elif p[1].gettokentype() == "DIV":
                return Div(left, right)
            else:
                raise AssertionError("Oops, this should not be possible!")

    def get(self):
        self.parse()
        return self.pg.build()

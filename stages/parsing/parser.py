from rply import ParserGenerator
from .ast import Assign, Number, Add, Statements, Sub, Mul, Div, Variable, Whether_not, Predicate, Declaration, Iterator, End


class Parser():
    def __init__(self, module, builder):
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
                "OPEN_BRACKET",
                "CLOSE_BRACKET",
                "MAIN",
                "ITERATE",
                "AS_LONG_AS",
                "LOWEREQ",
                "GREATEREQ",
                "EQUAL",
                "NEQUAL",
                "LOWER",
                "GREATER",
                "VAR",
                "VARIABLE",
                "ASSIGN",
                "WHETHER",
                "OR_NOT",
                "END"
            ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[("right", ["ADD", "RES"]), ("right", ["MUL"])],
        )
        self.module = module
        self.builder = builder
        self.symbol_table = {}

    def parse(self):
        @self.pg.production('main-program : MAIN OPEN_BRACKET statements end CLOSE_BRACKET')
        def program(p):
            p[2].eval()
            p[3].eval()

        @self.pg.production('code-block : OPEN_BRACKET statements CLOSE_BRACKET')
        def block(p):
            return p[1]

        @self.pg.production('statements : ')
        def empty_expression(p):
            return Statements()

        @self.pg.production('statements : statements expression')
        @self.pg.production('statements : statements initialization')
        @self.pg.production('statements : statements assignment')
        @self.pg.production('statements : statements iterator')
        @self.pg.production('statements : statements end')
        def statements(p):
            p[0].append(p[1])
            return p[0]

        @self.pg.production('expression : WHETHER predicate code-block OR_NOT code-block')
        def conditional(p):
            return Whether_not(self.builder, self.module, p[1], p[2], p[4])

        @self.pg.production('predicate : expression predicate-op expression')
        def predicate(p):
            return Predicate(self.builder, self.module, p[1], p[0], p[2])

        @self.pg.production('predicate-op : LOWEREQ')
        @self.pg.production('predicate-op : GREATEREQ')
        @self.pg.production('predicate-op : GREATER')
        @self.pg.production('predicate-op : EQUAL')
        @self.pg.production('predicate-op : NEQUAL')
        @self.pg.production('predicate-op : LOWER')
        def pred_op(p):
            return p[0].value

        @self.pg.production('initialization : VAR VARIABLE expression')
        def declare(p):
            return Declaration(self.builder, self.module, p[1], p[2], self.symbol_table)

        @self.pg.production('expression : predicate')
        def expression_cond(p):
            return p[0]

        @self.pg.production("expression : NUMBER")
        def expression_number(p):
            return Number(int(p[0].value))

        @self.pg.production("expression : OPEN_PAREN expression CLOSE_PAREN")
        def expression_parens(p):
            return p[1]

        @self.pg.production('expression : VARIABLE')
        @self.pg.production('var : VARIABLE')
        def var(p):
            return Variable(self.builder, self.module, p[0], self.symbol_table)

        @self.pg.production("expression : expression ADD expression")
        @self.pg.production("expression : expression RES expression")
        @self.pg.production("expression : expression MUL expression")
        @self.pg.production("expression : expression DIV expression")
        def expression_binop(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype() == "ADD":
                return Add(self.builder, self.module, left, right)
            elif p[1].gettokentype() == "RES":
                return Sub(self.builder, self.module, left, right)
            elif p[1].gettokentype() == "MUL":
                return Mul(self.builder, self.module, left, right)
            elif p[1].gettokentype() == "DIV":
                return Div(self.builder, self.module, left, right)
            else:
                raise AssertionError(
                    f"The operator '{p[1].gettokentype()}' in line: {p[1].source_pos} is not valid")

        @self.pg.production('iterator : ITERATE code-block AS_LONG_AS predicate')
        def iterator(p):
            return Iterator(self.builder, self.module, p[3], p[1])

        @self.pg.production('assignment : var ASSIGN expression')
        def assignment(p):
            return Assign(self.builder, self.module, p[0], p[2], self.symbol_table)

        @self.pg.production('end : END expression')
        def ret(p):
            return End(self.builder, self.module, p[1])

        @self.pg.error
        def error_handler(token):
            raise Exception(
                f"Ran into a {token.gettokentype()} where it was't expected \n{token.source_pos}")

    def get(self):
        self.parse()
        return self.pg.build()

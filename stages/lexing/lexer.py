from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _set_tokens(self):
        # Log
        self.lexer.add("LOG", r"log")

        # Main
        self.lexer.add("MAIN", r"main")

        # Read input
        self.lexer.add("INPUT", r"input")

        # Parenthesis
        self.lexer.add("OPEN_PAREN", r"\(")
        self.lexer.add("CLOSE_PAREN", r"\)")

        # Brackets
        self.lexer.add("OPEN_BRACKET", r"\[")
        self.lexer.add("CLOSE_BRACKET", r"\]")

        # Binary Operators
        self.lexer.add("ADD", r"\+")
        self.lexer.add("RES", r"\-")
        self.lexer.add("MUL", r"\*")
        self.lexer.add("DIV", r"\/")

        # Number
        self.lexer.add("NUMBER", r"\d+")

        # Conditional
        self.lexer.add('WHETHER', r"whether")
        self.lexer.add('OR_NOT', r"or not")

        # Functions
        self.lexer.add('ITERATE', r"iterate")
        self.lexer.add('UNTIL', r"until")
        self.lexer.add("GIVEBACK", r"giveback")

        # Conditional Operators
        self.lexer.add('LOWEREQ', r'<=')
        self.lexer.add('GREATEREQ', r'>=')
        self.lexer.add('EQUAL', r'==')
        self.lexer.add('NEQUAL', r'!=')
        self.lexer.add('LOWER', r'<')
        self.lexer.add('GREATER', r'>')

        # Vars
        self.lexer.add("VAR", r"var")
        self.lexer.add("VARIABLE", r"[a-zA-Z_][a-zA-Z0-9_]*")
        self.lexer.add("ASSIGN", r":=")

        # Ignore
        self.lexer.ignore(r" ")  # ignore spaces
        self.lexer.ignore(r"\n")  # ignore newline
        self.lexer.ignore(r"{{.*")  # comments

    def get(self):
        self._set_tokens()
        return self.lexer.build()

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

        # Conditional
        self.lexer.add("IF", r"if")

        # Booleans
        self.lexer.add("TRUE", r"true")
        self.lexer.add("FALSE", r"false")

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

        # Ignore
        self.lexer.ignore(r" ")  # ignore spaces
        self.lexer.ignore(r"\\n")  # ignore newline
        self.lexer.ignore(r"{{(.*)")  # comments

    def get(self):
        self._set_tokens()
        return self.lexer.build()

from antlr4 import *

from sid.languages.base.LanguageCleaner import LanguageCleaner
from sid.languages.python3.Python3Lexer import Python3Lexer
from sid.languages.python3.Python3Parser import Python3Parser
from sid.languages.python3.Walker import SIDPython3Walker


class Python3Cleaner(LanguageCleaner):
    def __init__(self):
        super().__init__()
        self.name = "python3"


    def clean(self, file):
        input = FileStream(file)
        lexer = Python3Lexer(input)
        stream = CommonTokenStream(lexer)
        parser = Python3Parser(stream)

        tree = parser.file_input()
        listener = SIDPython3Walker()

        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.str_symbols(), listener.tokens

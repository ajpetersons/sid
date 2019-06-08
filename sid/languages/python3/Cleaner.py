from antlr4 import *

from sid.languages.base.LanguageCleaner import LanguageCleaner
from sid.languages.python3.Python3Lexer import Python3Lexer
from sid.languages.python3.Python3Parser import Python3Parser
from sid.languages.python3.Walker import SIDPython3Walker


class Python3Cleaner(LanguageCleaner):
    """Class facilitates Python 3 language cleaner. This is a useful, reusable 
        wrapper around ANTLR commands needed to parse a program and to turn it 
        into tokens as expected by similarity detector.
    """

    def __init__(self):
        """Method initializes a new instance of Python 3 language cleaner
        """
        super().__init__()
        self.name = "python3"


    def clean(self, file):
        """Method takes an input file name, reads this file an parses it with 
            ANTLR. This method wraps basic ANTLR actions that would be necessary 
            in order to simplify language processing.
        
        :param file: Path to the file, which contains code to be processed
        :type file: str
        :return: Sequence of processed file contents by obfuscating code in a 
            way to reveal only the underlying structure. Also returns locations 
            of the characters in the original files as a list
        :rtype: tuple of str and list of dict
        """
        contents = FileStream(file)
        lexer = Python3Lexer(contents)
        stream = CommonTokenStream(lexer)
        parser = Python3Parser(stream)

        tree = parser.file_input()
        listener = SIDPython3Walker()

        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.str_symbols(), listener.tokens

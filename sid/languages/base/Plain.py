from sid.languages.base.LanguageCleaner import LanguageCleaner


class Plain(LanguageCleaner):
    """Class facilitates vase language cleaner. This class is intended to be 
        extended by language specific cleaners facilitating ANTLR or other 
        language processor commands. This class implements a basic cleaner which 
        outputs 1:1 input string as well as token indices.
    """

    def __init__(self):
        """Method initializes a new instance of language cleaner.
        """
        self.name = "identity"


    def clean(self, file):
        """Method takes an input file name, reads this file and outputs the saem
            string with associated indices for tokens.
        
        :param file: Path to the file, which contains code to be processed
        :type file: str
        :return: Sequence of processed file contents by obfuscating code in a 
            way to reveal only the underlying structure. Also returns locations 
            of the characters in the original files as a list
        :rtype: tuple of str and list of dict
        """
        token_locations = []

        f = open(file, "r")
        for line_idx, line in enumerate(f):
            for char_idx, char in enumerate(line):
                token_locations.append({
                    'line': line_idx + 1, 
                    'col': char_idx
                })

        f.seek(0)
        return f.read(), token_locations

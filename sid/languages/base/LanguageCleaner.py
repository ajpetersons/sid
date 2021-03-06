class LanguageCleaner(object):
    """Class facilitates vase language cleaner. This class is intended to be 
        extended by language specific cleaners facilitating ANTLR or other 
        language processor commands. This class implements a basic cleaner which 
        outputs 1:1 input string as well as token indices.
    """

    def __init__(self):
        """Method initializes a new instance of language cleaner.
        """
        self.name = None


    def clean(self, file):
        """Method takes an input file name, reads this file and outputs cleaned
            string with associated indices for tokens. All instances of 
            LanguageCleaner should implement this method, as SID will call this 
            to parse input source.
        
        :param file: Path to the file, which contains code to be processed
        :type file: str
        :return: Sequence of processed file contents by obfuscating code in a 
            way to reveal only the underlying structure. Also returns locations 
            of the characters in the original files as a list
        :rtype: tuple of str and list of dict
        """
        raise NotImplementedError

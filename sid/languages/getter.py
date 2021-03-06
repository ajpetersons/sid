from sid.languages.base.Plain import Plain
from sid.languages.python3.Cleaner import Python3Cleaner
from sid.languages.matlab.Cleaner import MatlabCleaner
from sid.languages.errors import UnknownLanguageError


languages = {
    "plain": Plain,
    "python3": Python3Cleaner,
    "matlab": MatlabCleaner
}


def available_languages():
    """Function lists all languages supported by SID.
    
    :return: List of supported languages
    :rtype: list of str
    """
    return languages.keys()


def get_language_parser(name):
    """Function retrieves an uninitialized parser for each language. Each parser 
        should extend LanguageCleaner class. If text needs to be mapped 1:1 from 
        parser, with indices computed, LanguageCleaner itself has base 
        implementation that can provide such functionality without knowing 
        anything about source code syntax.
    
    :param name: Name of the language to use
    :type name: str
    :raises UnknownLanguageError: Exception is raised when an unknown language 
        is passed to function, letting user know that this language is not 
        supported
    :return: Class instance of language type initialized for processing
    :rtype: function
    """

    if name in languages:
        return languages[name]

    raise UnknownLanguageError

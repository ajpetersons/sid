from sid.languages.javascript.processor import clean as js_clean
from sid.languages.base.LanguageCleaner import LanguageCleaner
from sid.languages.python3.cleaner import Python3Cleaner


def get_language_parser(name):
    """TODO:
    
    :param name: Name of the language to use
    :type name: str
    :return: Class instance of language type initialized for processing
    :rtype: function
    """
    
    languages = {
        # FIXME: refactor for correct indices
        "none": LanguageCleaner
    }

    if name in languages:
        return languages[name]

    return languages["none"]

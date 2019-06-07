from sid.languages.base.LanguageCleaner import LanguageCleaner
from sid.languages.python3.Cleaner import Python3Cleaner
# from sid.languages.matlab.Cleaner import MatlabCleaner


def get_language_parser(name):
    """TODO:
    
    :param name: Name of the language to use
    :type name: str
    :return: Class instance of language type initialized for processing
    :rtype: function
    """
    
    languages = {
        # FIXME: refactor for correct indices
        "none": LanguageCleaner,
        "python3": Python3Cleaner,
        # "matlab": MatlabCleaner
    }

    if name in languages:
        return languages[name]

    return languages["none"]

class UnknownLanguageError(Exception):
    def __init__(self, message=None):
        self.message = message


    def __str__(self):
        if self.message is not None:
            return self.message

        return "The provided programming language is not recognized"

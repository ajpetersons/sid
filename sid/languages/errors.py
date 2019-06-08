class SimpleError(Exception):
    """SimpleError class wraps basic functionality for custom errors. Custom 
        errors used in SID should have a default message, which can be overriden 
        by user provided message during initialization.
    """
    
    def __init__(self, message=None):
        """Method initializes SimpleError class instance, by setting override 
            message (if there is such) and a default message to be used when 
            nothing is known about the error.
        
        :param message: Message to display to user upon presenting this error, 
            defaults to None
        :type message: str, optional
        """
        self.message = message
        self.default_message = "Unknown error has occurred"


    def __str__(self):
        """Method builds a string representation of error, by returning the 
            custom message if such is set. Otherwise, the default message for 
            this error type is returned.
        
        :return: Human readable explanation of the semantics of this error
        :rtype: str
        """
        if self.message is not None:
            return self.message

        return self.default_message


class UnknownLanguageError(SimpleError):
    """Class defines an error when user attempts to run language parser on a 
        language that is not recognized as a valid language. This can happen due 
        to a mistake in language name or by trying to parse a language that 
        doesn't have grammar implemented.
    """

    def __init__(self, message=None):
        """Method initializes UnknownLanguageError class instance, by setting  
            overriden message (if there is such) and a default message to be 
            used when nothing is known about the error.
        
        :param message: Message to display to user upon presenting this error, 
            defaults to None
        :type message: str, optional
        """
        super().__init__(message=message)

        self.default_message = "The provided programming language is not recognized"


class UnknownSymbolError(SimpleError):
    """Class defines an error when a token is passed to processor, and the 
        processor does not recognize this symbol as one from the token set used 
        in representing the language.
    """

    def __init__(self, message=None):
        """Method initializes UnknownLanguageError class instance, by setting  
            overriden message (if there is such) and a default message to be 
            used when nothing is known about the error.
        
        :param message: Message to display to user upon presenting this error, 
            defaults to None
        :type message: str, optional
        """
        super().__init__(message=message)

        self.default_message = "The provided symbol is not recognized"

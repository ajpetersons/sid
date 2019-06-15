import logging

class Context(object):
    """Context is global variables for command invocation. Context is passed 
        from top command to its childs if @click.pass_context decorator is 
        present.
    """

    logFormat = '%(asctime)s\t[%(levelname)s]\t%(message)s'


    def __init__(self):
        """Method sets up a new context instance. This method initializes 
            default logging to write only 'WARN' or higher level messages. 
            Logging verbosity can be increased by one or two levels by passing 
            the verbosity flag and invoking setupLogging method.
        """
        self.verbosity = 0
        self.logging = False
        logging.basicConfig(format=self.logFormat, level='WARN')


    def setupLogging(self, verbosity):
        """Method sets up logging for the whole application. By default logging 
            is set to write only 'WARN' or higher level messages. Logging 
            verbosity can be increased by one or two levels by passing the 
            verbosity flag. Once verbosity flag is met, it is passed down to 
            further commands and any attempts to overwrite it will be 
            ineffective as this method will return without doing anything.

        :param verbosity: Updated logging verbosity
        :type verbosity: int
        """
        if self.logging:
            # Higher level command initialized logging, skip this function
            return
        
        self.logging = True
        self.verbosity = verbosity

        levels = {
            0: 'WARN',
            1: 'INFO',
            2: 'DEBUG'
        }

        level = levels[self.verbosity] if self.verbosity in levels else 'DEBUG'
        logging.basicConfig(format=self.logFormat, level=level)

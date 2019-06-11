import click

from sid.cmd.context import Context


def verbose(f):
    """Function defines a decorator that can be used for enabling more verbose 
        logging. The function adds a flag to command that can be used multiple 
        times to increase logging level, function then sets up logging instance 
        on command context.
    
    :param f: Command instance to apply decorator to
    :type f: click.Command
    :return: Command instance with decorator applied
    :rtype: click.Command
    """
    
    def callback(ctx, param, value):
        """Function defines actions to be performed on option value. In this 
            case logging verbosity is set and logging format reloaded.
        
        :param ctx: Command context that is passed around
        :type ctx: click.Context
        :param param: The option that has been associated with this decorator
        :type param: click.Option
        :param value: Value received from user input to this decorator - logging 
            verbosity
        :type value: int
        :return: Value received from user input to this decorator - logging 
            verbosity
        :rtype: int
        """
        c = ctx.ensure_object(Context)
        c.setupLogging(value)
        return value

    return click.option('-v', count=True, expose_value=False,
                        help='Enable verbose output', callback=callback)(f)

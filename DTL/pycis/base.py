from functools import partial
from DTL.api import Utils

from DTL.pycis.core import pyCis

class pyCisCommandError(Exception):
    """
    Exception class indicating a problem while executing a management
    command.

    If this exception is raised during the execution of a management
    command, it will be caught and turned into a nicely-printed error
    message to the appropriate output stream (i.e., stderr); as a
    result, raising this exception (with a sensible description of the
    error) is the preferred way to indicate that something has gone
    wrong in the execution of a command.

    """
    pass

class pyCisCommand(object):
    '''The base class form which all pycis commands ultimately derive'''
    
    def __init__(self):
        Utils.synthesize(self, "helpFlag", True)
        Utils.synthesize(self, "args", '')
        Utils.synthesize(self, "parentParser", '')
        Utils.synthesize(self, "parser", '')
    
    def usage(self, subcommand):
        """
        Return a brief description of how to use this command, by
        default from the attribute ``self.help``.
        """
        usage = '%%prog %s [options] %s' % (subcommand, self.args())
        if self.help:
            return '%s\n%s' % (usage, self.__doc__)
        else:
            return usage
    
    def print_help(self):
        """
        Print the help message for this command, derived from
        ``self.usage()``.

        """
        self.parser().print_help()
        
    def setupParser(self, parser):
        self.setParser(parser)
        self.handleParser(parser)
        
    def handleParser(self, parser):
        parser.set_defaults(func=partial(self.execute))
    
    def execute(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.

        """
        raise NotImplementedError()

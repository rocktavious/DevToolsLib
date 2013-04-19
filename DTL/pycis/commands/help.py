import sys
from functools import partial

from DTL.pycis.core import pyCis
from DTL.pycis.base import pyCisCommand, pyCisCommandError

#------------------------------------------------------------
class Command(pyCisCommand):
    '''This is the overall help function'''
    def __init__(self):
        super(Command, self).__init__()
        self.setHelpFlag(False)
    
    def handleParser(self, parser):
        parser.add_argument('command', help='Prints the help information for the command give')
        parser.set_defaults(func=partial(self.execute))    
        
    def execute(self, *args, **options):
        if args[0].command :
            pyCis().print_command_help(args[0].command)
        else:
            pyCis().print_help()
import sys
from functools import partial

from ..core import pyCis
from ..base import pyCisCommand, pyCisCommandError

#------------------------------------------------------------
class Command(pyCisCommand):
    '''This is the overall help function'''
    def handleParser(self, parser):
        parser.add_argument('-c', '--command', help='Prints the help information for the command give')
        parser.set_defaults(func=partial(self.execute))    
        
    def execute(self, *args, **options):
        if args[0].command :
            pyCis.instance().print_command_help(args[0].command)
        else:
            pyCis.instance().print_help()
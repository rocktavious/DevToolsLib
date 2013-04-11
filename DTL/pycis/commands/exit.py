import sys

from ..base import pyCisCommand, pyCisCommandError

#------------------------------------------------------------
class Command(pyCisCommand):
    '''Quits pyCis'''
    
    def execute(self, *args, **options):
        sys.exit(0)
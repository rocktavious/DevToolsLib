import sys

from DTL.pycis.core import pyCis
from DTL.pycis.base import pyCisCommand, pyCisCommandError

#------------------------------------------------------------
class Command(pyCisCommand):
    '''Quits pyCis'''
    
    def execute(self, *args, **options):
        sys.exit(0)
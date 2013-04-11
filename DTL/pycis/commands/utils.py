import sys

from . import command, alias

#------------------------------------------------------------
@command
@alias('about')
def help(pycis, *args):
    '''Help Command'''
    def _setupParser(parser):
        parser.add_argument('-x', type=int, default=1)
        parser.add_argument('y', type=float)        
        
    pycis.parser().print_help()
    
#------------------------------------------------------------
@command
@alias('about')
class read(object):
    '''Help Command'''
    def _setupParser(parser):
        parser.add_argument('-x', type=int, default=1)
        parser.add_argument('y', type=float)        
    
    def run(pycis, *args):
        pycis.parser().print_help()

#------------------------------------------------------------
@command
@alias('quit')
def exit(pycis, *args):
    '''Exit Command'''
    sys.exit(0)
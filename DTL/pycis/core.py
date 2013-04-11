import sys
import logging
from functools import partial
from argparse import ArgumentParser

from DTL.api import Logger, Utils

from commands import *


class pycisArgumentParser(ArgumentParser):
    """ArgumentParser that doesn't exit on error"""
    class ArgParseError(Exception):
        pass

    def parse_args(self, args=None, namespace=None):
        if not args: return None
        try: return ArgumentParser.parse_args(self, args, namespace)
        except self.__class__.ArgParseError : return None

    def exit(self, status=0, message=None):
        """Override exit function to prevent exiting the program"""
        if message:
            self._print_message(message, sys.stderr)
        raise self.__class__.ArgParseError()

class pyCis(object):
    '''pyCis - Python Console Intelligence System'''
    __metaclass__ = Logger.getMetaClass()   
    
    #------------------------------------------------------------
    def __init__(self):  
        Utils.synthesize(self, 'parser', None)
        
        self._setupLogging()
        self._setupParser()
        self._setupCommands()
        
        self._mainloop()
    
    #------------------------------------------------------------
    def _setupLogging(self):
        Logger.setupStreamLogger(formatter=logging.Formatter('\t%(message)s'))
    
    #------------------------------------------------------------
    def _setupParser(self):
        main_parser = pycisArgumentParser(prog='', add_help=False)
        self.setParser(main_parser)
    
    #------------------------------------------------------------
    def _setupCommands(self):
        subparsers = self.parser().add_subparsers()
        for name, func in commands.items():
            parser = subparsers.add_parser(name, help=func.__doc__)
            if hasattr(func, '_setupParser'):
                func._setupParser(parser)            
            parser.set_defaults(func=partial(func, self))
        for name, func in aliases.items():        
            parser = subparsers.add_parser(name, help=func.__doc__)
            if hasattr(func, '_setupParser'):
                func._setupParser(parser)                
            parser.set_defaults(func=partial(func, self))
    
    #------------------------------------------------------------
    def _mainloop(self):
        while True:
            line = raw_input('pyCis >> ')
            args = self.parser().parse_args(line.split())
            if args:
                args.func(args)

if __name__ == '__main__':
    pyCis()
import sys
from DTL.api import apiUtils

class App(object):
    def __init__(self, *args, **kwds):
        pass
    
    def run(self):
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv[0], 'collectstatic')
        
        execute_from_command_line(sys.argv[0], 'runserver')
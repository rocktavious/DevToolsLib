"""
Custom Json document class

Description
=============
    Contains both the dictionary of data and the filepath for ease of saving, reading and accessing

Usage Example
=============
    >>> json_store = JsonDocument('c:/temp/test.json')
    >>> print json_store['Json Data Item']

"""

import os.path
import json

from . import Path

#------------------------------------------------------------
#------------------------------------------------------------
class JsonDocument(dict):
    '''Custom Dictionary class that has an associated json file for easy saving/reading'''
    #------------------------------------------------------------
    def __init__(self, file_path=None):
        super(JsonDocument, self).__init__()
        self.setFilePath(file_path)
        self._encoder = None
        self.read()
    
    #------------------------------------------------------------
    def setFilePath(self, file_path):
        if isinstance(file_path, Path):
            self._file = file_path
        else :
            self._file = Path(file_path)
            
    #------------------------------------------------------------
    def setEncoder(self, encoder):
        self._encoder = encoder
    
    #------------------------------------------------------------
    def save(self):
        '''Writes the dict data to the json file'''
        with open(self._file.path,'wb') as json_file :
            json_data = json.dumps(self, sort_keys=True, indent=4, cls=self._encoder)
            json_file.write(json_data)
            #print "Saving...", self._file.path
    
    #------------------------------------------------------------
    def read(self):
        '''Reads from a json file the dictionary data'''
        if not self._file.exists :
            return
        with open(self._file.path,'r') as json_file :
            data = json.load(json_file)
        for key, value in data.items():
            self.__setitem__(key, value)
                
    #------------------------------------------------------------
    def defaults(self, defaults={}):
        '''Allows the user to specify default values that should appear in the data'''
        for key, value in defaults.items():
            if not self.has_key(key):
                self.__setitem__(key, value)


import os.path
import json

from DTL.api.path import Path
from DTL.api.document import Document
from DTL.api import utils as Utils

#------------------------------------------------------------
#------------------------------------------------------------
class JsonDocument(Document):
    '''Custom Dictionary class that has an associated json file for easy saving/reading'''
    #------------------------------------------------------------
    def __init__(self, *args, **kwds):
        super(JsonDocument, self).__init__(*args, **kwds)
        Utils.synthesize(self, 'encoder', None)
    
    #------------------------------------------------------------
    def _unparse(self, data_dict):
        return json.dumps(data_dict, sort_keys=True, indent=4, cls=self.encoder())
    
    #------------------------------------------------------------
    def _parse(self, file_handle):
        '''Reads from a json file the dictionary data'''
        return json.load(file_handle)


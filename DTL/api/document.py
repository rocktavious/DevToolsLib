from DTL.api.bases import BaseStruct
from DTL.api.path import Path
from DTL.api import apiUtils

#------------------------------------------------------------
#------------------------------------------------------------
class Document(BaseStruct, dict):
    '''Custom Dictionary class that has an associated file for easy saving/reading/printing'''
    #------------------------------------------------------------
    def __init__(self, data_dict={}, file_path=None):
        super(Document, self).__init__()
        apiUtils.synthesize(self, 'filePath', Path())
        if file_path :
            self.setFilePath(file_path=file_path)
        self.read()
        self._set_data(data_dict=data_dict)

    #------------------------------------------------------------
    def setFilePath(self, file_path):
        self._filePath = Path(file_path)
            
    #------------------------------------------------------------
    def serialize(self):
        return (dict(self),)

    #------------------------------------------------------------
    def save(self):
        '''Writes the dict data to the xml file'''
        data_dict = self._unparse(self)
        if self.filePath() != '' :
            with open(self.filePath(),'wb') as file_handle :
                file_handle.write(data_dict)
    
    #------------------------------------------------------------
    def read(self):
        '''Reads file and stores the data in self as a dictionary'''
        if not self.filePath().exists() :
            return
        with open(self.filePath(),'r') as file_handle :
            data_dict = self._parse(file_handle)
        self._set_data(data_dict)
        
    #------------------------------------------------------------
    def setdefault(self, default={}):
        '''Allows the user to specify default values that should appear in the data'''
        for key, value in default.items():
            if not self.has_key(key):
                self.__setitem__(key, value)
            
    #------------------------------------------------------------
    def _set_data(self, data_dict):
        for key, value in data_dict.items():
            self.__setitem__(key, value)
            
    #------------------------------------------------------------
    def _parse(self, data_stream):
        return data_stream
    
    #------------------------------------------------------------
    def _unparse(self, data_dict):
        return data_dict
    

if __name__ == '__main__':
    new_doc = Document({'Testing':'min'})
    new_doc.setFilePath('/testing/file/path')
    new_doc2 = Document({'next doc':new_doc})
    print new_doc
    print 'Filepath = "{0}"'.format(new_doc.filePath())
    print [new_doc, new_doc2] == eval(str([new_doc, new_doc2]))
    print new_doc2['next doc'].filePath()

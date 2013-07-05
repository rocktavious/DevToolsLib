from DTL.api.core import BaseStruct, Enum, apiUtils

VersionStatus = Enum('Alpha','Beta','Gold')

class Version(BaseStruct):
    #------------------------------------------------------------
    def __init__(self, attitude=None):
        apiUtils.synthesize(self, 'major', 1)
        apiUtils.synthesize(self, 'minor', 0)
        apiUtils.synthesize(self, 'fix', 0)
        apiUtils.synthesize(self, 'status', 0)
        
        self.__set(attitude)
    
    #------------------------------------------------------------
    def __get(self):
        return {"major":self._major,
                "minor":self._minor,
                "fix":self._fix,
                "status":self._status}        
    
    #------------------------------------------------------------
    def __set(self, value):
        if isinstance(value, str):
            if len(value.split('.')) == 4:
                value = value.split('.')
        
        if isinstance(value, tuple) or isinstance(value, list) :
            if len(value) == 4:
                value = {'major':value[0],
                         'minor':value[1],
                         'fix':value[2],
                         'status':value[3]}
                
        if isinstance(value, Version):
            value = value.get()
        
        if isinstance(value, dict) :
            self._major = value.get('major',self._major)
            self._minor = value.get('minor',self._minor)
            self._fix = value.get('fix',self._fix)
            
            enum_value = value.get('status',self._status)
            if isinstance(enum_value, str):
                self._status = VersionStatus.names.index(enum_value)
            else:
                self._status = VersionStatus.names.index(VersionStatus.names[enum_value])


if __name__ == '__main__':
    version = Version()
    print version
    version2 = Version()
    version.set((2,0,5,'Beta'))
    print version
    version2.set(version)
    version2.set({'status':VersionStatus.Gold})
    print version2
    print version == version2
    print Version({'status': 0, 'major': 1, 'fix': 0, 'minor': 0})
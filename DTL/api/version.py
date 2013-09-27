from DTL.api import BaseDict, Enum, apiUtils

VersionStatus = Enum('Alpha','Beta','Gold')

class Version(BaseDict):
    def __init__(self, *args, **kwds):
        self.__setitem__('major',0)
        self.__setitem__('minor',0)
        self.__setitem__('fix',0)
        self.__setitem__('status',VersionStatus.Alpha)
        
        super(Version, self).__init__(*args, **kwds)
    
    def serialize(self):
        return (dict(self),)
        
    def deserialize(self, version=None):       
        if isinstance(version, str):
            if len(version.split('.')) == 4:
                version = version.split('.')
        
        if isinstance(version, tuple) or isinstance(version, list) :
            if len(version) == 4:
                version = {'major':version[0],
                           'minor':version[1],
                           'fix':version[2],
                           'status':version[3]}
                
        if isinstance(version, Version):
            version = version
        
        if isinstance(version, dict) :
            self.__setitem__('major', int(version.get('major',self['major'])))
            self.__setitem__('minor', int(version.get('minor',self['minor'])))
            self.__setitem__('fix', int(version.get('fix',self['fix'])))
            
            enum_value = version.get('status',self['status'])
            if isinstance(enum_value, str):
                self.__setitem__('status', VersionStatus.names.index(enum_value))
            else:
                self.__setitem__('status', VersionStatus.names.index(VersionStatus.names[enum_value]))
        
    def update(self, other):
        self.deserialize(other)

"""
Version class

Usage Example
=============
    >>> version = Version()
    >>> print version
    Version( 1.0.0 - Alpha )
    >>> version2 = Version()
    >>> version.set((2,0,5,'Beta'))
    >>> print version
    Version( 2.0.5 - Beta )
    >>> version2.set(version)
    >>> version2.set({'status':Status.Gold})
    >>> print version2
    Version( 2.0.5 - Gold )
    >>> print version == version2
    False
    
"""
from . import Enum

Status = Enum('Alpha','Beta','Gold')

class Version(object):
    #------------------------------------------------------------
    def __init__(self, attitude):
        self._major = 1
        self._minor = 0
        self._fix = 0
        self._status = 0   
        self.set(attitude)
    
    #------------------------------------------------------------
    def __eq__(self, other):
        if not isinstance(other, Version) :
            return False
        if not self._major == other._major :
            return False
        if not self._minor == other._minor :
            return False
        if not self._fix == other._fix :
            return False
        if not self._status == other._status :
            return False
        
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
    
    #------------------------------------------------------------
    def __repr__(self):
        return 'Version( %i.%i.%i - %s )' % (self._major, self._minor, self._fix, Status.names[self._status]) 

    #------------------------------------------------------------
    def __str__(self):
        return self.__repr__()
    
    #------------------------------------------------------------
    def get(self):
        return {"major":self._major,
                "minor":self._minor,
                "fix":self._fix,
                "status":self._status}        
    
    #------------------------------------------------------------
    def set(self, value):
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
                self._status = Status.names.index(enum_value)
            else:
                self._status = Status.names.index(Status.names[enum_value])


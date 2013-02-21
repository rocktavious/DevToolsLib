"""
Path helper classes

Usage Example
=============
    >>> myPath = Path('c:/dev_tools')
    >>> myPath2 = Path(myPath)
    >>> myPath.join('dtl','__init__.py')
    >>> print myPath
    Path( "c:\dev_tools\dtl\__init__.py" )
    >>> print myPath.case_sensative_path
    C:\dev_tools\DTL\__init__.py
    >>> print myPath.branch_relative_path
    \dtl\__init__.py
    >>> print myPath.file
    __init__.py
    >>> print myPath.ext
    .py
    >>> print myPath == myPath2
    False

"""

import os

#------------------------------------------------------------
#------------------------------------------------------------
class Path(object):
    _branch = None
    #------------------------------------------------------------
    def __init__(self, path=None):
        if isinstance(path, Path):
            path = path.path
        self._set_path(path)
        
    #------------------------------------------------------------
    def _get_path(self):
        return self._path
    
    #------------------------------------------------------------
    def _set_path(self, path):
        if path is not None:
            normPath = os.path.normpath(os.path.abspath(path))
            self._path = normPath.lower()
        else:
            self._path = None
        
        
    path = property(_get_path, _set_path)
        
    #------------------------------------------------------------
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.path == other.path
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash(self.path)
    def __repr__(self):
        return 'Path( "%s" )' % self.path
    def __str__(self):
        return self.__repr__()
    
    #------------------------------------------------------------
    def join(self, *a):
        new_path = os.path.join(self.path, *a)
        self._set_path(new_path)
    
    #------------------------------------------------------------
    def new_path_join(self, *a):
        new_path = os.path.join(self.path, *a)
        return Path(new_path)
    
    #------------------------------------------------------------
    def validate_dirs(self):
        import errno
        try:
            os.makedirs(self.dir)
        except os.error as e:
            if e.errno != errno.EEXIST:
                raise
    
    #------------------------------------------------------------
    @property
    def case_sensative_path(self):
        return Path.get_case_sensative_path(self.path)
    
    #------------------------------------------------------------
    @property
    def branch_relative_path(self):
        return Path.get_branch_relative_path(self.path)
    
    #------------------------------------------------------------
    @property
    def isFile(self):
        return os.path.isfile(self._path)
    
    #------------------------------------------------------------
    @property
    def file(self):
        if self.isFile :
            return os.path.split(self._path)[1]
        else:
            return None
    
    #------------------------------------------------------------
    @property
    def dir(self):
        if os.path.isdir(self._path):
            return self._path
        else:
            return os.path.dirname(self._path)
        
    #------------------------------------------------------------
    @property
    def ext(self):
        if self.isFile :
            return os.path.splitext(self._path)[1]
        else:
            return None
    
    #------------------------------------------------------------
    @staticmethod
    def branch():
        '''Returns the directory of the Project Root for use in branch relative paths'''
        if Path._branch is None :
            path = os.path.abspath(__file__)
            while 1:
                path, tail = os.path.split(path)
                if (os.path.isfile(os.path.join(path,"ProjectRoot"))):
                    break
                if (len(tail)==0):
                    path = ""
                    break
            Path._branch = path
        
        return Path._branch
    
    #------------------------------------------------------------
    @staticmethod
    def get_case_sensative_path(path):
        '''Returns a case sensative path on any system'''
        path = os.path.abspath(path)
        rest, last = os.path.split(path)
        if rest == path:
            drive, path = os.path.splitdrive(path)
            drive = drive.upper()
            return os.path.normpath(os.path.join(drive, path))

        if not last:
            return Path.get_case_sensative_path(rest) + os.path.sep

        if os.path.exists(rest):
            options = [x for x in os.listdir(rest) if x.lower() == last.lower()]
            if len(options) == 0:
                options = [last]
        else:
            options = [last]

        path = os.path.join(Path.get_case_sensative_path(rest), options[0])
        return os.path.normpath(path)

    #------------------------------------------------------------
    @staticmethod
    def get_branch_relative_path(path):
        '''Removes the current branch from the given path and returns it'''
        if Path.branch():
            path = path.replace(Path.branch(),'')
        return os.path.normpath(path)


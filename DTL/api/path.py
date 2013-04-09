"""
Path helper classes

Special thanks to John Crocker and Jason Orendorff
"""

import os
import sys
import errno

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
    # --- Path object internal python functions
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.path == other.path
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash(self.path)
    def __repr__(self):
        return 'Path( "{0}" )'.format(self.path)
    def __str__(self):
        return self.__repr__()
    def __add__(self, more):
        """Adding a path and a string yields a path."""
        try:
            resultStr = str.__add__(self.path, more)
        except TypeError:  #Python bug
            resultStr = NotImplemented
        if resultStr is NotImplemented:
            return resultStr
        return self.__class__(resultStr)
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other.__add__(self))
        else:
            return NotImplemented
    def __div__(self, rel):
        """ fp.__div__(rel) == fp / rel == fp.joinpath(rel)

        Join two path components, adding a separator character if
        needed.
        """
        return self.__class__(os.path.join(self, rel))

    # Make the / operator work even when true division is enabled.
    __truediv__ = __div__
    
    
    #------------------------------------------------------------
    # --- Path object properties
    #------------------------------------------------------------
    def _get_path(self):
        return self._path
    
    #------------------------------------------------------------
    def _set_path(self, path):
        if path is not None and path is not '':
            normPath = os.path.normpath(os.path.abspath(path))
            self._path = normPath.lower()
        else:
            self._path = None
    
    path = property(_get_path, _set_path)
    
    #------------------------------------------------------------
    @property
    def exists(self):
        return os.path.exists(self._path)
    
    #------------------------------------------------------------
    @property
    def isEmpty(self):
        if self._path is None or self._path == '':
            return True
        else:
            return False
    
    #------------------------------------------------------------
    @property
    def isFile(self):
        return os.path.isfile(self.caseSensative)
    
    #------------------------------------------------------------
    @property
    def ext(self):
        if self.isFile :
            return os.path.splitext(self._path)[1]
        elif os.path.splitext(self._path)[1]:
            return os.path.splitext(self._path)[1]
        else:
            return None
    
    #------------------------------------------------------------
    @property
    def parent(self):
        """ The parent directory, as a new path object.
        Example: path('/usr/local/lib/libpython.so').parent == path('/usr/local/lib')
        """
        return self.__class__(os.path.dirname(self._path))
    
    #------------------------------------------------------------
    @property
    def dir(self):
        """ Validates if this path is a directory and returns it
        if not then it returns the parent of this path
        """
        if os.path.isdir(self._path):
            return self
        else:
            return self.parent
    
    #------------------------------------------------------------
    @property
    def name(self):
        """ The name of this file or directory without the full path.
        Example: path('/usr/local/lib/libpython.so').name == 'libpython.so'
        """
        return os.path.basename(self._path)
    
    #------------------------------------------------------------
    @property
    def drive(self):
        """ The drive specifier, for example 'C:'.
        This is always empty on systems that don't use drive specifiers.
        """
        drive = ''
        if sys.platform == "win32" :
            drive, r = os.path.splitdrive(self._path)
        return drive
    
    #------------------------------------------------------------
    @property
    def caseSensative(self):
        """Path objects are stored in all lower with forward slashes
        If you need a caseSensative path use this instead of .path
        """
        return self.__class__.getCaseSensativePath(self._path)
    
    #------------------------------------------------------------
    @property
    def branchRelative(self):
        """Path objects are stored as absolute paths but the branch is stored on the class
        if you need a branch relative path use this instead of .path
        """
        return self.__class__.getBranchRelativePath(self._path)
    
    @property
    def mayaPath(self):
        """Returns a path suitible for maya"""
        return self.caseSensative.replace('\\','/')
    
    #------------------------------------------------------------
    # --- Statistic opertaions on files and directories
    def stat(self):
        """ Perform a stat() system call on this path. """
        return os.stat(self._path)
    
    def lstat(self):
        """ Like path.stat(), but do not follow symbolic links. """
        return os.lstat(self._path)
    
    #------------------------------------------------------------
    # --- Modifying operations on files and directories
    def chmod(self, mode):
        os.chmod(self._path, mode)
    def rename(self, new):
        os.rename(self._path, new)
        
    #------------------------------------------------------------
    # --- Create/delete operations on directories
    def mkdir(self, mode=0777):
        try:
            os.mkdir(self.dir.path, mode)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    def makedirs(self, mode=0777):
        try:
            os.makedirs(self.dir.path, mode)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    def rmdir(self):
        os.rmdir(self.dir.path)
    def removedirs(self):
        os.removedirs(self.dir.path)
        
    #------------------------------------------------------------
    # --- Modifying operations on files
    def touch(self):
        """ Set the access/modified times of this file to the current time.
        Create the file if it does not exist.
        """
        fd = os.open(self._path, os.O_WRONLY | os.O_CREAT, 0666)
        os.close(fd)
        os.utime(self._path, None)
    def remove(self):
        os.remove(self._path)
    def unlink(self):
        os.unlink(self._path)
        
    #------------------------------------------------------------
    # --- Operations on path strings.
    def abspath(self):       return self.__class__(os.path.abspath(self._path))
    def normcase(self):      return self.__class__(os.path.normcase(self._path))
    def normpath(self):      return self.__class__(os.path.normpath(self._path))
    def realpath(self):      return self.__class__(os.path.realpath(self._path))
    def expanduser(self):    return self.__class__(os.path.expanduser(self._path))
    def expandvars(self):    return self.__class__(os.path.expandvars(self._path))
    def dirname(self):       return self.__class__(os.path.dirname(self._path))
    
    def expand(self):
        """ Clean up a filename by calling expandvars(),
        expanduser(), and normpath() on it.

        This is commonly everything needed to clean up a filename
        read from a configuration file, for example.
        """
        return self.expandvars().expanduser().normpath()
        
    def join(self, *args):
        """ Join two or more path components, adding a separator
        character (os.sep) if needed.  Returns a new path
        object.
        """
        return self.__class__(os.path.join(self._path, *args))
    
    #------------------------------------------------------------
    # --- Operations used by paths but not limited to path objects
    @staticmethod
    def branch():
        '''Returns the directory of the Project Root for use in branch relative paths
        Will find the branch relative to the location of this python file
        It will be stored as a class variable for faster access in the future'''
        if Path._branch is None :
            path = os.path.abspath(sys.argv[0])
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
    def getCaseSensativePath(path):
        '''Returns a case sensative path on any system'''
        path = os.path.abspath(path)
        rest, last = os.path.split(path)
        if rest == path:
            drive, path = os.path.splitdrive(path)
            drive = drive.upper()
            return os.path.normpath(os.path.join(drive, path))

        if not last:
            return Path.getCaseSensativePath(rest) + os.path.sep

        if os.path.exists(rest):
            options = [x for x in os.listdir(rest) if x.lower() == last.lower()]
            if len(options) == 0:
                options = [last]
        else:
            options = [last]

        path = os.path.join(Path.getCaseSensativePath(rest), options[0])
        return os.path.normpath(path)

    #------------------------------------------------------------
    @staticmethod
    def getBranchRelativePath(path):
        '''Removes the current branch from the given path and returns it'''
        if Path.branch():
            path = path.replace(Path.branch(),'')
        return os.path.normpath(path)

if __name__ == "__main__" :
    myPath = Path('c:/Users/kylerockman/Downloads/blur3d.tgz.zip.bin')
    print myPath
    print myPath.name
    print myPath.caseSensative
    print myPath.drive
    print myPath.parent
    print myPath.ext
    myPath = myPath.join("agent.rar")
    print myPath
    print myPath.ext

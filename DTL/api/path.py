"""
path.py - An object representing a path to a file or directory.

Current Author : Kyle Rockman

Special thanks to:
 John Crocker
 Jason Orendorff
 Mikhail Gusarov <dottedmag@dottedmag.net>
 Marc Abramowitz <marc@marc-abramowitz.com>
 Jason R. Coombs <jaraco@jaraco.com>
 Jason Chu <jchu@xentac.net>
 Vojislav Stojkovic <vstojkovic@syntertainment.com>
"""
import os
import imp
import sys
import shutil

import re
import fnmatch
import glob

import errno

__all__ = ['Path']

#------------------------------------------------------------
#------------------------------------------------------------
class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

#------------------------------------------------------------
#------------------------------------------------------------
class Path(unicode):
    """ Represents a filesystem path.

    For documentation on individual methods, consult their
    counterparts in os.path.
    """
    module = os.path #The module to use for path operations.
    _branch = None
    #------------------------------------------------------------
    def __init__(self, value=''):
        if not isinstance(value, basestring):
            raise TypeError("path must be a string")

    #------------------------------------------------------------
    # Path object class methods
    #------------------------------------------------------------
    @ClassProperty
    @classmethod
    def _next_class(cls):
        """
        What class should be used to construct new instances from this class
        """
        return cls
    
    @classmethod
    def getcwd(cls):
        """ Return the current working directory as a path object. """
        return cls(os.getcwdu())
    
    @classmethod
    def getMainDir(cls):
        """ This will get us the program's directory,
        even if we are frozen using py2exe"""
        from DTL import getcwd
        return cls(getcwd())
    
    @classmethod
    def getHomeDir(cls):
        """ This will get us the user's home directory"""
        return cls('~').expand()

    #------------------------------------------------------------
    # Path object dunder methods
    #------------------------------------------------------------
    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, super(Path, self).__repr__())
    def __eq__(self, other):
        return self.lower() == other.lower()
    def __ne__(self, other):
        return not self.__eq__(other)
    def __add__(self, more):
        """Adding a path and a string yields a path."""
        try:
            return self._next_class(super(Path, self).__add__(more))
        except TypeError:  # Python bug
            return NotImplemented
    def __radd__(self, other):
        if not isinstance(other, basestring):
            return NotImplemented
        return self._next_class(other.__add__(self))
    def __div__(self, rel):
        """ fp.__div__(rel) == fp / rel == fp.joinpath(rel)

        Join two path components, adding a separator character if
        needed.
        """
        return self._next_class(self.module.join(self, rel))
    # Make the / operator work even when true division is enabled.
    __truediv__ = __div__        
    def __enter__(self):
        self._old_dir = self.getcwd()
        os.chdir(self)
    def __exit__(self, *_):
        os.chdir(self._old_dir)

    #------------------------------------------------------------
    # os module wrappers
    #------------------------------------------------------------
    def stat(self): return os.stat(self)
    def lstat(self): return os.lstat(self)
    def chmod(self, mode): os.chmod(self, mode)
    def rename(self, new): os.rename(self, new); return self._next_class(new)
    def unlink(self): os.unlink(self)
    
    #------------------------------------------------------------
    # os.path module wrappers
    #------------------------------------------------------------
    def isabs(self): return self.module.isabs(self)
    def exists(self): return self.module.exists(self)
    def isdir(self): return self.module.isdir(self)
    def isfile(self): return self.module.isfile(self)
    def islink(self): return self.module.islink(self)
    def ismount(self): return self.module.ismount(self)
    def samefile(self): return self.module.samefile(self)
    def atime(self): return self.module.getatime(self)
    def mtime(self): return self.module.getmtime(self)
    def ctime(self): return self.module.getctime(self)
    def size(self): return self.module.getsize(self)
    
    #------------------------------------------------------------
    def isdirEmpty(self): return len(self.listdir()) == 0

    #------------------------------------------------------------
    # os.path module wrappers that returns path objects
    #------------------------------------------------------------
    def abspath(self): return self._next_class(self.module.abspath(self))
    def normcase(self): return self._next_class(self.module.normcase(self))
    def normpath(self): return self._next_class(self.module.normpath(self))
    def realpath(self): return self._next_class(self.module.realpath(self))
    def expanduser(self): return self._next_class(self.module.expanduser(self))
    def expandvars(self): return self._next_class(self.module.expandvars(self))
    def dirname(self): return self._next_class(self.module.dirname(self))
    def basename(self):return self._next_class(self.module.basename(self))
    #------------------------------------------------------------
    def splitpath(self):
        """ p.splitpath() -> Return (p.parent, p.name). """
        parent, child = self.module.split(self)
        return self._next_class(parent), child
    #------------------------------------------------------------
    def splitdrive(self):
        """ p.splitdrive() -> Return (p.drive, <the rest of p>).

        Split the drive specifier from this path.  If there is
        no drive specifier, p.drive is empty, so the return value
        is simply (path(''), p).  This is always the case on Unix.
        """
        drive, rel = self.module.splitdrive(self)
        return self._next_class(drive), rel
    #------------------------------------------------------------
    def splitext(self):
        """ p.splitext() -> Return (p.stripext(), p.ext).

        Split the filename extension from this path and return
        the two parts.  Either part may be empty.

        The extension is everything from '.' to the end of the
        last path segment.  This has the property that if
        (a, b) == p.splitext(), then a + b == p.
        """
        filename, ext = self.module.splitext(self)
        return self._next_class(filename), ext
    #------------------------------------------------------------
    def stripext(self):
        """ p.stripext() -> Remove one file extension from the path.

        For example, path('/home/guido/python.tar.gz').stripext()
        returns path('/home/guido/python.tar').
        """
        return self.splitext()[0]
    #------------------------------------------------------------
    def expand(self):
        """ Clean up a filename by calling expandvars(),
        expanduser(), and normpath() on it.

        This is commonly everything needed to clean up a filename
        read from a configuration file, for example.
        """
        return self.expandvars().expanduser().normpath()
    #------------------------------------------------------------
    def join(self, *args):
        """ Join two or more path components, adding a separator
        character (os.sep) if needed.  Returns a new path
        object.
        """
        return self._next_class(self.module.join(self, *args))
    #------------------------------------------------------------
    def listdir(self, pattern=None):
        """ D.listdir() -> List of items in this directory.

        Use D.files() or D.dirs() instead if you want a listing
        of just files or just subdirectories.

        The elements of the list are path objects.

        With the optional 'pattern' argument, this only lists
        items whose names match the given pattern.
        """
        names = os.listdir(self)
        if pattern is not None:
            names = fnmatch.filter(names, pattern)
        return [self / child for child in names]
    #------------------------------------------------------------
    def dirs(self, pattern=None):
        """ D.dirs() -> List of this directory's subdirectories.

        The elements of the list are path objects.
        This does not walk recursively into subdirectories
        (but see path.walkdirs).

        With the optional 'pattern' argument, this only lists
        directories whose names match the given pattern.  For
        example, ``d.dirs('build-*')``.
        """
        return [p for p in self.listdir(pattern) if p.isdir()]
    #------------------------------------------------------------
    def files(self, pattern=None):
        """ D.files() -> List of the files in this directory.

        The elements of the list are path objects.
        This does not walk into subdirectories (see path.walk).

        With the optional 'pattern' argument, this only lists files
        whose names match the given pattern.  For example,
        ``d.files('*.pyc')``.
        """
        return [p for p in self.listdir(pattern) if p.isfile()]
    #------------------------------------------------------------
    def walk(self, pattern=None, topdown=False):
        """Returns children files and dirs recusively as path objects"""
        for root, dirs, files in os.walk(self, topdown=topdown):
            for name in files:
                next_path = self._next_class(os.path.join(root, name))
                if pattern is None or next_path.fnmatch(pattern):
                    yield next_path
            for name in dirs:
                next_path = self._next_class(os.path.join(root, name))
                if pattern is None or next_path.fnmatch(pattern):
                    yield next_path
    #------------------------------------------------------------
    def regex(self, pattern, inclusive=False, topdown=False):
        """ Return a list of path objects that match the pattern,
        
        pattern - a regular expression
        
        """
        output_files = []
        output_dirs = []
        regexObj = re.compile(pattern)
        for root, dirs, files in os.walk(self, topdown=topdown):
            for name in files:
                next_path = self._next_class(os.path.join(root, name))
                if bool(regexObj.search(next_path)) == bool(not inclusive):
                    output_files.append(next_path)
            for name in dirs:
                next_path = self._next_class(os.path.join(root, name))
                if pattern is None or next_path.fnmatch(pattern):
                    output_dirs.append(next_path)
        return output_files, output_dirs
    #------------------------------------------------------------
    def fnmatch(self, pattern):
        """ Return True if self.name matches the given pattern.

        pattern - A filename pattern with wildcards,
            for example ``'*.py'``.
        """
        return fnmatch.fnmatch(self.name, pattern)
    #------------------------------------------------------------
    def glob(self, pattern):
        """ Return a list of path objects that match the pattern.

        pattern - a path relative to this directory, with wildcards.

        For example, path('/users').glob('*/bin/*') returns a list
        of all the files users have in their bin directories.
        """
        cls = self._next_class
        return [cls(s) for s in glob.glob(self / pattern)]
    #------------------------------------------------------------
    def open(self, mode='r'):
        """ Open this file.  Return a file object. """
        return open(self, mode)


    #------------------------------------------------------------
    # Modifying operations on files and directories  
    #------------------------------------------------------------
    def mkdir(self, mode=0777):
        try:
            os.mkdir(self.dir(), mode)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    #------------------------------------------------------------
    def makedirs(self, mode=0777):
        try:
            os.makedirs(self.dir(), mode)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    #------------------------------------------------------------
    def rmdir(self):
        try:
            os.rmdir(self.dir())
        except OSError, e:
            if e.errno != errno.ENOTEMPTY and e.errno != errno.EEXIST:
                raise
    #------------------------------------------------------------
    def removedirs(self):
        try:
            os.removedirs(self.dir())
        except OSError, e:
            if e.errno != errno.ENOTEMPTY and e.errno != errno.EEXIST:
                raise
    #------------------------------------------------------------
    def rmtree(self):
        try:
            shutil.rmtree(self)
        except OSError, e:
            if e.errno != errno.ENOENT:
                raise   

    copyfile = shutil.copyfile
    copymode = shutil.copymode
    copystat = shutil.copystat
    copy = shutil.copy
    copy2 = shutil.copy2
    copytree = shutil.copytree
    #------------------------------------------------------------
    def touch(self):
        """ Set the access/modified times of this file to the current time.
        Create the file if it does not exist.
        """
        fd = os.open(self, os.O_WRONLY | os.O_CREAT, 0666)
        os.close(fd)
        os.utime(self, None)
    #------------------------------------------------------------
    def remove(self):
        try:
            self.unlink()
        except OSError, e:
            if e.errno != errno.ENOENT:
                raise

    #------------------------------------------------------------
    # Path Object Properties
    #------------------------------------------------------------
    @property
    def ext(self):
        return self.splitext()[-1]

    #------------------------------------------------------------
    @property
    def parent(self):
        """ The parent directory, as a new path object.
        Example: path('/usr/local/lib/libpython.so').parent == path('/usr/local/lib')
        """
        return self.dirname()
    
    #------------------------------------------------------------
    @property
    def name(self):
        """ The name of this file or directory without the full path.
        Example: path('/usr/local/lib/libpython.so').name == 'libpython.so'
        """
        return self.basename()

    #------------------------------------------------------------
    @property
    def drive(self):
        """ The drive specifier, for example 'C:'.
        This is always empty on systems that don't use drive specifiers.
        """
        return self.splitdrive()[0]

    #------------------------------------------------------------
    # Misc utility methods
    #------------------------------------------------------------
    def dir(self):
        """ Validates if this path is a directory and returns it
        if not then it returns the parent of this path
        """
        if not self.exists() : #This is an atempt at best guess
            head, tail = self.splitpath()
            if os.path.splitext(tail)[1] == '' :
                return self
            return head
        if self.isdir():
            return self
        else:
            return self.parent
    
    #------------------------------------------------------------
    def caseSensative(self):
        """Path objects are stored in all lower with python escaped backwards slashes
        If you need a caseSensative path use this
        """
        return self.__class__.getCaseSensativePath(self)

    #------------------------------------------------------------
    def branchRelative(self):
        """Path objects are stored as absolute paths but the branch is stored on the class
        if you need a branch relative path use this
        """
        return self.__class__.getBranchRelativePath(self)
    
    #------------------------------------------------------------
    def mayaPath(self):
        """Returns a path suitible for maya"""
        return self.caseSensative().replace('\\','/')


    #------------------------------------------------------------
    # Utilties used for paths but not limited to path objects
    #------------------------------------------------------------
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
    print Path.getMainDir()
    
    myPathSepTest = Path('c:\\Users/krockman/documents').join('mytest')
    print myPathSepTest    
    
    myPath = Path(r'C:\Users\krockman\documents\StarCitizen\Client\blur3d.tgz.zip.bin'.lower())
    print "documents" in myPath
    print myPath != myPath
    print myPath
    print myPath.name
    print "case sensative", myPath.caseSensative()
    print myPath.drive
    print "parent", myPath.parent
    print myPath.ext
    myPath = myPath.join("agent.rar")
    print myPath
    print myPath.ext
    print {"MyVar": myPath} == {"MyVar":'c:/users/Krockman/Documents/sTaRcItIzeN/client/blur3d.tgz.zip.bin/agent.rar'}
    print {"MyVar": myPath}
    print Path.getMainDir()
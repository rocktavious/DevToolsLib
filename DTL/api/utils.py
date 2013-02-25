'''
Utility Funcs for DTL

These are imported into the DTL namespace upon import
'''
import os
import sys
import subprocess
from PyQt4 import QtCore, QtGui

from . import Settings, Path


#------------------------------------------------------------
def getAppSettings():
    return QtCore.QSettings(Settings['COMPANY'], Settings._pkg)

#------------------------------------------------------------
def activeWindow():
    if QtGui.QApplication.instance():
        return QtGui.QApplication.instance().activeWindow()
    return None

#------------------------------------------------------------
def getStyleSheet():
    ss_file = Settings._resources_dir.new_path_join('darkorange.stylesheet')
    data = ''
    with open(ss_file.path, 'r') as filespec :
        data = filespec.read()
    return '%s' % data

#------------------------------------------------------------
def rootWindow():
    window = None
    if (QtGui.QApplication.instance()):
        window = QtGui.QApplication.instance().activeWindow()

        # grab the root window
        if (window):
            while (window.parent()):
                window = window.parent()

    return window

#------------------------------------------------------------
def runFile( filepath, basePath=None, cmd=None, debug=False ):
    """
    Runs the filepath in a shell with proper commands given, or passes 
    the command to the shell. (CMD in windows) the current platform

    :param filepath: path to the file to execute
    :param basePath: working directory where the command should be called
    from.  If omitted, the current working directory is used.

    """
    status = False
    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    # make sure the filepath we're running is a file 
    if not filepath.isFile:
        return status

    # determine the base path for the system
    if basePath is None:
        basePath = filepath.dir
        
    options = { 'filepath': filepath.path, 'basepath': basePath }

    if cmd == None :
        if filepath.ext in ['.py','.pyw']:
            if debug:
                cmd = 'python.exe "%s"' % filepath.path
            else:
                cmd = 'pythonw.exe "%s"' % filepath.path
            
            status = subprocess.Popen( cmd, stdout=sys.stdout, stderr=sys.stderr, shell=debug, cwd=basePath)
            #status = subprocess.Popen('cmd.exe /k %s' % cmd, cwd=basePath)

    if not status :
        try:
            status = os.startfile(filepath.path)
        except:
            print 'Core.runFile] Cannot run type (*%s)' % filepath.ext

    return status



#------------------------------------------------------------
def notifyUser(msg='', parent=None):
    QtGui.QMessageBox.question(parent,
                               'Message',
                               msg,
                               QtGui.QMessageBox.Ok,
                               QtGui.QMessageBox.Ok)        

#------------------------------------------------------------
def getConfirmDialog(msg='', parent=None):
    reply = QtGui.QMessageBox.question(parent,
                                       'Message',
                                       msg,
                                       QtGui.QMessageBox.Yes | 
                                       QtGui.QMessageBox.No,
                                       QtGui.QMessageBox.No)
    
    if reply == QtGui.QMessageBox.Yes:
        return True
    else:
        return False

#------------------------------------------------------------
def getFileFromUser(parent=None, ext=[]):
    file_dialog = QtGui.QFileDialog(parent)
    file_dialog.setViewMode(QtGui.QFileDialog.Detail)
    return _return_file(file_dialog)

#------------------------------------------------------------
def getDirFromUser(parent=None):
    file_dialog = QtGui.QFileDialog(parent)
    file_dialog.setFileMode(QtGui.QFileDialog.Directory)
    file_dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
    file_dialog.setViewMode(QtGui.QFileDialog.Detail)
    return _return_file(file_dialog)    

#------------------------------------------------------------
def getSaveFileFromUser(parent=None, ext=[]):
    file_dialog = QtGui.QFileDialog(parent)
    file_dialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
    file_dialog.setViewMode(QtGui.QFileDialog.Detail)
    return _return_file(file_dialog)

#------------------------------------------------------------
def _return_file(file_dialog):
    if file_dialog.exec_():
        returned_file = str(file_dialog.selectedFiles()[0])
        return Path(returned_file)
    return Path()
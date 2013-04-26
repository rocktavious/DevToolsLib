'''
Utility functions for working with pyqt
'''
import os
import sys
import imp
import types
import re
import subprocess
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from DTL import __pkgname__, __company__, __pkgresources__
from DTL.api.path import Path

#------------------------------------------------------------
def getApp():
    app = QtGui.QApplication.instance()
    if not app :
        app = QtGui.QApplication(sys.argv)
        app.setStyle( 'Plastique' )
        #app.setStyleSheet(Utils.getStyleSheet())
    
    return app

#------------------------------------------------------------
def getAppSettings():
    return QtCore.QSettings(__company__, __pkgname__)

#------------------------------------------------------------
def getActiveWindow():
    activeWindow = None
    if QtGui.QApplication.instance():
        activeWindow = QtGui.QApplication.instance().activeWindow()

    return activeWindow

#------------------------------------------------------------
def getStyleSheet():
    ss_file = os.path.join(__pkgresources__, 'darkorange.stylesheet')
    data = ''
    with open(ss_file, 'r') as filespec :
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
def notifyUser(msg='', parent=None):
    QtGui.QMessageBox.question(parent,
                               'Message',
                               msg,
                               QtGui.QMessageBox.Ok,
                               QtGui.QMessageBox.Ok)

#------------------------------------------------------------
def pauseDialog(msg='', parent=None, func=None):
    msgbox = QtGui.QMessageBox(parent)
    msgbox.setAttribute(Qt.WA_DeleteOnClose)
    msgbox.setWindowTitle('Message')
    msgbox.setText(msg)
    yesbtn = msgbox.addButton(QtGui.QMessageBox.Yes)
    yesbtn.clicked.connect(func)
    msgbox.addButton(QtGui.QMessageBox.No)
    msgbox.setModal(False)
    msgbox.show()

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
def getUserInput(msg='', parent=None):
    text, success = QtGui.QInputDialog.getText(parent, 'Input Dialog', msg)
    return str(text), success

#------------------------------------------------------------
def getFileFromUser(parent=None, ext=''):
    file_dialog = QtGui.QFileDialog(parent)
    file_dialog.setViewMode(QtGui.QFileDialog.Detail)
    file_dialog.setNameFilter(ext)
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
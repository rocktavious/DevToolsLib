'''
Utility functions for working with pyqt
'''
import os
import sys
import imp
import types
import re
import subprocess
from DTL.qt import QtCore, QtGui
from DTL.api import Path
from DTL.gui import Core

#------------------------------------------------------------
def getActiveWindow():
    activeWindow = None
    if QtGui.QApplication.instance():
        activeWindow = QtGui.QApplication.instance().activeWindow()

    return activeWindow

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
    return success, str(text)

#------------------------------------------------------------
def getFileFromUser(parent=None, ext=''):
    return Core.getFileFromUser()

#------------------------------------------------------------
def getDirFromUser(parent=None):
    return Core.getDirFromUser()

#------------------------------------------------------------
def getSaveFileFromUser(parent=None, ext=[]):
    return Core.getSaveFileFromUser()


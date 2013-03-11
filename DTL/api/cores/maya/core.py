import sip
from PyQt4 import QtCore, QtGui
import maya.OpenMayaUI as OM_UI

from ... import Settings, Utils
from ..external.core import Core

#------------------------------------------------------------
#------------------------------------------------------------
class MayaCore(Core):
    '''Tool Environment Core for Maya'''
    #------------------------------------------------------------
    @staticmethod
    def getMayaWindow():
	    """Get the main Maya window as a QtGui.QMainWindow instance"""
	    ptr = OM_UI.MQtUtil.mainWindow()
	    if ptr is not None:
		    return sip.wrapinstance(long(ptr), QtCore.QObject)
    
    #------------------------------------------------------------
    @staticmethod
    def getMayaQtObject(mayaUiName):
	    """Convert a Maya ui path(Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" ) to a Qt object"""	    
	    ptr = OM_UI.MQtUtil.findControl(mayaUiName)
	    if ptr is None:
		    ptr = OM_UI.MQtUtil.findLayout(mayaUiName)
	    if ptr is None:
		    ptr = OM_UI.MQtUtil.findMenuItem(mayaUiName)
	    if ptr is not None:
		    return sip.wrapinstance(long(ptr), QtCore.QObject)
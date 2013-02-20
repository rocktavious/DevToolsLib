def getMayaWindow():
	"""
	Get the main Maya window as a QtGui.QMainWindow instance
	@return: QtGui.QMainWindow instance of the top level Maya windows
	"""
	import sip
	import maya.OpenMayaUI as OM_UI
	ptr = OM_UI.MQtUtil.mainWindow()
	if ptr is not None:
		return sip.wrapinstance(long(ptr), QtCore.QObject)
def getMayaQtObject(mayaName):
	"""
	Convert a Maya ui path to a Qt object
	@param mayaName: Maya UI Path to convert (Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" )
	@return: PyQt representation of that object
	"""
	import sip
	import maya.OpenMayaUI as OM_UI
	ptr = OM_UI.MQtUtil.findControl(mayaName)
	if ptr is None:
		ptr = OM_UI.MQtUtil.findLayout(mayaName)
	if ptr is None:
		ptr = OM_UI.MQtUtil.findMenuItem(mayaName)
	if ptr is not None:
		return sip.wrapinstance(long(ptr), QtCore.QObject)
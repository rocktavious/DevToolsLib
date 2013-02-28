import os
from PyQt4 import QtCore, QtGui
from DTL.api import SubTool


#------------------------------------------------------------
#------------------------------------------------------------
class PropertiesEditor(SubTool):
    
    #------------------------------------------------------------
    def onInit(self):
        self._model = None
        self._proxyModel = None
        self._editors = {}
        self.ui_file = os.path.join(os.path.dirname(__file__),'views','properties_editor.ui')
    
    #------------------------------------------------------------
    def onFinalize(self):
        self.setEditors()
        for key, editor in self._editors.items() :
            self.properties_layout.addWidget(editor)
            editor.setVisible(False)
        
    #------------------------------------------------------------
    def setEditors(self):
        '''For subclass to implement all of the editors'''
        self._editors['Node'] = NodeEditor()
        self._editors['FloatTransformNode'] = FloatTransformNodeEditor()
        self._editors['IntTransformNode'] = IntTransformNodeEditor()
        self._editors['Layer'] = LayerEditor()
        pass
    
    #------------------------------------------------------------
    def setProxyModel(self, proxyModel):
        self._proxyModel = proxyModel
        
        for key, editor in self._editors.items() :
            editor.setProxyModel(model)
    
    #------------------------------------------------------------
    def setModel(self, model):
        for key, editor in self._editors.items() :
            editor.setModel(model)
            
    #------------------------------------------------------------
    def clearSelection(self):
        for key, editor in self._editors.items():
            editor.setVisible(False)          
    
    #------------------------------------------------------------
    def setSelection(self, index):
        if self._proxyModel is not None :
            index = self._proxyModel.mapToSource(index)

        self.clearSelection()

        node = index.internalPointer()
        if node is None :
            return
        
        for key, editor in self._editors.items():
            editor.setSelection(index)
            
        for item in node.__class__.__mro__ :
            if not hasattr(item, '__name__') :
                continue
            
            if self._editors.get(item.__name__, False):
                self._editors[item.__name__].setVisible(True)


#------------------------------------------------------------
#------------------------------------------------------------
class Editor(SubTool):
    
    #------------------------------------------------------------
    def __init__(self):
        super(Editor, self).__init__(register=False)
    
    #------------------------------------------------------------
    def onInit(self):
        self._model = None
        self._proxyModel = None
        self._dataMapper = QtGui.QDataWidgetMapper()
        #self._dataMapper.setSubmitPolicy(QtGui.QDataWidgetMapper.ManualSubmit)
    
    #------------------------------------------------------------
    def setProxyModel(self, proxyModel):
        self._proxyModel = proxyModel
        self._model = proxyModel.sourceModel()
        self._dataMapper.setModel(self._model)
        
        self.setMappings()
    
    #------------------------------------------------------------
    def setModel(self, model):
        self._model = model
        self._dataMapper.setModel(self._model)
        
        self.setMappings()
    
    #------------------------------------------------------------
    def setMappings(self):
        '''For Subclass to implement to map the UI elements to the data'''
        #self._dataMapper.addMapping(self.uiName, 0)
        #self._dataMapper.addMapping(self.uiType, 1)
        pass
        
    #------------------------------------------------------------
    def setSelection(self, index):
        parent = index.parent()
        self._dataMapper.setRootIndex(parent)
        
        self._dataMapper.setCurrentModelIndex(index)


#------------------------------------------------------------
#------------------------------------------------------------
class NodeEditor(Editor):
    #------------------------------------------------------------
    def onInit(self):
        super(NodeEditor, self).onInit()
        self.ui_file = os.path.join(os.path.dirname(__file__),'views','node_editor.ui')
    
    #------------------------------------------------------------
    def setMappings(self):
        self._dataMapper.addMapping(self.prop_name, 0)
        self._dataMapper.addMapping(self.prop_type, 1)
        
#------------------------------------------------------------
#------------------------------------------------------------
class FloatTransformNodeEditor(Editor):
    #------------------------------------------------------------
    def onInit(self):
        super(FloatTransformNodeEditor, self).onInit()
        self.ui_file = os.path.join(os.path.dirname(__file__),'views','floattransformnode_editor.ui')
    
    #------------------------------------------------------------
    def setMappings(self):
        self._dataMapper.addMapping(self.prop_x, 2)
        self._dataMapper.addMapping(self.prop_y, 3)
        self._dataMapper.addMapping(self.prop_z, 4)
        

#------------------------------------------------------------
#------------------------------------------------------------
class IntTransformNodeEditor(Editor):
    #------------------------------------------------------------
    def onInit(self):
        super(IntTransformNodeEditor, self).onInit()
        self.ui_file = os.path.join(os.path.dirname(__file__),'views','inttransformnode_editor.ui')
    
    #------------------------------------------------------------
    def setMappings(self):
        self._dataMapper.addMapping(self.prop_x, 2)
        self._dataMapper.addMapping(self.prop_y, 3)
        self._dataMapper.addMapping(self.prop_z, 4)
        
#------------------------------------------------------------
#------------------------------------------------------------
class LayerEditor(Editor):
    #------------------------------------------------------------
    def onInit(self):
        super(LayerEditor, self).onInit()
        self.ui_file = os.path.join(os.path.dirname(__file__),'views','layer_editor.ui')
    
    #------------------------------------------------------------
    def setMappings(self):
        self._dataMapper.addMapping(self.prop_index, 2)
        

        

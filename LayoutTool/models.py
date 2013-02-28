from PyQt4 import QtCore, QtGui

from DTL.api import Utils
from DTL.db.data import Layer
from DTL.db.models import SceneGraphModel

from data import Tile

class MapModel(SceneGraphModel):
    
    def addLayer(self):
        text, success = Utils.getUserInput('Enter new layer name:')
        
        if success:
            child = Layer(name=text)
            self.insertRows(0,1,node=child)

        return success
    
    def addTile(self):
        child = Tile(name='Tile')
        parent = self.index(0,0,QtCore.QModelIndex())
        childCount = parent.internalPointer().childCount()
        self.insertRows(childCount,1,parent,child)
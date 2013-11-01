from DTL.qt import QtCore, QtGui
from DTL.qt.QtCore import Qt


#------------------------------------------------------------
#------------------------------------------------------------
class ListModel(QtCore.QAbstractListModel):
    #------------------------------------------------------------
    def __init__(self, data=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__data = data
    
    #------------------------------------------------------------
    def rowCount(self, parent):
        return len(self.__data)
    
    #------------------------------------------------------------
    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    #------------------------------------------------------------
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            
            if orientation == Qt.Horizontal :
                return QtCore.QString("%1").arg(section)
            else:
                return QtCore.QString("%1").arg(section)
    
    #------------------------------------------------------------
    def data(self, index, role):
        row = index.row()
        value = self.__data[row]
        
        if role == Qt.EditRole :
            return value
        
        if role == Qt.DisplayRole :
            return value
        
        if role == Qt.ToolTipRole :
            return value
        
        #if role == Qt.DecorationRole:
            #pixmap = QtGui.QPixmap(26, 26)
            #pixmap.fill(QtGui.QColor(0,0,0))
            #icon = QtGui.QIcon(pixmap)
            #return icon
    
    #------------------------------------------------------------
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            self.__data.insert(position, '')
        
        self.endInsertRows()
        return True
    
    #------------------------------------------------------------
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            value = self.__data[position]
            self.__data.remove(value)
        
        self.endRemoveRows()
        return True
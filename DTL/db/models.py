from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

from .data import Node

#------------------------------------------------------------
#------------------------------------------------------------
class TableModel(QtCore.QAbstractTableModel):
    #------------------------------------------------------------
    def __init__(self, data=[[]], headers=[], parent=None):
        super(TableModel, self).__init__(parent)
        self.__data = data
        self.__headers = headers
    
    #------------------------------------------------------------
    def rowCount(self, parent):
        return len(self.__data)
    
    #------------------------------------------------------------
    def columnCount(self, parent):
        return len(self.__data[0])
    
    #------------------------------------------------------------
    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    #------------------------------------------------------------
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            
            if orientation == Qt.Horizontal :
                if section < len(self._headers):
                    return self.__headers[section]
                else:
                    return 'NONE'
            else:
                return QtCore.QString("%1").arg(section)
    
    #------------------------------------------------------------
    def data(self, index, role):
        row = index.row()
        column = index.column()
        value = self.__data[row][column]
        
        if role == Qt.EditRole :
            return value
        
        if role == Qt.DisplayRole :
            return value
        
        if role == Qt.ToolTipRole :
            return value
        
        if role == Qt.DecorationRole:
            pixmap = QtGui.QPixmap(26, 26)
            pixmap.fill(QtGui.QColor(0,0,0))
            icon = QtGui.QIcon(pixmap)
            return icon
    
    #------------------------------------------------------------
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            default_values = ['' for i in range(self.columnCount(None))]
            self.__data.insert(position, default_values)
        
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
    
    #------------------------------------------------------------
    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        
        rowCount = len(self.__data)
        
        for i in range(columns):
            for j in range(rowCount):
                self.__data[j].insert(position, '')
                
        self.endInsertColumns()
        
        return True
    
    #------------------------------------------------------------
    def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + columns - 1)

        rowCount = len(self.__data)
        
        for i in range(columns):
            for j in range(rowCount):
                value = self.__data[j][position]
                self.__data[j].remove(value)
        
        self.endRemoveRows()
        return True


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
        
        if role == Qt.DecorationRole:
            pixmap = QtGui.QPixmap(26, 26)
            pixmap.fill(QtGui.QColor(0,0,0))
            icon = QtGui.QIcon(pixmap)
            return icon
    
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


#------------------------------------------------------------
#------------------------------------------------------------
class SceneGraphModel(QtCore.QAbstractItemModel):
    sortRole   = Qt.UserRole
    filterRole = Qt.UserRole + 1
    #------------------------------------------------------------
    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root
    
    #------------------------------------------------------------
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()
    
    #------------------------------------------------------------
    def columnCount(self, parent):
        return 1
    
    #------------------------------------------------------------
    def data(self, index, role):
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return node.data(index.column())
 
        if role == Qt.DecorationRole:
            if index.column() == 0:
                resource = node.resource()
                return QtGui.QIcon(QtGui.QPixmap(resource))
            
        if role == SceneGraphModel.sortRole:
            return node.typeInfo()

        if role == SceneGraphModel.filterRole:
            return node.typeInfo()

    #------------------------------------------------------------
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            
            node = index.internalPointer()
            
            if role == Qt.EditRole:
                node.setData(index.column(), value)
                self.dataChanged.emit(index, index)
                return True
            
        return False
    
    #------------------------------------------------------------
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if section == 0:
                return "Scenegraph"
            else:
                return "Typeinfo"
    
    #------------------------------------------------------------
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
    
    #------------------------------------------------------------
    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent()
        
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)
    
    #------------------------------------------------------------
    def index(self, row, column, parent):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()
    
    #------------------------------------------------------------
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
            
        return self._rootNode
    
    #------------------------------------------------------------
    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), node=None):
        parentNode = self.getNode(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            
            childCount = parentNode.childCount()
            if node :
                childNode = node
            else:
                childNode = Node(name="untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        
        self.endInsertRows()

        return success
    
    #------------------------------------------------------------
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parentNode.removeChild(position)
            
        self.endRemoveRows()
        
        return success

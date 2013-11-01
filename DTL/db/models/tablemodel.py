from DTL.qt import QtCore, QtGui
from DTL.qt.QtCore import Qt

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
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return 'NONE'
            else:
                return section

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

        #if role == Qt.DecorationRole:
            #pixmap = QtGui.QPixmap(26, 26)
            #pixmap.fill(QtGui.QColor(0,0,0))
            #icon = QtGui.QIcon(pixmap)
            #return icon

    #------------------------------------------------------------
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            if role == Qt.EditRole:
                self.__data[index.row()][index.column()] = value
                self.dataChanged.emit(index, index)
                return True

        return False

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
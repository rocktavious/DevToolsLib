import sys
from PyQt4.QtCore import Qt,QDir,QObject,QString,SIGNAL,SLOT
from PyQt4.QtGui  import QApplication,QDirModel,QSplitter,QListView,QTreeView,QTableView,QPushButton
 
app = QApplication(sys.argv)
dirModel  = QDirModel()
 
# Make something like:
#  ____  ____  ____
# |view||view||view|
# |____||____||____|
# |__b_u_t_t_o_n___|
#
 
# Splits top-bottom first.
vsplitter=QSplitter()
vsplitter.setOrientation( Qt.Vertical )
 
#Top pane has the three views, split horizontally
hsplitter = QSplitter(  vsplitter )
listView  = QListView(  hsplitter )
treeView  = QTreeView(  hsplitter )
tableView = QTableView( hsplitter )
 
# ...set all three to view the same directory model
listView.setModel(  dirModel )
treeView.setModel(  dirModel )
tableView.setModel( dirModel )
 
#(I forget exactly what this was for. Consistent item indexing, perhaps?)
treeView.setRootIndex(  dirModel.index( QDir.currentPath() ) )
listView.setRootIndex(  dirModel.index( QDir.currentPath() ) )
tableView.setRootIndex( dirModel.index( QDir.currentPath() ) )
 
#Synchronize *selection* between views as well
listView.setSelectionModel(  treeView.selectionModel() );
tableView.setSelectionModel( treeView.selectionModel() );
 
 
#Bottom pane of the vertical split just has a big quit button
quit=QPushButton(QString("Quit"),vsplitter)
#The button executes the quit function
QObject.connect( quit,SIGNAL("clicked()") ,
                 app, SLOT("quit()") )
 
#Window details (vsplitter is effectively the window itself)
vsplitter.setWindowTitle("Three selection-synched views of the current dir")
vsplitter.resize(600, 400)
app.setActiveWindow(vsplitter) #this may be implied by not giving it a parent, verify.
vsplitter.show()
 
sys.exit( app.exec_() )
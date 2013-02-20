import os
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QApplication, QMainWindow

from ...api import Settings

#------------------------------------------------------------
#------------------------------------------------------------
class Core(QObject):
    '''Tool Environment Core'''
    #------------------------------------------------------------
    def __init__(self):
        super(Core, self).__init__()
        self._app = None
        self._has_app_exec = False
        self.setObjectName(Settings['COMPANY'] + ' Tools Environment Core')
        self.on_init()
        self.wnd = QMainWindow()
        self.wnd.show()

    #------------------------------------------------------------
    def on_init(self):
        self._app = QApplication.instance()
        if not self._app :
            self._app = QApplication([])
        
        
        self._app.setStyle( 'Plastique' )
        self._app.setStyleSheet(self.getStyleSheet())
    
    #------------------------------------------------------------
    def start(self):
        if ( self._app and not self._has_app_exec):
            self._has_app_exec = True
            print "QT App Started!"
            self._app.exec_()
            self.shutdown()
            print "QT App Finished!"

    #------------------------------------------------------------
    def shutdown(self):
        if (QApplication.instance()):
            QApplication.instance().closeAllWindows()
            QApplication.instance().quit()
                
    
    #------------------------------------------------------------
    def getStyleSheet(self):
        ss_file = Settings._resources_dir.new_path_join('darkorange.stylesheet')
        data = ''
        with open(ss_file.path, 'r') as filespec :
            data = filespec.read()
        return '%s' % data
        
    #------------------------------------------------------------
    def rootWindow(self):
        window = None
        if (QApplication.instance()):
            window = QApplication.instance().activeWindow()

            # grab the root window
            if (window):
                while (window.parent()):
                    window = window.parent()

        return window
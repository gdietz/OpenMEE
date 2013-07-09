from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import sys

import ui_main_window
import ee_model


class MainForm(QtGui.QMainWindow, ui_main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi(self)
        
        self.model = ee_model.EETableModel()
        self.tableView.setModel(self.model)
        
        self.statusBar().showMessage(QString("This is a test message"), 1000)
        
        #self.show()

        self._setup_connections()

    def _setup_connections(self):
        #self.connect(header, SIGNAL("sectionClicked(int)"),
        #                 self.sortTable)
        #self.connect(addShipButton, SIGNAL("clicked()"), self.addShip)
        #self.connect(removeShipButton, SIGNAL("clicked()"),
        #             self.removeShip)
        #self.connect(quitButton, SIGNAL("clicked()"), self.accept)
        pass
        
        
        
        
if __name__ == '__main__':
    #pass        
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()
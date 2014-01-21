from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

# simple progress bar
import ui_running
class MetaProgress(QDialog, ui_running.Ui_running):
    
    def __init__(self, msg=None, parent=None):
        super(MetaProgress, self).__init__(parent)
        self.setupUi(self)
        
        if msg:
            self.label.setText(msg)
            
    def setText(self, msg):
        self.label.setText(msg)
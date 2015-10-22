from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

class MyTableView(QTableView):
    def keyPressEvent(self, event):
        backspace_or_delete = event.key() in [Qt.Key_Backspace, Qt.Key_Delete]
        if (backspace_or_delete and self.state() != QAbstractItemView.EditingState):
        	self.model().clearIndex(self.currentIndex())
        QTableView.keyPressEvent(self, event)
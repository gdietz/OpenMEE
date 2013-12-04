import sys

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_scrollable_infobox

class ScrollableInfoBox(QtGui.QDialog, ui_scrollable_infobox.Ui_Dialog):
    def __init__(self, windowtitle="ScrollableInfoBox", main_label="Teacup, short, stout", content="\n".join([str(x) for x in range(30)]), parent=None):
        super(ScrollableInfoBox, self).__init__(parent)
        self.setupUi(self)
        
        self.set_window_title(windowtitle)
        self.set_main_label(main_label)
        self.set_content(content)
        
    def set_window_title(self, title):
        self.setWindowTitle(title)
        
    def set_content(self, text):
        self.content.setPlainText(text)
        
    def set_main_label(self, label):
        self.main_label.setText(label)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ScrollableInfoBox()
    form.show()
    form.raise_()
    app.exec_()
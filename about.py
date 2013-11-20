import os

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_about

class About(QDialog, ui_about.Ui_Dialog):
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
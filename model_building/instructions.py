from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_instructions

class InstructionsPage(QWizardPage, ui_instructions.Ui_WizardPage):
    def __init__(self, parent=None):
        super(InstructionsPage, self).__init__(parent)
        self.setupUi(self)
        
    def __str__(self):
        return ""
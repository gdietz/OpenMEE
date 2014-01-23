from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *
import ui_summary_page

class SummaryPage(QWizardPage, ui_summary_page.Ui_WizardPage):
    def __init__(self, parent=None):
        super(SummaryPage, self).__init__(parent)
        self.setupUi(self)
        
    def initializePage(self):
        self.plainTextEdit.clear()
        self.plainTextEdit.insertPlainText(self.wizard().get_summary())
        
    def save_selections(self):
        return self.save_selections_checkBox.isChecked()
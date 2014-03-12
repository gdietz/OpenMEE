'''
Created on Mar 11, 2014

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_mice_output_page

class MiceOutputPage(QWizardPage, ui_mice_output_page.Ui_WizardPage):
    def __init__(self, parent=None): # todo: set defaults of previous parameters to None
        super(MiceOutputPage, self).__init__(parent)
        self.setupUi(self)
        
    def initializePage(self):
        # Run Mice, collect output
        
        self.wizard()._run_imputation()
        summary = self.wizard().get_imputation_summary()
        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText(summary)
        
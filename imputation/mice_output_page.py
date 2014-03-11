'''
Created on Mar 11, 2014

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_mice_output_page
import python_to_R

class MiceOutputPage(QWizardPage, ui_mice_output_page.Ui_WizardPage):
    def __init__(self, parent=None): # todo: set defaults of previous parameters to None
        super(MiceOutputPage, self).__init__(parent)
        self.setupUi(self)
        
    def initializePage(self):
        # Run Mice, collect output
        
        self.imputation_results = self.wizard()._run_imputation()
        summary = self._get_imputation_summary()
        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText(summary)
        
    def _get_imputation_summary(self):
        return self.imputation_results['summary']
        
    def get_imputation_choices(self):
        covariates = self.wizard().get_included_covariates() # covariates in original order
        
        imputation_choices = python_to_R.imputation_dataframes_to_pylist_of_ordered_dicts(self.imputation_results['imputations'], covariates)
        
        return imputation_choices
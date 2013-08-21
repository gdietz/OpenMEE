from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *

import python_to_R
import ui_select_covariates_page

class SelectCovariatesPage(QWizardPage, ui_select_covariates_page.Ui_WizardPage):
    def __init__(self, model, parent=None):
        super(SelectCovariatesPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        

        #self.covariate_listWidget
        
        self.items_to_covariates = {}
        self.covariate_include_status = {}
        self.init_covariate_include_status()
        self._populate_covariate_list()
        
        
        self.covariate_listWidget.itemChanged.connect(self.update_covariate_include_status)
    
    def init_covariate_include_status(self):
        continuous_covariates = self._get_sorted_continuous_covariates()
        categorical_covariates = self._get_sorted_categorical_covariates()
        covariates = continuous_covariates+categorical_covariates
        self.covariate_include_status = dict([(cov, False) for cov in covariates])
        
    def update_covariate_include_status(self, item):
        covariate = self.items_to_covariates[item]
        state = item.checkState()
        
        if state == Qt.Checked: 
            self.covariate_include_status[covariate] = True
        elif state == Qt.Unchecked:
            self.covariate_include_status[covariate] = False
        
        self.completeChanged.emit()
        
        
    def isComplete(self):
        if any(self.covariate_include_status.values()):
            return True
        return False
    
    
    def initializePage(self):
        self.wizard().covariates_included_table = self.covariate_include_status
        self.wizard().using_fixed_effects = self.fixed_effects_radio_btn.isChecked
        
        
    def _get_sorted_continuous_covariates(self):
        continuous_covariates = self.model.get_variables(CONTINUOUS)
        continuous_covariates.sort(key=lambda cov_var: cov_var.get_label().lower())
        return continuous_covariates
    
    def _get_sorted_categorical_covariates(self):
        categorical_covariates = self.model.get_variables(CATEGORICAL)
        categorical_covariates.sort(key=lambda cov_var: cov_var.get_label().lower())
        return categorical_covariates
        
    def _populate_covariate_list(self):
        ''' Adds checkable list of covariates'''
        
        self.covariate_listWidget.blockSignals(True)
        self.covariate_listWidget.clear()
        
        # get and sort lists of possible continuous and categoical covariates
        continuous_covariates = self._get_sorted_continuous_covariates()
        categorical_covariates = self._get_sorted_categorical_covariates()
        
        def add_list_of_covariates(covariates, suffix = ""):
            for cov in covariates:
                label = cov.get_label()
                if label is None:
                    label = ""
                label += " "+suffix
                
                item = QListWidgetItem(label)
                self.items_to_covariates[item] = cov
                item.setCheckState(Qt.Unchecked)
                item.setFlags(item.flags()|Qt.ItemIsUserCheckable)
                self.covariate_listWidget.addItem(item)
        
        add_list_of_covariates(continuous_covariates, suffix="(continuous)")
        add_list_of_covariates(categorical_covariates, suffix="(categorical)")
        
        
        
        self.covariate_listWidget.blockSignals(False)
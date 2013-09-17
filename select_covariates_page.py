##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

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
        
        
        
        self.covariate_listWidget.itemChanged.connect(self.update_covariate_include_status)
        self.conf_level_spinbox.valueChanged[float].connect(self.update_conf_level)
    
    def init_covariate_include_status(self):
        continuous_covariates = self._get_sorted_continuous_covariates()
        categorical_covariates = self._get_sorted_categorical_covariates()
        covariates = continuous_covariates+categorical_covariates
        self.covariate_include_status = dict([(cov, False) for cov in covariates])
        
    def update_conf_level(self, new_conf_level):
        self.conf_level = new_conf_level
        print("New conf level is %s" % str(new_conf_level))
        
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
    
    def get_confidence_level(self):
        return self.conf_level
    
    
    def initializePage(self):
        self.items_to_covariates = {}
        self.covariate_include_status = {}
        self.init_covariate_include_status()
        
        self._populate_covariate_list()
        self.update_conf_level(DEFAULT_CONFIDENCE_LEVEL)
        
        self.wizard().covariates_included_table = self.covariate_include_status
        self.wizard().using_fixed_effects = self.fixed_effects_radio_btn.isChecked
        self.wizard().get_confidence_level = self.get_confidence_level
        
    def _get_sorted_continuous_covariates(self):
        continuous_covariates = self.model.get_variables(CONTINUOUS)
        continuous_covariates.sort(key=lambda cov_var: cov_var.get_label().lower())
        return continuous_covariates
    
    def _get_sorted_categorical_covariates(self):
        categorical_covariates = self.model.get_variables(CATEGORICAL)
        categorical_covariates.sort(key=lambda cov_var: cov_var.get_label().lower())
        return categorical_covariates
    
    def _get_sorted_count_covariates(self):
        count_covariates = self.model.get_variables(COUNT)
        count_covariates.sort(key=lambda cov_var: cov_var.get_label().lower())
        return count_covariates
        
    def _populate_covariate_list(self):
        ''' Adds checkable list of covariates'''
        
        self.covariate_listWidget.blockSignals(True)
        self.covariate_listWidget.clear()
        
        # get and sort lists of possible continuous and categoical covariates
        continuous_covariates = self._get_sorted_continuous_covariates()
        categorical_covariates = self._get_sorted_categorical_covariates()
        count_covariates = self._get_sorted_count_covariates()
        
        included_studies = self.wizard().get_included_studies_in_proper_order()
        
        
        def add_list_of_covariates(covariates, suffix = ""):
            for cov in covariates:
                # included studies have values for this covariate
                covariate_valid = self.covariate_valid_given_included_studies(included_studies, cov)
                
                label = cov.get_label()
                if label is None:
                    label = ""
                label += " "+suffix
                if not covariate_valid:
                    label += " MISSING VALUES EXIST FOR INCLUDED STUDIES"
                item = QListWidgetItem(label)
                self.items_to_covariates[item] = cov
                if covariate_valid:
                    item.setCheckState(Qt.Unchecked)
                    item.setFlags(item.flags()|Qt.ItemIsUserCheckable)
                else:
                    item.setCheckState(Qt.Unchecked)
                    item.setFlags(Qt.ItemIsSelectable)
                self.covariate_listWidget.addItem(item)
        
        add_list_of_covariates(continuous_covariates, suffix="(continuous)")
        add_list_of_covariates(categorical_covariates, suffix="(categorical)")
        add_list_of_covariates(count_covariates, suffix="(count)")
        
        
        
        self.covariate_listWidget.blockSignals(False)
        
    def covariate_valid_given_included_studies(self, included_studies, covariate):
        value_is_empty = lambda val: val==None or str(val)==""
        for study in included_studies:
            if value_is_empty(study.get_var(covariate)):
                return False
        return True
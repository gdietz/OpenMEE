##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

import python_to_R
import ui_select_covariates_page

class SelectCovariatesPage(QWizardPage, ui_select_covariates_page.Ui_WizardPage):
    def __init__(self, model, prev_conf_level, using_fixed_effects, mode=None, parent=None): # todo: set defaults of previous parameters to None
        super(SelectCovariatesPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.mode = mode
    
        # default values from previous analysis
        self.default_conf_level = prev_conf_level
        self.default_fixed_effects = using_fixed_effects
        if self.default_conf_level is not None: 
            self.conf_level_spinbox.setValue(self.default_conf_level)
        if self.default_fixed_effects is not None:
            if self.default_fixed_effects is True:
                self.fixed_effects_radio_btn.setChecked(True)
            else:
                self.random_effects_radio_btn.setChecked(True)
        
        self.covariate_listWidget.itemChanged.connect(self.update_covariate_include_status)
        self.conf_level_spinbox.valueChanged[float].connect(self.update_conf_level)
        
        
    
    def init_covariate_include_status(self):
        continuous_covariates = self.model.get_sorted_continuous_covariates()
        categorical_covariates = self.model.get_sorted_categorical_covariates()
        count_covariates = self.model.get_sorted_count_covariates()
        covariates = count_covariates + continuous_covariates+categorical_covariates
        self.covariate_include_status = dict([(cov, False) for cov in covariates])
        
        # Load previously included covariates (from last analysis) from the ee_model 
        included_studies = self.wizard().get_included_studies_in_proper_order()
        previously_included_covariates = self.model.get_previously_included_covariates()
        if previously_included_covariates is not None:
            for cov in previously_included_covariates:
                if cov in self.covariate_include_status.keys() and self.covariate_valid_given_included_studies(included_studies, cov):
                    self.covariate_include_status[cov]=True
        
        
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
        if self.mode in [META_REG_COND_MEANS, BOOTSTRAP_META_REG_COND_MEANS]:
            # Have to have at least a categorical covariate
            included_covs = [cov for cov,status in self.covariate_include_status.iteritems() if status]
            if any([cov.get_type()==CATEGORICAL for cov in included_covs]):
                return True
        else: 
            if any(self.covariate_include_status.values()):
                return True
        return False
    
    def get_confidence_level(self):
        return self.conf_level
    
    def initializePage(self):
        print("Initializing select covariates page")
        self.covariate_include_status = {}
        self.init_covariate_include_status()
        
        self.items_to_covariates = {}
        self._populate_covariate_list()
        self.update_conf_level(DEFAULT_CONFIDENCE_LEVEL)
        
    def _populate_covariate_list(self):
        ''' Adds checkable list of covariates'''
        
        self.covariate_listWidget.blockSignals(True)
        self.covariate_listWidget.clear()
        
        # get and sort lists of possible continuous and categoical covariates
        continuous_covariates = self.model.get_sorted_continuous_covariates()
        categorical_covariates = self.model.get_sorted_categorical_covariates()
        count_covariates = self.model.get_sorted_count_covariates()
        
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
                    #item.setCheckState(Qt.Unchecked)
                    included = self.covariate_include_status[cov]
                    item.setCheckState(Qt.Checked if included else Qt.Unchecked)
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
    
    def get_parameters(self):
        ''' main getter function to interact with the selections made on this page'''
          
        return {'included_covariates': self.get_included_covariates(),
                'using_fixed_effects': self.fixed_effects_radio_btn.isChecked(),
                'conf_level': self.get_confidence_level(),
                }
        
    def get_included_covariates(self):
        included_covariates = [cov for cov,should_include in self.covariate_include_status.items() if should_include]
        return included_covariates
    def get_using_fixed_effects(self):
        return self.fixed_effects_radio_btn.isChecked()
    def get_covpage_conf_level(self):
        return self.get_confidence_level()
        
        

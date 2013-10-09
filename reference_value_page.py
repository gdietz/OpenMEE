##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *

import ui_reference_value_page

class ReferenceValuePage(QWizardPage, ui_reference_value_page.Ui_WizardPage):
    def __init__(self, parent=None):
        super(ReferenceValuePage, self).__init__(parent)
        self.setupUi(self)
        
    def initializePage(self):
        print("Initialize Page called")
        
        # Clear list widgets
        self.cov_listWidget.blockSignals(True)
        self.val_listWidget.blockSignals(True)
        self.cov_listWidget.clear()
        self.val_listWidget.clear()
        self.cov_listWidget.blockSignals(True)
        self.val_listWidget.blockSignals(True)
        
        included_covariates = self.wizard().get_included_covariates()
        self.categorical_covariates = [cov for cov in included_covariates if cov.get_type()==CATEGORICAL]
        self.included_studies = self.wizard().get_included_studies_in_proper_order()\
        
        # store our choices here
        self.cov_to_ref_level = {}
        
        # mapping cov --> set of levels
        self.cov_to_levels = self._make_cov_to_levels_dict()
        
        # initialize cov_to_ref_level from previous selection
        self.default_cov_to_ref_level = self.model.get_cov_2_ref_values_selection()
        if self.default_cov_to_ref_level is not None:
            for cov in included_covariates:
                if cov in self.default_cov_to_ref_level and self.default_cov_to_ref_level[cov] in self.cov_to_levels[cov]:
                    self.cov_to_ref_level[cov] = self.default_cov_to_ref_level[cov]
        
        # mapping listWidget items to covariates/labels
        self.left_listWidgetItem_to_cov = {}
        self.right_listWidgetItem_to_level = {}
        self.current_cov = None
        
        # connect signals
        self.cov_listWidget.currentItemChanged.connect(self.left_list_item_changed)
        self.val_listWidget.currentItemChanged.connect(self.right_list_item_changed)
        
        
        self._populate_left_list(self.categorical_covariates)
    
        
        
        
    def cleanupPage(self):
        QWizardPage.cleanupPage(self)
        print("Cleaning up")
        # reset everything
        self._reset_everything()
        
        
    def _reset_everything(self):
        # Clear list widgets
        self.cov_listWidget.blockSignals(True)
        self.val_listWidget.blockSignals(True)
        self.cov_listWidget.clear()
        self.val_listWidget.clear()
        self.cov_listWidget.blockSignals(True)
        self.val_listWidget.blockSignals(True)
    
        # store our choices here
        self.cov_to_ref_level = {}
        # mapping cov --> set of levels
        self.cov_to_levels = {}
        
        # mapping listWidget items to covariates/labels
        self.left_listWidgetItem_to_cov = {}
        self.right_listWidgetItem_to_level = {}
        self.current_cov = None
        
        
    def left_list_item_changed(self, current_item, previous_item):
        self.current_cov = self.left_listWidgetItem_to_cov[current_item]
        
        self._populate_right_list(self.cov_to_levels[self.current_cov])
    
    def right_list_item_changed(self, current_item, previous_item):
        ref_level = self.right_listWidgetItem_to_level[current_item]
        self.cov_to_ref_level[self.current_cov] = ref_level
        self.wizard().cov_2_ref_values = self.cov_to_ref_level
        print("For covariate: %s, reference is now: %s" % (self.current_cov.get_label(), ref_level))
    
    def get_covariate_reference_levels(self):
        return self.cov_to_ref_level
    
    def _populate_left_list(self, covariates):
        self.cov_listWidget.blockSignals(True)
        self.cov_listWidget.clear()
        self.left_listWidgetItem_to_cov = {}
        for cov in self.categorical_covariates:
            item = QListWidgetItem(cov.get_label())
            self.cov_listWidget.addItem(item)
            self.left_listWidgetItem_to_cov[item]=cov
            
        if self.cov_listWidget.count() > 0:
            self.cov_listWidget.setCurrentItem(self.cov_listWidget.item(0))
            default_cov = self.left_listWidgetItem_to_cov[self.cov_listWidget.item(0)]
            self.current_cov = default_cov
            self._populate_right_list(self.cov_to_levels[default_cov])
        self.cov_listWidget.blockSignals(False)
        
    def _populate_right_list(self, levels):
        self.val_listWidget.blockSignals(True)
        self.val_listWidget.clear()
        self.right_listWidgetItem_to_level = {}
        level_to_item = {}
        for level in levels:
            item = QListWidgetItem(level)
            self.val_listWidget.addItem(item)
            self.right_listWidgetItem_to_level[item]=level
            level_to_item[level]=item
        # set already chosen level
        if self.current_cov in self.cov_to_ref_level:
            current_ref_level = self.cov_to_ref_level[self.current_cov]
            self.val_listWidget.setCurrentItem(level_to_item[current_ref_level])
        self.val_listWidget.blockSignals(False)
        
    def _make_cov_to_levels_dict(self):
        # makes set of possible levels for each covariate
        cov_to_levels = {}
        for cov in self.categorical_covariates:
            levels = set()
            for study in self.included_studies:
                val = study.get_var(cov)
                if val is not None and val is not "":
                    levels.add(val)
                    if cov not in self.cov_to_ref_level: # set defaults
                        self.cov_to_ref_level[cov]=val
            cov_to_levels[cov]=levels
        self.wizard().cov_2_ref_values = self.cov_to_ref_level
        return cov_to_levels   
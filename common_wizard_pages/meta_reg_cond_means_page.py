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
import ui_meta_reg_cond_means_page

class CondMeansPage(QWizardPage, ui_meta_reg_cond_means_page.Ui_WizardPage):
    def __init__(self, model, parent=None):
        super(CondMeansPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.cov_value_settings = {}

        # map cov --> values set by user
        self.default_selected_cov, self.default_cov_value_settings = self.model.get_previous_selected_cov_and_covs_to_values()
        self.selected_cov = self.default_selected_cov # will be overwritten if invalid

        
        self.choose_cov_comboBox.currentIndexChanged.connect(self._update_selected_cov_for_stratification)
        self.cat_listWidget.currentItemChanged.connect(self._cat_listWidgetItemChanged)
        self.cont_listWidget.currentItemChanged.connect(self._cont_listWidgetItemChanged)
        self.cont_le.textChanged.connect(self._update_cont_cov_level)
        self.cat_cbo_box.currentIndexChanged['int'].connect(self._update_cat_cov_level)
        
        
    def initializePage(self):
        included_covariates = self.wizard().get_included_covariates()
        self.continuous_covariates = self._get_sorted_covariates_of_type(included_covariates, [CONTINUOUS, COUNT])
        self.categorical_covariates = self._get_sorted_covariates_of_type(included_covariates, [CATEGORICAL,])
        
        self.included_studies = self.wizard().get_included_studies_in_proper_order()
        
        # initialize cov value settings from previous analysis if any
        
        if self.default_cov_value_settings:
            for cov, value in self.default_cov_value_settings.iteritems():
                cov_type = cov.get_type()
                if cov not in included_covariates:
                    continue
                if cov_type in [CONTINUOUS,COUNT]:
                    self.cov_value_settings[cov]=value
                elif cov_type == CATEGORICAL:
                    if value in self._get_cov_levels(cov):
                        self.cov_value_settings[cov]=value
            
        
        # assign arbitrary ids to covariates
        self.cov_id_to_cov = dict(enumerate(included_covariates))
        self.cov_to_cov_id = dict([(v,k) for k,v in self.cov_id_to_cov.items()])
        self._populate_choose_covariate_combo_box(self.categorical_covariates)
        
    def _populate_choose_covariate_combo_box(self, categorical_covariates):
        self._block_widget_signals(True)
        self.choose_cov_comboBox.clear()
        
        for cov in categorical_covariates:
            self.choose_cov_comboBox.addItem(cov.get_label(), self.cov_to_cov_id[cov])
            
        if self.selected_cov in categorical_covariates: # if we are provided with the selected covariate from a previous analysis
            self.choose_cov_comboBox.setCurrentIndex(self.choose_cov_comboBox.findData(self.cov_to_cov_id[self.selected_cov]))
        else:
            self.choose_cov_comboBox.setCurrentIndex(0)
        self._block_widget_signals(False)
        
        selected_cov = self._update_selected_cov_for_stratification()
        
    def _update_selected_cov_for_stratification(self):
        current_index = self.choose_cov_comboBox.currentIndex()
        cov_id = self.choose_cov_comboBox.itemData(current_index).toInt()[0]
        #pyqtRemoveInputHook()
        #import pdb; pdb.set_trace()
        self.selected_cov = self.cov_id_to_cov[cov_id]
        
        self.item_2_cov = {}
        
        # clear combo box and linedit:
        self._block_widget_signals(True)
        self.cont_le.setText("")
        self.cat_cbo_box.clear()
        self._block_widget_signals(False)
        
        self._populate_listwidget(self.cont_listWidget, self.continuous_covariates)
        self._populate_listwidget(self.cat_listWidget, [cov for cov in self.categorical_covariates if cov != self.selected_cov])
        
        return cov
        
    def _populate_listwidget(self, list_widget, covariates):
        self._block_widget_signals(True)
        
        list_widget.clear()
        
        
        for cov in covariates:
            item = QListWidgetItem(cov.get_label())
            self.item_2_cov[item] = cov
            list_widget.addItem(item)
        self._block_widget_signals(False)
        
    def _cont_listWidgetItemChanged(self, current_item, previous_item):
        cov = self.item_2_cov[current_item]
        if cov in self.cov_value_settings:
            self.cont_le.setText(str(self.cov_value_settings[cov]))
        else:
            self.cont_le.setText("")
    
    def _cat_listWidgetItemChanged(self, current_item, previous_item):
        cov = self.item_2_cov[current_item]
        
        self.cat_cbo_box.blockSignals(True)
        self.cat_cbo_box.clear()
        
        levels = self._get_cov_levels(cov)
        #print("Levels: %s" % str(levels))
        for level in levels:
            self.cat_cbo_box.addItem(str(level), level)
        # If we already have a level, set the combo box to this level
        set_default = True # default set if we don't have a valid level
        if cov in self.cov_value_settings:
            chosen_level = self.cov_value_settings[cov]
            if chosen_level in levels:
                self.cat_cbo_box.setCurrentIndex(self.cat_cbo_box.findData(chosen_level))
                set_default = False
            else:
                del self.cov_value_settings[cov]

        if set_default:
            if self.cat_cbo_box.count() > 0:
                self.cat_cbo_box.setCurrentIndex(0)
                self._update_cat_cov_level(0)
        self.cat_cbo_box.blockSignals(False)
    
    def _update_cat_cov_level(self, index):
        cov_item = self.cat_listWidget.currentItem()
        cov = self.item_2_cov[cov_item]
        level = str(self.cat_cbo_box.itemData(index).toString())
        self.cov_value_settings[cov] = level
        #self.print_covariate_values()##
        
        self.completeChanged.emit()
        
    def _update_cont_cov_level(self):
        cov_item = self.cont_listWidget.currentItem()
        cov = self.item_2_cov[cov_item]
        txt = str(self.cont_le.text())
        try:
            if txt != "":
                num = float(txt)
            else:
                if cov in self.cov_value_settings:
                    del self.cov_value_settings[cov]
                return
        except ValueError:
            QMessageBox.warning(self, "Invalid Number", "'%s' is not a valid number." % txt)
            return
        self.cov_value_settings[cov] = num
        #self.print_covariate_values()##
        
        self.completeChanged.emit()
    
    def print_covariate_values(self):
        print("Covariate values: %s" % str(self.cov_value_settings))
        for cov, value in self.cov_value_settings.items():
            print("%s: %s" % (cov.get_label(), str(value)))
        
    def _get_cov_levels(self, cov):
        levels = set([study.get_var(cov) for study in self.included_studies])
        levels = sorted(list(levels))
        return levels
        
        
    def isComplete(self):
        other_cat_covs = [cov for cov in self.categorical_covariates if cov != self.selected_cov]
        all_covs = other_cat_covs + self.continuous_covariates
        # must have values for all the necessary covariates
        for cov in all_covs:
            if cov not in self.cov_value_settings:
                return False
            if self.cov_value_settings[cov] is None:
                return False
        return True
                    
        
        
    def _block_widget_signals(self, state):
        widgets = [self.choose_cov_comboBox, self.cont_listWidget,
                   self.cat_listWidget, self.cat_cbo_box, self.cont_le]
        for widget in widgets:
            widget.blockSignals(state)
            
    def _get_sorted_covariates_of_type(self, covariates, cov_types):
        wanted_covariates = [cov for cov in covariates if cov.get_type() in cov_types]
        return sorted(wanted_covariates, key = lambda cov: cov.get_label().lower())
    
    ########## getter ########################################################
    
    def get_meta_reg_cond_means_data(self):
        if self.selected_cov in self.cov_value_settings:
            del self.cov_value_settings[self.selected_cov]
        return (self.selected_cov, self.cov_value_settings)
    
    #########################################################################
    
    def __str__(self):
        selected_cov, cov_value_settings = self.get_meta_reg_cond_means_data()
        cov_vals_strs = []
        for cov in sorted(cov_value_settings.keys()):
            cov_vals_strs.append("    %s: %s\n" % (cov.get_label(), str(cov_value_settings[cov])))
        cov_vals_str = "\n".join(cov_vals_strs)
        summary = "Conditional Means:\n" + "  Selected Covariate: %s\n" % selected_cov.get_label() + "  Values for other covariates:\n%s" % cov_vals_str
        return summary
    

    
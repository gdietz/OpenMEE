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
    def __init__(self, model,
                 previously_included_covs = [],
                 fixed_effects=True,
                 conf_level=95,
                 random_effects_method = "DL",
                 need_categorical = False, # need at least one categorical variable?
                 parent=None): # todo: set defaults of previous parameters to None
        super(SelectCovariatesPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.need_categorical = need_categorical
        
        ### Set values from previous analysis ###
        self.setup_values_from_previous_analysis(
            conf_level=conf_level,
            random_effects_method=random_effects_method,
            fixed_effects = fixed_effects,
            prev_covs=previously_included_covs)
        
        # Setup connections
        self.setup_connections()
        
    def setup_connections(self):
        # adding and removing covariates
        self.add_all_pushbutton.clicked.connect(self.add_all_covs)
        self.remove_all_pushButton.clicked.connect(self.remove_all_covs)
        # lambdas since 'clicked' signal sends along an unwanted bool
        self.add_pushbutton.clicked.connect(lambda: self.add_one_cov())
        self.remove_pushButton.clicked.connect(lambda: self.remove_one_cov())
        self.available_covs_listWidget.itemDoubleClicked.connect(self.add_one_cov)
        self.selected_covs_listWidget.itemDoubleClicked.connect(self.remove_one_cov)
        
        # radio buttons
        self.fixed_effects_radio_btn.clicked.connect(self.choose_fixed_effects)
        self.random_effects_radio_btn.clicked.connect(self.choose_random_effects)
        
    def setup_values_from_previous_analysis(self,
                                            conf_level,
                                            random_effects_method,
                                            fixed_effects, prev_covs):
        ### Set values from previous analysis ###
        if conf_level:
            self.conf_level_spinbox.setValue(conf_level)
        
        # populate random effects combobox
        self.add_random_effect_methods_to_combo_box(default_method=random_effects_method)
        
        # Using random effects or fixed effects?
        if fixed_effects:
            self.choose_fixed_effects()
            self.fixed_effects_radio_btn.setChecked(True)
        else:
            self.choose_random_effects()
            self.random_effects_radio_btn.setChecked(True)
        
        if prev_covs:
            self.prev_covs = prev_covs
        else:
            self.prev_covs = []
    
    
    def choose_fixed_effects(self):
        self.random_effects_method_GroupBox.setEnabled(False)
    def choose_random_effects(self):
        self.random_effects_method_GroupBox.setEnabled(True)
    
    def add_random_effect_methods_to_combo_box(self, default_method):
        self.random_effects_method_ComboBox.clear()
        
        for short_name, pretty_name in RANDOM_EFFECTS_METHODS_TO_PRETTY_STRS.items():
            self.random_effects_method_ComboBox.addItem(
                        pretty_name,
                        userData=QVariant(short_name))
        if default_method:
            idx = self.random_effects_method_ComboBox.findData(QVariant(default_method))
            self.random_effects_method_ComboBox.setCurrentIndex(idx)
    
    def initializePage(self):
        self.init_covariates_lists()
 
        # make mapping of covariates to list_items and visa-versa
        self.cov_to_item = {}
        self.item_to_cov = {}
        self.make_items_for_covs(self.available_covariates
                                 +self.selected_covariates
                                 +self.unavailable_covariates)
        
        # populate the 3 list widgets with items
        self.populate_listWidget(self.available_covs_listWidget, self.available_covariates)
        self.populate_listWidget(self.selected_covs_listWidget, self.selected_covariates)
        self.populate_listWidget(self.unavailable_covs_listWidget, self.unavailable_covariates, enabled=False)
        
    def init_covariates_lists(self):
        self.available_covariates = []
        self.selected_covariates = []
        self.unavailable_covariates = {} # cov --> reason why unavailable
        
        included_studies = self.wizard().get_included_studies_in_proper_order()
        valid_and_invalid_covariates = self.model.get_variables_with_data(studies=included_studies)
        self.available_covariates = valid_and_invalid_covariates['valid']
        self.unavailable_covariates = valid_and_invalid_covariates['invalid']
        
        # move previously included covariates to the selected_covariates list
        # if they still exist in the model and are valid given the study selections
        for cov in self.prev_covs:
            if cov in self.available_covariates:
                self.move_cov(cov, self.available_covariates, self.selected_covariates)
        
        # sort the lists
        sort_by_label = lambda var: var.get_label()
        self.available_covariates.sort(key=sort_by_label)
        self.unavailable_covariates.sort(key=sort_by_label)
        self.selected_covariates.sort(key=sort_by_label)
        
    def make_items_for_covs(self, cov_list):
        ''' Makes an QListWidgetItem for each cov and stores it in a dictionary
        mapping cov --> item '''
        
        for cov in cov_list:
            item = QListWidgetItem(cov.get_label())
            self.cov_to_item[cov] = item
            self.item_to_cov[item]=cov
    
                
    def move_cov(self, cov, source_list, target_list):
        ''' moves cov from source_list to target_list '''
        
        target_list.append(cov)
        source_list.remove(cov)
    
    def move_item(self, item, source, target):
        ''' move an item from one list widget and stick it on the end of
        another list widget '''
        
        source_row = source.row(item)
        # remove item from source_listWidget
        source.takeItem(source_row)
        # add to target_listWidget
        target.addItem(item)
                
    def populate_listWidget(self, list_widget, cov_list, selectable=True, enabled=True):
        ''' Adds the items corresponding the covariates in cov_list to the
        list_widget, sets selectable flag of items '''
        
        # build flags
        flags = Qt.ItemIsEnabled if enabled else ~Qt.ItemIsEnabled
        flags = flags|(Qt.ItemIsSelectable if selectable else ~Qt.ItemIsSelectable)
        
        
        list_widget.clear()
        for cov in cov_list:
            item = self.cov_to_item[cov]
            item.setFlags(flags)
            list_widget.addItem(item)
            
            
    def add_one_cov(self, item=None, emit_change_signal=True):
        '''
        1. Moves item from the available_listWidget to the
        selected_listWidget
        2. Updates internal 'available' list and 'selected' lists '''
        
        # if item is None, we select the current item
        if item is None:
            item = self.available_covs_listWidget.currentItem()
        
        
        
        cov = self.item_to_cov[item]
        print("adding covariate: %s" % cov.get_label())
        
        self.move_item(item, self.available_covs_listWidget, self.selected_covs_listWidget)
        self.move_cov(cov, self.available_covariates, self.selected_covariates)
    
        if emit_change_signal:
            self.completeChanged.emit()
        
    def remove_one_cov(self, item, emit_change_signal=True):
        ''' 1) Moves item from the selected_listWidget to the available_listWidget
            2) updates internal 'available' list and 'selected' lists '''

        # item is none we select the current item
        if item is None:
            item = self.selected_covs_listWidget.currentItem()
        
        cov = self.item_to_cov[item]
        self.move_item(item, self.selected_covs_listWidget, self.available_covs_listWidget)
        self.move_cov(cov, self.selected_covariates, self.available_covariates)

        if emit_change_signal:
            self.completeChanged.emit() 

        
    def add_all_covs(self):
        ''' 1) Moves all items from the available_listWidget to the
        selected_listWidget
            2) Move corresponding entries in internal list accordingly'''
    
        # start from the top and work down until the list is empty
        while self.available_covs_listWidget.count() > 0:
            item = self.available_covs_listWidget.item(0)
            self.add_one_cov(item, emit_change_signal=False)
        
        self.completeChanged.emit()
        
    def remove_all_covs(self):
        ''' 1) Moves all items from the selected_listWidget to the
        available_listWidget
        2) Move corresponding entries from selected_covs list to available_covs
        '''
        
        while self.selected_covs_listWidget.count() > 0:
            item = self.selected_covs_listWidget.item(0)
            self.remove_one_cov(item, emit_change_signal=False)
        
        self.completeChanged.emit()
        
                   
    def isComplete(self):
        if self.need_categorical:
            # is there at least one categorical variable selected?
            select_cov_types = (cov.get_type()==CATEGORICAL for cov in self.selected_covariates)
            return any(select_cov_types)
        else:
            # is at least one covariate selected?
            return len(self.selected_covariates) > 0
                
        
    ############################################################
    
    def get_parameters(self):
        ''' main getter function to interact with the selections made on this page'''
          
        return {'included_covariates': self.get_included_covariates(),
                'fixed_effects': self.fixed_effects_radio_btn.isChecked(),
                'conf_level': self.get_confidence_level(),
                'random_effects_method': self.get_random_effects_method(),
                }
    
    def get_confidence_level(self):
        return self.conf_level_spinbox.value()    
    def get_included_covariates(self):
        return self.selected_covariates
    def get_using_fixed_effects(self):
        return self.fixed_effects_radio_btn.isChecked()
    def get_random_effects_method(self):
        current_index = self.random_effects_method_ComboBox.currentIndex()
        current_data = self.random_effects_method_ComboBox.itemData(current_index)
        method = str(current_data.toString())
        return method
        

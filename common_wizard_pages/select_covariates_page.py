##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

import itertools

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *
from interaction import Interaction
from add_interaction_dlg import AddInteractionDlg

import ui_select_covariates_page

class SelectCovariatesPage(QWizardPage, ui_select_covariates_page.Ui_WizardPage):
    
    covariateAdded = pyqtSignal()
    covariateRemoved = pyqtSignal()
    interactionAdded = pyqtSignal()
    interactionRemoved = pyqtSignal()
    
    def __init__(self, model,
                 previously_included_covs = [],
                 min_covariates=1, # minimum # of covariates requires
                 allow_covs_with_missing_data=False,
                 disable_require_categorical=False,
                 parent=None): # todo: set defaults of previous parameters to None
        super(SelectCovariatesPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.min_covariates = min_covariates
        self.allow_covs_with_missing_data = allow_covs_with_missing_data
        self.disable_require_categorical = disable_require_categorical
        
        if allow_covs_with_missing_data:
            self.unavailable_covs_groupbox.hide()
        
        self.interactions = []
        self.item_to_interaction = {}
        
        ### Set values from previous analysis ###
        self.setup_values_from_previous_analysis(
            prev_covs=previously_included_covs)
        
        # Setup connections
        self.setup_connections()
        
    def add_interaction_clicked(self):
        dlg = AddInteractionDlg(covariates=self.selected_covariates,
                                existing_interactions=self.interactions,
                                possible_interactions=self._get_possible_interactions(self.selected_covariates))
        if dlg.exec_():
            interaction = dlg.get_interaction()
            
            # create item and add to interactions
            item = QListWidgetItem(str(interaction))
            self.interactions_listWidget.addItem(item)
            self.item_to_interaction[item] = interaction
            self.interactions.append(interaction)
            
            # interaction was added
            self.interactionAdded.emit()
    
    def remove_interaction_clicked(self):
        # Identify interaction and item
        item = self.interactions_listWidget.currentItem()
        item_row = self.interactions_listWidget.row(item)
        interaction = self.item_to_interaction[item]
        
        # Remove interaction and item
        self.interactions_listWidget.takeItem(item_row)
        del self.item_to_interaction[item]
        self.interactions.remove(interaction)
        
        # interaction was removed
        self.interactionRemoved.emit()

    def toggle_covariate_buttons_enabled_status(self):
        # Change the enabled status of the buttons for adding/removing
        # according to whether there are covariates to add/remove
        num_included_covariates = len(self.selected_covariates)
        num_available_covariates = len(self.available_covariates)

        enable_add_buttons = True
        if num_available_covariates == 0:
            enable_add_buttons = False

        enable_remove_buttons = True
        if num_included_covariates == 0:
            enable_remove_buttons = False

        self.add_pushbutton.setEnabled(enable_add_buttons)
        self.add_all_pushbutton.setEnabled(enable_add_buttons)
        self.remove_pushButton.setEnabled(enable_remove_buttons)
        self.remove_all_pushButton.setEnabled(enable_remove_buttons)

        # Single add/remove buttons need a selected covariate in their
        # respective listwidgets
        if (not self.available_covs_listWidget.currentItem()):
            self.add_pushbutton.setEnabled(False)
            self.add_pushbutton.setToolTip('must select a covariate to add')
        else:
            self.add_pushbutton.setToolTip('')

        if (not self.selected_covs_listWidget.currentItem()):
            self.remove_pushButton.setEnabled(False)
            self.remove_pushButton.setToolTip('must select a covariate to remove')
        else:
            self.remove_pushButton.setToolTip('')

        
    def chg_add_interaction_btn_enabled_status(self):
        # 1. You can only add an interaction if not every interaction is there
        # already, given the added covariates
        # 2. Also, only interactions betwixt added covariates are allowed.
        # 3. Only interactions between two variables are allowed
        #
        # NOTE: should be run when:
        #    1) a covariate(s) is added
        #    2) a covariate(s) is removed
        #    3) an interaction is added
        #    4) an interaction is removed
        
        enable = True
        
        covariates = self.get_included_covariates()
        interactions = self.get_interactions()
        
        possible_interactions = self._get_possible_interactions(covariates)
        
        if len(possible_interactions) == 0:
            enable = False # due to no covariates yet selected
        
        if len(possible_interactions) == len(interactions):
            enable = False # all interactions possible already added
        
        self.add_interaction_pushButton.setEnabled(enable)
        
    def chg_remove_interaction_btn_enabled_status(self):
        # You can only remove an interaction if there is at least one
        # interaction
        #
        # Should be run when:
        #     a) interaction added
        #     b) interaction removed
        
        enable = True
        if len(self.get_interactions()) == 0:
            enable = False
        self.remove_interaction_pushButton.setEnabled(enable)
            
    def _get_possible_interactions(self, covariate_list):
        if len(covariate_list) < 2:
            return []
        interactions = [Interaction([var_a,var_b]) for var_a, var_b in itertools.combinations(covariate_list,2)]
        #for interaction in interactions:
        #    print("%s" % interaction)
        
        return interactions
        
    def setup_connections(self):
        # adding and removing covariates
        self.add_all_pushbutton.clicked.connect(self.add_all_covs)
        self.remove_all_pushButton.clicked.connect(self.remove_all_covs)
        # lambdas since 'clicked' signal sends along an unwanted bool
        self.add_pushbutton.clicked.connect(lambda: self.add_one_cov())
        self.remove_pushButton.clicked.connect(lambda: self.remove_one_cov())
        self.available_covs_listWidget.itemDoubleClicked.connect(self.add_one_cov)
        self.selected_covs_listWidget.itemDoubleClicked.connect(self.remove_one_cov)
        # Toggle enable status of add/remove buttons
        self.covariateAdded.connect(self.toggle_covariate_buttons_enabled_status)
        self.covariateRemoved.connect(self.toggle_covariate_buttons_enabled_status)
        self.available_covs_listWidget.currentItemChanged.connect(self.toggle_covariate_buttons_enabled_status)
        self.selected_covs_listWidget.currentItemChanged.connect(self.toggle_covariate_buttons_enabled_status)

        #### interaction buttons
        # Connect buttons to handlers
        self.add_interaction_pushButton.clicked.connect(self.add_interaction_clicked)
        self.remove_interaction_pushButton.clicked.connect(self.remove_interaction_clicked)
        
        # add interaction button enable signals
        self.covariateAdded.connect(self.chg_add_interaction_btn_enabled_status)
        self.covariateRemoved.connect(self.chg_add_interaction_btn_enabled_status)
        self.interactionAdded.connect(self.chg_add_interaction_btn_enabled_status)
        self.interactionRemoved.connect(self.chg_add_interaction_btn_enabled_status)
        # remove interaction button enable signals
        self.interactionAdded.connect(self.chg_remove_interaction_btn_enabled_status)
        self.interactionRemoved.connect(self.chg_remove_interaction_btn_enabled_status)
    
    def setup_values_from_previous_analysis(self, prev_covs):        
        if prev_covs:
            self.prev_covs = prev_covs
        else:
            self.prev_covs = []
    
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
        
        # Toggle the enable status of the add/remove covariate buttons
        self.toggle_covariate_buttons_enabled_status()

        # enable/disable interaction buttons
        self.chg_add_interaction_btn_enabled_status()
        self.chg_remove_interaction_btn_enabled_status()
        
    def init_covariates_lists(self):
        self.available_covariates = []
        self.selected_covariates = []
        self.unavailable_covariates = []
        
        included_studies = self.wizard().get_included_studies_in_proper_order()
        
        if self.allow_covs_with_missing_data:
            self.available_covariates = self.model.get_variables()
        else:
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
            label = cov.get_label()
            if self.allow_covs_with_missing_data:
                missing_entries = self.count_missing_entries(cov)
                if missing_entries > 0:
                    label += " (%d missing entries)" % missing_entries

            item = QListWidgetItem(label)
            self.cov_to_item[cov] = item
            self.item_to_cov[item]=cov
            
    def count_missing_entries(self, cov):
        # count the number of missing entries for the cov in the included
        # studies
        
        included_studies = self.wizard().get_included_studies_in_proper_order()
        
        # count missing data points
        n_missing = 0
        for study in included_studies:
            val = study.get_var(cov)
            if val is None or val == "":
                n_missing += 1
        return n_missing
    
                
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
        self.covariateAdded.emit()
        
        
    def remove_one_cov(self, item=None, emit_change_signal=True):
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
        self.covariateRemoved.emit()

        
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
    
    def _require_categorical(self):
        if self.disable_require_categorical:
            return False
        return self.wizard()._require_categorical()
                   
    def isComplete(self):
        if self._require_categorical():
            # is there at least one categorical variable selected?
            select_cov_types = (cov.get_type()==CATEGORICAL for cov in self.selected_covariates)
            return any(select_cov_types)
        else:
            # are at least the minimum # of covariates selected?
            return len(self.selected_covariates) >= self.min_covariates
                
        
    ############ getters ################################################   
    def get_included_covariates(self):
        return self.selected_covariates
    
    def get_interactions(self):
        return self.interactions
    
    ###########################################################################
    
    def __str__(self):
        covariates_str = "\n".join(["  " + cov.get_label() for cov in self.get_included_covariates()])
        interactions_str = "\n".join(["  " + str(interaction) for interaction in self.interactions])
        
        if len(self.interactions)==0:
            summary = "Included Covariates:\n%s" % covariates_str
        else:
            summary = "Included Covariates:\n%s\nInteractions: %s" % (covariates_str, interactions_str)
        return summary
        
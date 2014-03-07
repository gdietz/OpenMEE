##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
# Date: 3/7/14   #
#                #
##################

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_covariate_select_page

class CovariateSelectPage(QWizardPage, ui_covariate_select_page.Ui_WizardPage):
    
    covariateAdded = pyqtSignal()
    covariateRemoved = pyqtSignal()
    
    def __init__(self, model, parent=None): # todo: set defaults of previous parameters to None
        super(CovariateSelectPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.setup_connections()
        
        self.studies = self.model.get_studies_in_current_order()
        
    def setup_connections(self):
        # adding and removing covariates
        self.add_all_pushbutton.clicked.connect(self.add_all_covs)
        self.remove_all_pushButton.clicked.connect(self.remove_all_covs)
        # lambdas since 'clicked' signal sends along an unwanted bool
        self.add_pushbutton.clicked.connect(lambda: self.add_one_cov())
        self.remove_pushButton.clicked.connect(lambda: self.remove_one_cov())
        self.available_covs_listWidget.itemDoubleClicked.connect(self.add_one_cov)
        self.selected_covs_listWidget.itemDoubleClicked.connect(self.remove_one_cov)
    
    
    def initializePage(self):
        self.init_covariates_lists()
 
        # make mapping of covariates to list_items and visa-versa
        self.cov_to_item = {}
        self.item_to_cov = {}
        self.make_items_for_covs(self.available_covariates
                                 +self.selected_covariates)
        
        # populate the 3 list widgets with items
        self.populate_listWidget(self.available_covs_listWidget, self.available_covariates)
        self.populate_listWidget(self.selected_covs_listWidget, self.selected_covariates)
        
    def init_covariates_lists(self):
        self.available_covariates = []
        self.selected_covariates = []
        
        self.available_covariates = self.model.get_variables()
        
        # sort the lists
        sort_by_label = lambda var: var.get_label()
        self.available_covariates.sort(key=sort_by_label)
        self.selected_covariates.sort(key=sort_by_label)
        
    def make_items_for_covs(self, cov_list):
        ''' Makes an QListWidgetItem for each cov and stores it in a dictionary
        mapping cov --> item '''
        
        def cov_item_label(cov):
            ''' Covariate item label will be the name of the covariate followed
            by the number of missing data points e.g. "Habitat (4 missing entries) '''
            name = cov.get_label()
            #n_studies = len(self.studies)
            
            # count missing data points
            n_missing = 0
            for study in self.studies:
                val = study.get_var(cov)
                if val is None or val == "":
                    n_missing += 1
            
            #entries_str = entries_str="entry" if n_missing==1 else "entries"
            
            label = "{cov_name} ({n_missing} missing".format(
                            cov_name=name, n_missing=n_missing)
            return label
        
        for cov in cov_list:
            item = QListWidgetItem(cov_item_label(cov))
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
        self.covariateAdded.emit()
        
        
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
                  
    def isComplete(self):
        # are at least 2 covariates selected?
        return len(self.selected_covariates) >= 2
                
        
    ############ getters ################################################   
    def get_included_covariates(self):
        return self.selected_covariates
    ###########################################################################
    
    def __str__(self):
        covariates_str = "\n".join(["  " + cov.get_label() for cov in self.get_included_covariates()])
        summary = "Included Covariates:\n%s" % covariates_str
        return summary
        
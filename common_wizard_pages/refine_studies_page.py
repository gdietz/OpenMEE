##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

#from functools import partial
#import gc

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *
from dataset.study import Study

import ui_refine_studies_page
from scrollable_infobox import ScrollableInfoBox

MISSING_ENTRY_STR = "Not entered"
INCLUDED = True


# Policy:
# Use include states of previously analyzed studies if the state exists,
# otherwise, include the study by default (if it is includable)

class Var_Categories_Nstudies:
    # For each variable, stores the categories associated with it
    # for each category, stores the # of studies that have that category
    
    def __init__(self, studies, categorical_variables):
        self.studies = studies
        self.categorical_variables = categorical_variables
        self.preprocess()
        
    def preprocess(self):
        self.var_to_cat_to_n_studies = {var: {} for var in self.categorical_variables} # number of studies for each category of var
        
        MISSING_CATEGORIES = [None, ""] # values which mean 'missing category'
        
        # get categories of each variable and n_studies of each variable
        for var in self.categorical_variables:
            for study in self.studies:
                category = study.get_var(var)
                if category in MISSING_CATEGORIES:
                    category = None
                try:
                    n = self.var_to_cat_to_n_studies[var][category]
                except KeyError:
                    n = 0
                self.var_to_cat_to_n_studies[var][category] = n + 1 

    def get_categories_of_var(self, var):
        ''' returns sorted categories of variable, putting missing entry at the end'''
        
        categories = self.var_to_cat_to_n_studies[var].keys()
        categories.sort()
        try:
            categories.remove(None)
            None_addition = [None,]
        except ValueError: # None is not present as a category
            None_addition = []
            
        return categories + None_addition
        
    
    def get_n_studies_for_category_of_var(self, var, cat):
        try:
            return self.var_to_cat_to_n_studies[var][cat]
        except KeyError: # if the category is not found, there are zero studies
            return 0
        
class StudyFilter:
    def __init__(self, allowed_studies, reason_others_excluded=""):
        self.allowed_studies = allowed_studies
        self.reason_others_excluded = reason_others_excluded
        
    def is_allowed(self, study):
        ''' Returns true if the study is allowed, False otherwise.
            If false, the reason string is provided '''
        allowed = study in self.allowed_studies
        if allowed:
            return (True, None)
        else:
            return (False, self.reason_others_excluded)

class RefineStudiesPage(QWizardPage, ui_refine_studies_page.Ui_WizardPage):
    def __init__(self,
                 model,
                 previously_included_studies=None,
                 study_filter = None, # an object which contains info about which studies are allowed
                 need_species = False,
                 parent=None):
        super(RefineStudiesPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.previously_included_studies = previously_included_studies
        self.need_species = need_species
        
        self.studies_to_include_status = {} # map study ---> included?
        self.missing_data_items_to_covs = {}
        self.items_to_studies = {} # items refers to those in the refine_studies tab
        # mapping: item --> (categorical variable, category)
        self.items_to_factor_values = {} # items refers to those in the refine_categories tab
        
        # stores former state of tree widget item (has to do with transitions from partially_checked --> unchecked when some underlying studies are not includable
        self.treeitem_previous_states = {}
        
        QObject.connect(self.refine_studies_list_widget, SIGNAL("itemChanged(QListWidgetItem*)"), self._change_study_include_state)
        QObject.connect(self.cat_treeWidget, SIGNAL("itemChanged(QTreeWidgetItem*,int)"),         self._change_category_include_state)
        
        QObject.connect(self.select_all_btn, SIGNAL("clicked()"), self.include_all_studies)
        QObject.connect(self.deselect_all_btn, SIGNAL("clicked()"), self.deselect_all_studies)
        
        self.tabWidget.currentChanged.connect(self.handle_tab_change)
        self.missing_data_apply_btn.clicked.connect(self.apply_btn_pushed)
        
        if DEBUG_MODE:
            print_include_btn = QPushButton("Print included status")
            self.refine_studies_btn_layout.addWidget(print_include_btn)
            QObject.connect(print_include_btn, SIGNAL("clicked()"), self.print_included_studies)
        
        self.slow_preprocessing()
    
    def slow_preprocessing(self):
        # this holds the slow operations, not that slow anymore
        self.categorical_variables = self.model.get_categorical_variables()
        self.studies = self.model.get_studies_in_current_order()
        
        self.var_category_n_study_info = Var_Categories_Nstudies(studies=self.studies,
                                                                 categorical_variables=self.categorical_variables)
        
    
    def handle_tab_change(self, tab_index):
        print("Tab index is now %d" % tab_index)
        if tab_index == 0: # studies list tab
            self._recheck_studies_list()
        elif tab_index == 1:
            self.included_cat_stats = Var_Categories_Nstudies(
                                            studies=self.get_included_studies(),
                                            categorical_variables=self.categorical_variables)
            #print("collecting the garbage")
            #gc.collect() # a test to see if collecting the garbage generates the C++ Runtime error about the deleted object, it does not.
            self._recheck_category_tree_widget()
            print("any problems?")
            
        if tab_index == 2: # 2 is the index of the exclude missing data tab
            self._populate_missing_data_list()
    
    def apply_btn_pushed(self):
        value_is_empty = lambda val: val==None or str(val)==""
        
        checked_covs = [cov for item,cov in self.missing_data_items_to_covs.iteritems() if item.checkState() == Qt.Checked]
        included_studies = [study for study,status in self.studies_to_include_status.iteritems() if status == INCLUDED]
        
        removed_study_names_to_cov_name_which_caused_removal = []
        for study in included_studies:
            for cov in checked_covs:
                if value_is_empty(study.get_var(cov)):
                    self.studies_to_include_status[study] = False
                    removed_study_names_to_cov_name_which_caused_removal.append(study.get_label()+": "+cov.get_label())
                    break
        
        if len(removed_study_names_to_cov_name_which_caused_removal) > 0:
            scrollable_infobox = ScrollableInfoBox(windowtitle="Removed Study Names",
                                                   main_label="The following studies were excluded along with the covariate causing their exclusion:",
                                                   content="\n".join(removed_study_names_to_cov_name_which_caused_removal))
            scrollable_infobox.exec_()
        else:
            QMessageBox.information(self, "", "No studies needed to be excluded")
        self.tabWidget.setCurrentIndex(0) # 0 is the index of the refine studies list
        
        self._populate_missing_data_list() # clears list and repopulates it
        
    def initializePage(self):
        # get variables associated with effect size and variance
        data_location   = self.wizard().get_data_location()
        effect_size_col = data_location['effect_size']
        variance_col    = data_location['variance']

        self.effect_size_var = self.model.get_variable_assigned_to_column(effect_size_col)
        self.variance_var    = self.model.get_variable_assigned_to_column(variance_col)
        
        # for issue #15
        if self.need_species:
            species_col = data_location['species']
            self.species_var = self.model.get_variable_assigned_to_column(species_col)
        
        # map studies to boolean storing whether they CAN be included (if they have values for effect size and variance)
        self.studies_includable = dict([(study, self._is_includable(study)[0]) for study in self.studies])
        # maps studies to boolean storing whether they are included or not
        self.studies_to_include_status = self.get_studies_included_dict_with_previously_included_studies()

        self._populate_refine_studies_tab()
        self._populate_refine_categories_tab()
        

        
        self.emit(SIGNAL("completeChanged()"))
        

        
    def _get_default_studies_included_dict(self):
        #''' Includes all includable studies '''
        ''' Nothing included by default '''
        
        #return dict([(study, self.studies_includable[study]) for study in self.studies])
        return dict([(study, False) for study in self.studies])
    
    def get_studies_included_dict_with_previously_included_studies(self):
        previously_included_studies = self.model.get_previously_included_studies()
        
        included_studies_dict = self._get_default_studies_included_dict()
        
        for study,status in included_studies_dict.items():
            # modify dictionary if there is a previous include/exclude state
            if previously_included_studies is not None:
                if study in previously_included_studies and self._is_includable(study)[0]:
                    included_studies_dict[study] = True
                else:
                    included_studies_dict[study] = False 
        
        if len(included_studies_dict) > 0:
            first_el_is_study = [isinstance(x,Study) for x in included_studies_dict.iterkeys()]
            if not all(first_el_is_study):
                raise Exception("The first element of each tuple should be a study!")
        return included_studies_dict
        
    def _is_includable(self, study):
        ''' Returns a tuple indicating whether or not a study is includable:
        Returns a tuple: (boolean includable, str reason not includable)
        To be includable, a study must:
            1) Have an effect size and variance
            2) The variance must not be zero.
            3) If the study needs a species, it must have one
        '''
        
        if not isinstance(study, Study):
            raise TypeError("study argument is not a study")
        
        includable = True
        reason = ""
        if not self._effect_size_and_var_present(study):
            includable = False
            reason = "Effect size or variance missing"
        else:
            if study.get_var(self.variance_var) == 0:
                includable = False
                reason = "zero variance"
            elif study.get_var(self.variance_var) < 0:
                includable = False
                reason = "negative variance is invalid"
            else:
                if self.need_species and not self._species_present(study):
                    includable = False
                    reason = "species is missing"
        
        return (includable, reason)

    def _effect_size_and_var_present(self, study):
        effect_size = study.get_var(self.effect_size_var)
        variance = study.get_var(self.variance_var)
        
        includable = False
        if isinstance(effect_size, float) and isinstance(variance, float):
            includable = True
            
        return includable
    
    def _species_present(self, study):
        species = study.get_var(self.species_var)
        
        if isinstance(species, str) and len(species) > 0:
            return True
        return False

    
    def print_old_new(self, old, new):
        print("Old: %s, New: %s" % (str(old), str(new)))
        


    
    def isComplete(self):
        if True in self.studies_to_include_status.values():
            return True
        return False
    
    def print_included_studies(self):
        ''' For debugging, prints the status of the studies: included or not '''
        
        for study, include_state in self.studies_to_include_status.items():
            print("Study id,label: %d,%s\tInclude State: %s" % (study.get_id(), str(study.get_label()), str(include_state)))
    
    
    def include_all_studies(self):
        ''' include all the studies that CAN be included '''
        
        # First change the include status of the studies, then, change the checkboxes & tree
        for study in self.studies_to_include_status.keys():
            if not isinstance(study, Study):
                raise TypeError("study argument is not a study")
            if self._is_includable(study)[0]:
                self.studies_to_include_status[study] = True # include in study
        
        # change status of the checkboxes
        self._recheck_studies_list()
        self.emit(SIGNAL("completeChanged()"))
        
    def deselect_all_studies(self):
        # just like include_all_studies but deselect
        for study in self.studies_to_include_status.keys():
            self.studies_to_include_status[study] = False

        self._recheck_studies_list()
        self.emit(SIGNAL("completeChanged()"))
        
    def _recheck_category_tree_widget(self):
        self.cat_treeWidget.blockSignals(True)
        
        for category_item in self.items_to_factor_values.keys():
                category_item.setCheckState(0, self._get_rightful_state_of_treewidget_item(self.included_cat_stats, category_item))
        
        self.cat_treeWidget.blockSignals(False)
        
    def _recheck_studies_list(self):
        ''' Resets the checks mark status of the studies list widget based on
        the internal study include status '''
        
        self.refine_studies_list_widget.blockSignals(True)
        
        # work on studies list first
        for x in xrange(self.refine_studies_list_widget.count()):
            item = self.refine_studies_list_widget.item(x)
            study = self.items_to_studies[item]
            item.setCheckState(Qt.Checked if self.studies_to_include_status[study] is True else Qt.Unchecked)
            
        self.refine_studies_list_widget.blockSignals(False)
    
    def _populate_refine_studies_tab(self):
        ''' Adds checkable list of studies based on their include state'''
        
        self.refine_studies_list_widget.blockSignals(True)
        self.refine_studies_list_widget.clear()
        
        for study in self.studies:
            includable, reason = self._is_includable(study)
            
            
            label = study.get_label()
            if label in [None, ""]:
                row = self.model.get_row_assigned_to_study(study)
                label = "Study row %d" % (row+1) # row in model indexed from 0
            if not includable:
                label += " (can't include study: %s)" % reason
            item = QListWidgetItem(label)
            self.items_to_studies[item] = study
            item.setCheckState(Qt.Checked if self.studies_to_include_status[study] is True else Qt.Unchecked)
            if not includable:
                item.setFlags(Qt.ItemIsSelectable)
            self.refine_studies_list_widget.addItem(item)
        
        self.refine_studies_list_widget.blockSignals(False)
            
    def _populate_refine_categories_tab(self):
        # count number of currently included studies in each category
        self.included_cat_stats = Var_Categories_Nstudies(
                                                    studies=self.get_included_studies(),
                                                    categorical_variables=self.categorical_variables)
        self.cat_treeWidget.blockSignals(True)
        self.cat_treeWidget.clear()
        
        self.cat_treeWidget.setColumnCount(1)
        toplevel_factor_items = []
        for var in self.categorical_variables:
            item = QTreeWidgetItem(self.cat_treeWidget, [QString(var.get_label())])
            toplevel_factor_items.append(item)
            ## add categories to factor as checkable options
            categories = self.var_category_n_study_info.get_categories_of_var(var)
            for category in categories:
                if category is not None:
                    category_item = QTreeWidgetItem(item, [QString(category)])
                else:
                    category_item = QTreeWidgetItem(item, [QString(MISSING_ENTRY_STR)])
                self.items_to_factor_values[category_item] = (var, category)
                category_item.setCheckState(0, self._get_rightful_state_of_treewidget_item(self.included_cat_stats, category_item))
                self.treeitem_previous_states[category_item] = category_item.checkState(0)

        if len(toplevel_factor_items) > 0: # just expand the first toplevel item
            self.cat_treeWidget.expandItem(toplevel_factor_items[0])
        self.cat_treeWidget.blockSignals(False)
        
    def _get_rightful_state_of_treewidget_item(self, current_stats, item):
        ''' Gets the rightful state of the item, where item is a checkable
        box from the tree widget and state is checked, partially checked, or
        unchecked '''
        
        variable, category = self.items_to_factor_values[item]
        n_studies_in_category = self.var_category_n_study_info.get_n_studies_for_category_of_var(variable, category)
        n_included_studies_in_category = current_stats.get_n_studies_for_category_of_var(variable, category)
        
        if n_included_studies_in_category==n_studies_in_category: # all studies checked
            return Qt.Checked
        elif n_included_studies_in_category==0: # no studies checked
            return Qt.Unchecked
        else: # some studies are checked
            return Qt.PartiallyChecked
    
        
    def _change_study_include_state(self, item):
        bad_checkstate_msg = "Should not get here, did I forget to disable signals?"
        print('entered _change_include_state')
        
        state = item.checkState()
        study = self.items_to_studies[item]
        
        if state == Qt.Unchecked:
            self.studies_to_include_status[study] = False
        elif state == Qt.Checked:
            self.studies_to_include_status[study] = True
        else:
            raise ValueError(bad_checkstate_msg)
        
        
        
        self.emit(SIGNAL("completeChanged()"))
    
    def _change_category_include_state(self, item, column=None):
        bad_checkstate_msg = "Should not get here, did I forget to disable signals?"
        
        state = item.checkState(column)
        
        #############
        # change transition from partially checked---> checked to
        # partially checked-->unchecked
        previous_state = self.treeitem_previous_states[item]
        if state == Qt.Checked and previous_state == Qt.PartiallyChecked and self._get_rightful_state_of_treewidget_item(self.included_cat_stats, item) == Qt.PartiallyChecked:
            state = Qt.Unchecked
            self.treeitem_previous_states[item] = state
        # let the state think it is checked in order to includes studies but actually its just partially checked
        elif state == Qt.Checked and previous_state == Qt.Unchecked and self._get_rightful_state_of_treewidget_item(self.included_cat_stats, item) == Qt.PartiallyChecked:
            self.treeitem_previous_states[item] = Qt.PartiallyChecked
        else: # no special condition
            self.treeitem_previous_states[item] = state
        #################
        
            
        print("changing included state in refine categories")
        # check or deselect as necessary across groups of studies
        variable, category = self.items_to_factor_values[item]
        for study in self.studies_to_include_status.keys():
            if study.get_var(variable)==category and self._is_includable(study)[0]:
                print("matched")
                if state == Qt.Unchecked:
                    self.studies_to_include_status[study]=False
                elif state == Qt.Checked:
                    self.studies_to_include_status[study]=True
                else:
                    raise ValueError(bad_checkstate_msg)
        self.emit(SIGNAL("completeChanged()"))

    def _populate_missing_data_list(self):
        ''' Adds checkable list of covariates'''
        
        self.missing_data_listwidget.blockSignals(True)
        self.missing_data_listwidget.clear()
        self.missing_data_items_to_covs = {}
        
        # get and sort lists of possible continuous and categoical covariates
        continuous_covariates = self.model.get_sorted_continuous_covariates()
        categorical_covariates = self.model.get_sorted_categorical_covariates()
        count_covariates = self.model.get_sorted_count_covariates()
        
        def add_covariates_to_list(covariates, suffix = ""):
            for cov in covariates: 
                label = cov.get_label()
                if label is None:
                    label = ""
                label += " "+suffix
                item = QListWidgetItem(label)
                self.missing_data_items_to_covs[item] = cov
                item.setCheckState(Qt.Unchecked)
                item.setFlags(item.flags()|Qt.ItemIsUserCheckable)
                self.missing_data_listwidget.addItem(item)
        
        
        add_covariates_to_list(continuous_covariates, suffix="(continuous)")
        add_covariates_to_list(categorical_covariates, suffix="(categorical)")
        add_covariates_to_list(count_covariates, suffix="(count)")
        
        self.missing_data_listwidget.blockSignals(False)
        
    ############################## getter #####################################
    
    def get_included_studies(self):
        ''' main interface to outside '''
        
        return [study for study,included in self.studies_to_include_status.items() if included]

    def get_included_studies_in_proper_order(self):
        all_studies = self.model.get_studies_in_current_order()
        included_studies = [study for study,included in self.studies_to_include_status.items() if included]
        included_studies_in_order = [study for study in all_studies if study in included_studies]
        return included_studies_in_order
    
    ###########################################################################
    
    def __str__(self):
        summary = "Included Studies:\n"
        
        studies = self.get_included_studies()
        summary += "\n".join(["  %s" % study.get_label() for study in studies])
        return summary
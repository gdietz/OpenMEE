##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *
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
        return self.var_to_cat_to_n_studies[var][cat]
        


class RefineStudiesPage(QWizardPage, ui_refine_studies_page.Ui_WizardPage):
    def __init__(self, model, mode=MA_MODE, previously_included_studies=None, parent=None):
        super(RefineStudiesPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.mode = mode
        self.previously_included_studies = previously_included_studies
        
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
        
        #QObject.connect(self.cat_treeWidget, SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"), self.print_old_new)
        
        self.tabWidget.currentChanged.connect(self.handle_tab_change)
        self.missing_data_apply_btn.clicked.connect(self.apply_btn_pushed)
        
        if DEBUG_MODE:
            print_include_btn = QPushButton("Print included status")
            self.refine_studies_btn_layout.addWidget(print_include_btn)
            QObject.connect(print_include_btn, SIGNAL("clicked()"), self.print_included_studies)
            
            
        # For performance improvement
        self.included_studies_changes = {'added':set(),
                                         'removed':set()}
        
        self.slow_preprocessing()
    
    #@profile_this
    def slow_preprocessing(self):
        # this holds the slow operations
        self.categorical_variables = self.model.get_categorical_variables()
        self.studies = self.model.get_studies_in_current_order()
        
        self.var_category_n_study_info = Var_Categories_Nstudies(studies=self.studies,
                                                                 categorical_variables=self.categorical_variables)
        
    def reset_included_studies_changes(self):
        self.included_studies_changes = {'added':set(),
                                         'removed':set()}
    
    
    def handle_tab_change(self, tab_index):
        print("Tab index is now %d" % tab_index)
        if tab_index == 0: # studies list tab
            self.reset_included_studies_changes()
            self._recheck_studies_list()
        elif tab_index == 1:
            self._recheck_category_tree_widget()
        if tab_index == 2: # 2 is the index of the exclude missing data tab
            self.reset_included_studies_changes()
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
                    self._included_studies_changes(study, added=False)
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
        
    #@profile_this
    def initializePage(self):
        # get variables associated with effect size and variance
        data_location   = self.wizard().get_data_location()
        effect_size_col = data_location['effect_size']
        variance_col    = data_location['variance']
        self.effect_size_var = self.model.get_variable_assigned_to_column(effect_size_col)
        self.variance_var    = self.model.get_variable_assigned_to_column(variance_col)
        
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
            assert(all(first_el_is_study),"The first element of each tuple should be a study!")
        return included_studies_dict
        
    def _is_includable(self, study):
        ''' Returns a tuple indicating whether or not a study is includable (i.e. if it has an
        effect size and variance. tuple: (boolean includable, str reason not includable) '''
        
        if not isinstance(study, Study):
            raise TypeError("study argument is not a study")
        
        if self._effect_size_and_var_present(study):
            includable = True
            reason = ""
        else:
            includable = False
            reason = "Effect size or variance missing"
        
        return (includable, reason)

    def _effect_size_and_var_present(self, study):  
        effect_size = study.get_var(self.effect_size_var)
        variance = study.get_var(self.variance_var)
        
        includable= False
        if isinstance(effect_size, float) and isinstance(variance, float):
            includable=True
            
        return includable

    
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
    
    def get_included_studies(self):
        ''' main interface to outside '''
        
        return [study for study,included in self.studies_to_include_status.items() if included]
        
        
        
    def include_all_studies(self):
        ''' include all the studies that CAN be included '''
        
        # First change the include status of the studies, then, change the checkboxes & tree
        for study in self.studies_to_include_status.keys():
            if not isinstance(study, Study):
                raise TypeError("study argument is not a study")
            if self._is_includable(study)[0]:
                self.studies_to_include_status[study] = True # include in study
                self._included_studies_changes(study, added=True)
        
        # change status of the checkboxes
        self._recheck_studies_list()
        self.emit(SIGNAL("completeChanged()"))
        
    def deselect_all_studies(self):
        # just like include_all_studies but deselect
        for study in self.studies_to_include_status.keys():
            self.studies_to_include_status[study] = False
            self._included_studies_changes(study, added=False)

        self._recheck_studies_list()
        self.emit(SIGNAL("completeChanged()"))
        
    def _recheck_category_tree_widget(self):
        self.cat_treeWidget.blockSignals(True)

        # work on tree widget next
        for category_item in self.items_to_factor_values.keys():
            #category_item.setCheckState(0, self._get_rightful_state_of_treewidget_item(category_item))
            category_item.setCheckState(0, self._get_rightful_state_of_treewidget_item__for_study_changes(category_item))
        
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
        self.cat_treeWidget.setColumnCount(1)
        toplevel_factor_items = []
        for var in self.categorical_variables:
            item = QTreeWidgetItem(QStringList(var.get_label()))
            toplevel_factor_items.append(item)
            ## add categories to factor as checkable options
            categories = self.var_category_n_study_info.get_categories_of_var(var)
            for category in categories:
                if category is not None:
                    category_item = QTreeWidgetItem(QStringList(category))
                else:
                    category_item = QTreeWidgetItem(QStringList(MISSING_ENTRY_STR))
                self.items_to_factor_values[category_item] = (var, category)
                category_item.setCheckState(0, self._get_rightful_state_of_treewidget_item(category_item))
                self.treeitem_previous_states[category_item] = category_item.checkState(0)
                item.addChild(category_item)
            
        
        self.cat_treeWidget.blockSignals(True)
        self.cat_treeWidget.clear()
        self.cat_treeWidget.insertTopLevelItems(0, toplevel_factor_items)
        for item in toplevel_factor_items:
            self.cat_treeWidget.expandItem(item)
        self.cat_treeWidget.blockSignals(False)
    
    @profile_this
    def _get_rightful_state_of_treewidget_item(self, item):
        ''' Gets the rightful state of the item, where item is a checkable
        box from the tree widget and state is checked, partially checked, or
        unchecked '''
        
        
        variable, category = self.items_to_factor_values[item]
        studies_in_category = [study for study in self.studies if study.get_var(variable)==category]
        included_studies_in_category = [study for study in studies_in_category if self.studies_to_include_status[study]==True]
        
        if len(included_studies_in_category)==len(studies_in_category): # all studies checked
            return Qt.Checked
        elif len(included_studies_in_category)==0: # no studies checked
            return Qt.Unchecked
        else: # some studies are checked
            return Qt.PartiallyChecked
        
    def _get_rightful_state_of_treewidget_item__for_study_changes(self, item):
        ''' version of _get_rightful_state_of_treewidget_item() for use when
        the only change that happened was that the refine studies tab choices changed '''
         
        variable, category = self.items_to_factor_values[item]
        current_check_state = item.checkState(0)
         
        added_studies_set = self.included_studies_changes['added']
        removed_studies_set = self.included_studies_changes['removed']

        n_studies_in_category = self.var_category_n_study_info.get_n_studies_for_category_of_var(variable, category)
        
        # for performance gains
        if current_check_state == Qt.Checked:
            if category in [study.get_var(variable) for study in removed_studies_set]:
                pass # continue on with the slow rest of the function
            else: # category was not touched by the changes
                return Qt.Checked
        elif current_check_state == Qt.Unchecked:
            category_of_each_added_study = [study.get_var(variable) for study in added_studies_set]
            if category in category_of_each_added_study:
                # were all the studies of this category added?
                if len([x for x in category_of_each_added_study if x==category]) == n_studies_in_category:
                    return Qt.Checked
            else: # category was not touched by the changes
                return Qt.Unchecked
        elif current_check_state == Qt.PartiallyChecked:
            category_of_each_added_study = [study.get_var(variable) for study in added_studies_set]
            category_of_each_removed_study = [study.get_var(variable) for study in removed_studies_set]
            if category not in category_of_each_added_study+category_of_each_removed_study: 
                return Qt.PartiallyChecked # category was not touched by the changes
  
        
        #studies_in_category = [study for study in self.studies if study.get_var(variable)==category]
        included_studies_in_category = [study for study in self.studies if self.studies_to_include_status[study]==True and study.get_var(variable)==category]
        
        if len(included_studies_in_category)==n_studies_in_category: # all studies checked
            return Qt.Checked
        elif len(included_studies_in_category)==0: # no studies checked
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
            self._included_studies_changes(study, added=False)
        elif state == Qt.Checked:
            self.studies_to_include_status[study] = True
            self._included_studies_changes(study, added=True)
        else:
            raise ValueError(bad_checkstate_msg)
        
        
        
        self.emit(SIGNAL("completeChanged()"))
        
    def _included_studies_changes(self, study, added):
        # Before we entered the refine studies tab the included_studies_changes dict should be empty
        # if we add a study, we add it to the 'added' subset
        # if we remove a study, we add it to the 'removed' subset
        # if we add a study then remove it, there is no net change, so we remove it from both sets
        #     likewise if we remove a study, then add it back
        
        added_set = self.included_studies_changes['added']
        removed_set = self.included_studies_changes['removed']
        
        # initially := when the tab became visible
        if added:
            try: # if successful, study was initially included
                removed_set.remove(study)
            except KeyError:
                added_set.add(study)
        else: # removed
            try: # if successful, study was initially included
                added_set.remove(study)
            except KeyError:
                removed_set.add(study)
    
    def _change_category_include_state(self, item, column=None):
        bad_checkstate_msg = "Should not get here, did I forget to disable signals?"
        
        state = item.checkState(column)
        
        #############
        # change transition from partially checked---> checked to
        # partially checked-->unchecked
        previous_state = self.treeitem_previous_states[item]
        if state == Qt.Checked and previous_state == Qt.PartiallyChecked and self._get_rightful_state_of_treewidget_item(item) == Qt.PartiallyChecked:
            state = Qt.Unchecked
            self.treeitem_previous_states[item] = state
        # let the state think it is checked in order to includes studies but actually its just partially checked
        elif state == Qt.Checked and previous_state == Qt.Unchecked and self._get_rightful_state_of_treewidget_item(item) == Qt.PartiallyChecked:
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
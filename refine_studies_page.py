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

import ui_refine_studies_page

MISSING_ENTRY_STR = "Not entered"


# Policy:
# Use include states of previously analyzed studies if the state exists,
# otherwise, include the study by default (if it is includable)

class RefineStudiesPage(QWizardPage, ui_refine_studies_page.Ui_WizardPage):
    def __init__(self, model, mode=MA_MODE, parent=None):
        super(RefineStudiesPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.mode=mode
        
        self.studies_included_dict = {}
        
        self.studies = self.model.get_studies_in_current_order()
        
        self.categorical_variables = self.model.get_variables(var_type=CATEGORICAL)
        
        self.items_to_studies = {} # items refers to those in the refine_studies tab
        # mapping: item --> (categorical variable, category
        self.items_to_factor_values = {} # items refers to those in the refine_categories tab
        
        # stores former state of tree widget item (has to do with transitions from partially_checked --> unchecked when some underlying studies are not includable
        self.treeitem_previous_states = {}
        
        QObject.connect(self.refine_studies_list_widget, SIGNAL("itemChanged(QListWidgetItem*)"), partial(self.change_include_state, section='refine_studies'))
        QObject.connect(self.cat_treeWidget, SIGNAL("itemChanged(QTreeWidgetItem*,int)"),         partial(self.change_include_state, section='refine_categories'))
        
        #QObject.connect(self.refine_studies_list_widget, SIGNAL("itemClicked(QListWidgetItem*)"), self.item_clicked)
        QObject.connect(self.select_all_btn, SIGNAL("clicked()"), self.include_all_studies)
        QObject.connect(self.deselect_all_btn, SIGNAL("clicked()"), self.deselect_all_studies)
        
        QObject.connect(self.cat_treeWidget, SIGNAL("currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)"), self.print_old_new)
        
        if DEBUG_MODE:
            print_include_btn = QPushButton("Print included status")
            self.refine_studies_btn_layout.addWidget(print_include_btn)
            QObject.connect(print_include_btn, SIGNAL("clicked()"), self.print_included_studies)
        

    def initializePage(self):
        # map studies to boolean storing whether they CAN be included (if they have values for effect size and variance)
        self.studies_includable = dict([(study, self._is_includable(study)[0]) for study in self.studies])
        # maps studies to boolean storing whether they are included or not
        self.studies_included_dict = self.get_studies_included_dict_with_previously_included_studies()

        self.wizard().studies_included_table = self.studies_included_dict

        self._populate_refine_studies_tab()
        self._populate_refine_categories_tab()
        
        self.emit(SIGNAL("completeChanged()"))
        
    def _get_default_studies_included_dict(self):
        ''' Includes all includable studies '''
        
        return dict([(study, self.studies_includable[study]) for study in self.studies])
    
    def get_studies_included_dict_with_previously_included_studies(self):
        previous_study_inclusion_state = self.model.get_previously_included_studies()
        
        included_studies_dict = self._get_default_studies_included_dict()
        
        for study, include_status in included_studies_dict.items():
            # modify dictionary if there is a previous include/exclude state
            if study in previous_study_inclusion_state and self._is_includable(study)[0]:
                included_studies_dict[study] = previous_study_inclusion_state[study]
        
        return included_studies_dict
        
    def _is_includable(self, study):
        ''' Returns a tuple indicating whether or not a study is includable (i.e. if it has an
        effect size and variance. tuple: (boolean includable, str reason not includable) '''
        
        def effect_size_and_var_present():
            reason = ""
            # get variables associated with efffect size and variance
            data_location   = self.wizard().data_location
            effect_size_col = data_location['effect_size']
            variance_col    = data_location['variance']
            effect_size_var = self.model.get_variable_assigned_to_column(effect_size_col)
            variance_var    = self.model.get_variable_assigned_to_column(variance_col)
            
            effect_size = study.get_var(effect_size_var)
            variance = study.get_var(variance_var)
            
            includable= False
            if isinstance(effect_size, float) and isinstance(variance, float):
                includable=True
            
            reason = "Effect size or variance missing"
            return (includable, reason)
        
        
        includable, reason = effect_size_and_var_present()
        return (includable, reason)
    
    def print_old_new(self, old, new):
        print("Old: %s, New: %s" % (str(old), str(new)))
        


    
    def isComplete(self):
        if True in self.studies_included_dict.values():
            return True
        return False
    
    def print_included_studies(self):
        ''' For debugging, prints the status of the studies: included or not '''
        
        for study, include_state in self.studies_included_dict.items():
            print("Study id,label: %d,%s\tInclude State: %s" % (study.get_id(), str(study.get_label()), str(include_state)))
    

        
    def include_all_studies(self):
        ''' include all the studies that CAN be included '''
        
        # First change the include status of the studies, then, change the checkboxes & tree
        for study in self.studies_included_dict.keys():
            if self._is_includable(study)[0]:
                self.studies_included_dict[study] = True # include in study
        
        # change status of the checkboxes
        self._recheck_studies_lists()
        self.emit(SIGNAL("completeChanged()"))
        
    def deselect_all_studies(self):
        # just like include_all_studies but deselect
        for study in self.studies_included_dict.keys():
            self.studies_included_dict[study] = False
            
        self._recheck_studies_lists()
        self.emit(SIGNAL("completeChanged()"))
        
    def _recheck_studies_lists(self):
        ''' Resets the checks mark status of the studies list widget based on
        the internal study include status '''
        
        self.refine_studies_list_widget.blockSignals(True)
        self.cat_treeWidget.blockSignals(True)
        
        # work on studies list first
        for x in range(self.refine_studies_list_widget.count()):
            item = self.refine_studies_list_widget.item(x)
            study = self.items_to_studies[item]
            item.setCheckState(Qt.Checked if self.studies_included_dict[study] is True else Qt.Unchecked)
        
        # work on tree widget next
        for category_item in self.items_to_factor_values.keys():
            category_item.setCheckState(0, self.get_rightful_state_of_treewidget_item(category_item))
        
        self.refine_studies_list_widget.blockSignals(False)
        self.cat_treeWidget.blockSignals(False)
    
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
            #item.setFlags(item.flags()|Qt.ItemIsUserCheckable|Qt.ItemIsTristate)
            item.setCheckState(Qt.Checked if self.studies_included_dict[study] is True else Qt.Unchecked)
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
            categories = self.categories_of_var(self.studies, var)
            for category in categories:
                if category is not None:
                    category_item = QTreeWidgetItem(QStringList(category))
                else:
                    category_item = QTreeWidgetItem(QStringList(MISSING_ENTRY_STR))
                self.items_to_factor_values[category_item] = (var, category if category is not None else None)
                category_item.setCheckState(0, self.get_rightful_state_of_treewidget_item(category_item))
                self.treeitem_previous_states[category_item] = category_item.checkState(0)
                item.addChild(category_item)
            
        
        self.cat_treeWidget.blockSignals(True)
        self.cat_treeWidget.clear()
        self.cat_treeWidget.insertTopLevelItems(0, toplevel_factor_items)
        for item in toplevel_factor_items:
            self.cat_treeWidget.expandItem(item)
        self.cat_treeWidget.blockSignals(False)
        
    def get_rightful_state_of_treewidget_item(self, item):
        ''' Gets the rightful state of the item, where item is a checkable
        box from the tree widget and state is checked, partially checked, or
        unchecked '''
        
        
        variable, category = self.items_to_factor_values[item]
        studies_in_category = [study for study in self.studies if study.get_var(variable)==category]
        included_studies_in_category = [study for study in studies_in_category if self.studies_included_dict[study]==True]
        
        if len(included_studies_in_category)==len(studies_in_category): # all studies checked
            return Qt.Checked
        elif len(included_studies_in_category)==0: # no studies checked
            return Qt.Unchecked
        else: # some studies are checked
            return Qt.PartiallyChecked
        
    def get_maximum_checkstate_of_treewidget_item(self, item):
        ''' determines the maximum state of the item i.e. checked vs. partially checked '''
        
        variable, category = self.items_to_factor_values[item]
        studies_in_category = [study for study in self.studies if study.get_var(variable)==category]
        includable_studies_in_category = [study for study in studies_in_category if self.studies_includable[study]==True]
        
        if len(includable_studies_in_category)==len(studies_in_category): # all studies checked
            return Qt.Checked
        elif len(includable_studies_in_category)==0: # no studies checked
            return Qt.Unchecked
        else:
            return Qt.PartiallyChecked
        
            
    def change_include_state(self, item, column=None, section=None):
        if section is None:
            raise ValueError
        
        bad_checkstate_msg = "Should not get here, did I forget to disable signals?"
        print('entered change_include_state')
        
        if section == 'refine_studies':
            state = item.checkState()
            study = self.items_to_studies[item]
            
            if state == Qt.Unchecked:
                self.studies_included_dict[study] = False
            elif state == Qt.Checked:
                self.studies_included_dict[study] = True
            else:
                raise ValueError(bad_checkstate_msg)
        elif section == 'refine_categories':
            state = item.checkState(column)
            
            #############
            # change transition from partially checked---> checked to
            # partially checked-->unchecked
            previous_state = self.treeitem_previous_states[item]
            if state == Qt.Checked and previous_state == Qt.PartiallyChecked and self.get_maximum_checkstate_of_treewidget_item(item) == Qt.PartiallyChecked:
                state = Qt.Unchecked
                self.treeitem_previous_states[item] = state
            # let the state think it is checked in order to includes studies but actually its just partially checked
            elif state == Qt.Checked and previous_state == Qt.Unchecked and self.get_maximum_checkstate_of_treewidget_item(item) == Qt.PartiallyChecked:
                self.treeitem_previous_states[item] = Qt.PartiallyChecked
            else: # no special condition
                self.treeitem_previous_states[item] = state
            #################
            
                
            print("changing included state in refine categories")
            # check or deselect as necessary across groups of studies
            variable, category = self.items_to_factor_values[item]
            for study in self.studies_included_dict.keys():
                if study.get_var(variable)==category and self._is_includable(study)[0]:
                    print("matched")
                    if state == Qt.Unchecked:
                        self.studies_included_dict[study]=False
                    elif state == Qt.Checked:
                        self.studies_included_dict[study]=True
                    else:
                        raise ValueError(bad_checkstate_msg)
                    
        
        self._recheck_studies_lists()
        self.emit(SIGNAL("completeChanged()"))
            
        
#    def item_clicked(self, item):
#        study = self.items_to_studies[item]
        
    def categories_of_var(self, studies, variable):
        ''' Returns a list of the categories of a categorical variable'''
        
        if variable.get_type() != CATEGORICAL:
            raise ValueError("Variable type is not categorical!")
        
        missing_entries_present = False
        categories = set([study.get_var(variable) for study in studies])
        if None in categories or "" in categories:
            categories.discard(None)
            categories.discard("")
            missing_entries_present = True
        categories = sorted(list(categories))
        if missing_entries_present: # stick missing at end if present
            categories.append(None)
        
        return categories
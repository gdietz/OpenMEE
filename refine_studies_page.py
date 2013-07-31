from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *

import ui_refine_studies_page

class RefineStudiesPage(QWizardPage, ui_refine_studies_page.Ui_WizardPage):
    def __init__(self, model, parent=None):
        super(RefineStudiesPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        
        self.studies = self.model.get_studies_in_current_order()
        
        self.categorical_variables = self._get_categorical_variables(self.model)
        
        # maps studies to boolean storing whether they are included or not
        self.studies_included_dict = dict([(study, True) for study in self.studies])
        self.items_to_studies = {}
        
        QObject.connect(self.refine_studies_list_widget, SIGNAL("itemChanged(QListWidgetItem*)"), partial(self.change_include_state, section='refine_studies'))
        #QObject.connect(self.refine_studies_list_widget, SIGNAL("itemClicked(QListWidgetItem*)"), self.item_clicked)
            
        
    def initializePage(self):
        # TODO: 
        pass
        self._populate_refine_studies_tab()
    
    def _populate_refine_categories_tab(self):
        self.layout()
    
    
    def _populate_refine_studies_tab(self):
        ''' Adds checkable list of studies to based on their include state'''
        
        for study in self.studies:
            label = study.get_label()
            if label in [None, ""]:
                row = self.model.get_row_assigned_to_study(study)
                label = "Study row %d" % (row+1) # row in model indexed from 0
            item = QListWidgetItem(label)
            self.items_to_studies[item] = study
            #item.setFlags(item.flags()|Qt.ItemIsUserCheckable|Qt.ItemIsTristate)
            item.setCheckState(Qt.Checked if self.studies_included_dict[study] is True else Qt.Unchecked)
            self.refine_studies_list_widget.addItem(item)
            
    def change_include_state(self, item, section=None):
        if section is None:
            raise ValueError
        
        if section == 'refine_studies':
            state = item.checkState()
            study = self.items_to_studies[item]
            
            if state == Qt.Unchecked:
                self.studies_included_dict[study] = False
            elif state == Qt.Checked:
                self.studies_included_dict[study] = True
            else:
                raise ValueError("Should not get here, did I forget to disable signals?")
        elif section == 'refine_categories':
            pass
        
#    def item_clicked(self, item):
#        study = self.items_to_studies[item]
    
    def _get_categorical_variables(self, model):
        cat_cols = self.model.get_categorical_columns()
        cat_vars = [self.model.get_variable_assigned_to_column(col) for col in cat_cols]
        return cat_vars
        
    def categories_of_var(self, studies, variable):
        ''' Returns a list of the categories of a categorical variable'''
        
        if variable.get_type != CATEGORICAL:
            raise ValueError("Variable type is not categorical!")
        
        missing_entries_present = False
        categories = set([study.get_var(variable) for study in studies])
        if None in categories or "" in categories:
            categories.discard(None)
            categories.discard("")
            missing_entries_present = True
        categories = list(categories).sort()
        if missing_entries_present: # stick missing at end if present
            categories.append(None)
        
        return categories
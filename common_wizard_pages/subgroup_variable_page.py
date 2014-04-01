##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

#from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *
import ui_subgroup_variable_page

class SubgroupVariablePage(QWizardPage, ui_subgroup_variable_page.Ui_subgroup_variable_page):
    def __init__(self, model, previous_subgroup_var=None, parent=None):
        super(SubgroupVariablePage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.default_subgroup_var = previous_subgroup_var
        self.subgroup_variable_col = None

        categorical_cols = self.model.get_categorical_columns()
        if len(categorical_cols)==0:
            raise Exception("There are no categorical variables. A subgroup analysis cannot occur")
    
    def initializePage(self):
        self._populate_combo_box(self.model.get_categorical_columns())
        QObject.connect(self.comboBox, SIGNAL("currentIndexChanged(int)"), self._update_current_selection)
        
    def _populate_combo_box(self, columns):
        ''' populates combo box with categorical variable choices '''
        
        self.comboBox.blockSignals(True)
        self.comboBox.clear()
        key_fn = lambda col: self.model.get_variable_assigned_to_column(col).get_label() # sort by column label
        vars_to_cols = {}
        for col in sorted(columns, key=key_fn):
            var = self.model.get_variable_assigned_to_column(col)
            self.comboBox.addItem(var.get_label(), col) # store the chosen col
            vars_to_cols[var] = col
        if self.default_subgroup_var in vars_to_cols.keys():
            self.comboBox.setCurrentIndex(self.comboBox.findData(vars_to_cols[var]))
        else:
            self.comboBox.setCurrentIndex(0)
        self.comboBox.blockSignals(False)
        
        self._update_current_selection()


    def _update_current_selection(self):
        self.subgroup_variable_col = self.selected_column(self.comboBox)
        
    def get_subgroup_variable_col(self):
        return self.subgroup_variable_col
    
    def get_subgroup_variable(self):
        if self.subgroup_variable_col is None:
            return None
        return self.model.get_variable_assigned_to_column(self.subgroup_variable_col)
        
    
    def selected_column(self, combo_box):
        item_data = combo_box.itemData(combo_box.currentIndex())
        selected_column = item_data.toInt()[0]
        if selected_column == -1:
            return None
        return selected_column

    def __str__(self):
        return "Subgroup Variable: %s" % self.get_subgroup_variable().get_label()


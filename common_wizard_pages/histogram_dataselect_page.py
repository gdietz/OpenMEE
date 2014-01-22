import sys
from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from ome_globals import *

import ui_histogram_dataselect_page

class HistogramDataSelectPage(QWizardPage, ui_histogram_dataselect_page.Ui_WizardPage):
    def __init__(self, model, prev_hist_var=None, parent=None):
        super(HistogramDataSelectPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.prev_hist_var = prev_hist_var
        
        self._populate_combo_box()

        
    def _populate_combo_box(self):
        ''' populates combo box with numerical variables '''
        
        vars= self.model.get_variables()
        vars.sort(key=lambda var: var.get_label())
        
        default_index = 0
        for var in vars:
            # store column of var in user data
            col = self.model.get_column_assigned_to_variable(var)
            self.comboBox.addItem(var.get_label(), userData=QVariant(col))
            index_of_item = self.comboBox.count()-1
            if self.prev_hist_var == var:
                default_index = index_of_item
        # set default selection if given
        self.comboBox.setCurrentIndex(default_index)
        
        self.completeChanged.emit()
        
    def isComplete(self):
        return True
        
    def get_selected_var(self):
        idx = self.comboBox.currentIndex()
        data = self.comboBox.itemData(idx)
        col = data.toInt()[0]
        return self.model.get_variable_assigned_to_column(col)
        
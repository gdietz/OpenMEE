'''
Created on Feb 12, 2014

@author: george
'''


from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_contingency_table

from ome_globals import CATEGORICAL

class ContingencyTableDlg(QDialog, ui_contingency_table.Ui_Dialog):
    def __init__(self, model, parent=None):
        super(ContingencyTableDlg, self).__init__(parent)
        self.setupUi(self)
        
        self.model= model
        
        self.categorical_vars = sorted(self.model.get_variables(var_type=CATEGORICAL),key= lambda var: var.get_label())
        
        
        self._populate_combo_box(self.horizontal_comboBox, self.categorical_vars, 0)
        self._populate_combo_box(self.vertical_comboBox, self.categorical_vars, 1)
        self._rebuild_table()
        
        self.horizontal_comboBox.currentIndexChanged.connect(self._rebuild_table)
        self.vertical_comboBox.currentIndexChanged.connect(self._rebuild_table)
        
    def _populate_combo_box(self, box, variables, startindex=0):
        # store var by var index
        
        box.blockSignals(True)
        box.addItems([var.get_label() for var in variables])
        box.setCurrentIndex(startindex)
        box.blockSignals(False)
        
    def _get_values_of_variable(self, var):
        studies = self.model.get_studies_in_current_order()
        return [study.get_var(var) for study in studies]
        
    def _rebuild_table(self, discard_None=True, discard_empty_string=True):
        
        self.tableWidget.blockSignals(True)
        self.tableWidget.clear()
        
        vert_var = self.categorical_vars[self.vertical_comboBox.currentIndex()]
        horz_var = self.categorical_vars[self.horizontal_comboBox.currentIndex()]
        
        vert_var_vals = self._get_values_of_variable(vert_var)
        horz_var_vals = self._get_values_of_variable(horz_var)
        
        vert_levels = set(vert_var_vals)
        horz_levels = set(horz_var_vals)
        if discard_None:
            vert_levels.discard(None)
            horz_levels.discard(None)
        if discard_empty_string:
            vert_levels.discard("")
            horz_levels.discard("")
        # sort alphanetically
        vert_levels = sorted(vert_levels)
        horz_levels = sorted(horz_levels)
        
        # headers and table dimensions
        self.tableWidget.setRowCount(len(vert_levels))
        self.tableWidget.setColumnCount(len(horz_levels))
        self.tableWidget.setHorizontalHeaderLabels(horz_levels)
        self.tableWidget.setVerticalHeaderLabels(vert_levels)
        
        ### Count # of studies
        # initialize counts
        study_counts = {}
        for hlevel in horz_levels:
            study_counts[hlevel]={}
            for vlevel in vert_levels:
                study_counts[hlevel][vlevel]=0
    
        # Do the counting
        for h_val, v_val in zip(horz_var_vals, vert_var_vals):
            try:
                study_counts[h_val][v_val] += 1
            except KeyError:
                # Error will be due to None or "" being in the data, we just don't count studies with those
                pass
        
        # Make the table items
        for col, hlevel in enumerate(horz_levels):
            for row, vlevel in enumerate(vert_levels):
                item = QTableWidgetItem("%d studies" % study_counts[hlevel][vlevel])
                self.tableWidget.setItem(row, col, item)
        
        self.tableWidget.blockSignals(False)
        self.adjustSize()
            
            
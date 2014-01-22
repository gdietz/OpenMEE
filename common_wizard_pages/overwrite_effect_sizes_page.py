from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *
import ui_overwrite_effect_sizes_page


class OverwriteEffectSizesPage(QWizardPage, ui_overwrite_effect_sizes_page.Ui_WizardPage):
    def __init__(self, model, parent=None):
        super(OverwriteEffectSizesPage, self).__init__(parent)
        self.setupUi(self)
        self.frame.hide()
        self.same_col_grp_lbl.hide()
        self.same_col_grp_lbl.setStyleSheet("QLabel { color : red; }");
        
        self.model = model
        self.trans_effect_columns = self.model.get_trans_effect_columns()
        self.trans_var_columns = self.model.get_trans_var_columns()
        # sort alphabetically
        self.trans_effect_columns = self._sort_col_list_alphabetically(self.trans_effect_columns)
        self.trans_var_columns = self._sort_col_list_alphabetically(self.trans_var_columns)
        
        # populate combo boxes
        self._populate_combo_box(box=self.effect_cbo_box, columns=self.trans_effect_columns)
        self._populate_combo_box(box=self.var_cbo_box, columns=self.trans_var_columns)
        
        # connect signals
        self.yes_btn.clicked.connect(self.completeChanged.emit)
        self.no_btn.clicked.connect(self.completeChanged.emit)
        self.effect_cbo_box.currentIndexChanged.connect(self.completeChanged.emit)
        self.var_cbo_box.currentIndexChanged.connect(self.completeChanged.emit)
        
    
    def _sort_col_list_alphabetically(self, col_list):
        col_list = list(col_list)
        key_fn = lambda col: self.model.get_variable_assigned_to_column(col).get_label()
        return sorted(col_list, key=key_fn)
        
    def _populate_combo_box(self, box, columns):
        box.blockSignals(True)
        for col in columns:
            var = self.model.get_variable_assigned_to_column(col)
            box.addItem(var.get_label(), userData=QVariant(col))
        box.blockSignals(False)
 
    def get_columns_to_overwrite(self):
        if self.no_btn.isChecked():
            return None
        
        trans_effect_index = self.effect_cbo_box.currentIndex()
        trans_var_index = self.var_cbo_box.currentIndex()
        
        if -1 in [trans_effect_index, trans_var_index]:
            return None
        
        trans_effect_col = self.effect_cbo_box.itemData(trans_effect_index).toInt()[0]
        trans_var_col = self.var_cbo_box.itemData(trans_var_index).toInt()[0]
        
        cols_to_overwrite = {TRANS_EFFECT:trans_effect_col,
                             TRANS_VAR:trans_var_col}
        
        if self.cols_belong_to_same_col_group(cols_to_overwrite):
            self.same_col_grp_lbl.hide()
        else:
            self.same_col_grp_lbl.show()
        return cols_to_overwrite


    def cols_belong_to_same_col_group(self, cols_to_overwrite):
        if cols_to_overwrite is None:
            return False
        
        col_groups = set()
        col_group_list = []
        for col in cols_to_overwrite.values():
            var = self.model.get_variable_assigned_to_column(col)
            col_grp = self.model.get_variable_group_of_var(var)
            
            col_groups.add(col_grp)
            col_group_list.append(col_grp)
        
        return len(col_groups) == 1

    def isComplete(self):
        if self.no_btn.isChecked():
            return True
        elif self.yes_btn.isChecked():
            cols_to_overwrite = self.get_columns_to_overwrite()
            if cols_to_overwrite:
                return True
        return False
    
    def print_cols_to_overwrite(self):
        print("cols to overwrite is now %s" % str(self.get_columns_to_overwrite()))
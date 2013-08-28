
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *

import ui_effect_size_locations_page



class EffectSizeLocationsPage(QWizardPage, ui_effect_size_locations_page.Ui_wizardPage):
    def __init__(self, model, parent=None):
        super(EffectSizeLocationsPage, self).__init__(parent)
        
        self.model = model
        
        self.continuous_columns = self.model.get_continuous_columns()
        
        self.raw_combo_boxes = [self.raw_effect_cbo_box,
                                self.raw_lower_cbo_box,
                                self.raw_upper_cbo_box]
        self.trans_combo_boxes = [self.trans_effect_cbo_box,
                                  self.trans_var_cbo_box]
        
        
    def initializePage(self):
        if self.wizard().direction == RAW_TO_TRANS:
            # Enable appropriate half of menu
            self.raw_grp_box.setEnabled(True)
            self.trans_grp_box.setEnabled(False)
            
            self._populate_combo_boxes(self.raw_combo_boxes, self.continuous_columns)
        elif self.wizard().direction == TRANS_TO_RAW:
            self.trans_grp_box.setEnabled(True)
            self.raw_grp_box.setEnabled(False)
            
            self._populate_combo_boxes(self.trans_combo_boxes, self.continuous_columns)
            
        else:
            raise Exception("Direction of transformation not recognized")
        
    
    def _populate_combo_boxes(self, combo_boxes, columns):
        ''' Populates combo boxes that are 'continuous' with list of continuous
        -type columns'''
        
        for box in combo_boxes:
            box.blockSignals(True)
            box.clear()
            box.addItem("", QVariant(-1)) # -1 meaning no choice
            key_fn = lambda col: self.model.get_variable_assigned_to_column(col).get_label() # sort by column label
            for col in sorted(columns, key=key_fn):
                var = self.model.get_variable_assigned_to_column(col)
                box.addItem(var.get_label(), col) # store the chosen col
            box.setCurrentIndex(0)
            box.blockSignals(False)
            
        self._set_default_choices_for_combo_boxes(combo_boxes, columns)
        
        
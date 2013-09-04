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

import ui_new_column_group_transform_effect_page

class NewColumnGroupTransformEffectPage(QWizardPage, ui_new_column_group_transform_effect_page.Ui_WizardPage):
    def __init__(self, model, parent=None):
        super(NewColumnGroupTransformEffectPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.metric = None
        
        self.selections = {TRANS_EFFECT:None,
                           TRANS_VAR:None,
                           RAW_EFFECT:None,
                           RAW_LOWER:None,
                           RAW_UPPER:None}
        
        self.box_to_selection_key = {self.trans_effect_cbo_box:TRANS_EFFECT,
                                     self.trans_var_cbo_box:TRANS_VAR,
                                     self.raw_effect_cbo_box:RAW_EFFECT,
                                     self.raw_lower_cbo_box:RAW_LOWER,
                                     self.raw_upper_cbo_box:RAW_UPPER}
        
        self.trans_effect_columns = self._get_subtype_columns(TRANS_EFFECT)
        self.trans_var_colums     = self._get_subtype_columns(TRANS_VAR)
        self.raw_effect_columns   = self._get_subtype_columns(RAW_EFFECT)
        self.raw_lower_columns    = self._get_subtype_columns(RAW_LOWER)
        self.raw_upper_colums     = self._get_subtype_columns(RAW_UPPER)
        
        self.trans_boxes = [self.trans_effect_cbo_box, self.trans_var_cbo_box]
        self.raw_boxes = [self.raw_effect_cbo_box, self.raw_lower_cbo_box, self.raw_upper_cbo_box]
    
    
    def _get_subtype_columns(self, subtype, exclude_if_already_in_group=True):
        continuous_columns = self.model.get_continuous_columns()
        subtype_cols = [col for col in continuous_columns if self.model.get_variable_assigned_to_column(col).get_subtype() == subtype]
        
        if exclude_if_already_in_group:
            subtype_cols = [col for col in subtype_cols if self.model.get_variable_assigned_to_column(col).get_column_group() is None]
        return subtype_cols
        
    
    def initializePage(self):
        # set info for wizard
        self.wizard().get_new_column_group_column_selections = self.get_selections
        self.wizard().new_column_group = True
        self.wizard().get_new_column_group_metric = self.get_metric
        
        # local data
        self.direction = self.wizard().get_transformation_direction()
        self.effect_var_col = self.wizard().get_chosen_column()

        if self.direction == TRANS_TO_RAW:
            self.raw_grp_box.setVisible(False)
            self.trans_grp_box.setVisible(True)
            self._add_chosen_effect_col_to_box_then_disable_it(self.trans_effect_cbo_box, self.effect_var_col)
            self._populate_combo_box(self.trans_var_cbo_box, self.trans_var_colums)
        elif self.direction == RAW_TO_TRANS:
            self.raw_grp_box.setVisible(True)
            self.trans_grp_box.setVisible(False)
            self._add_chosen_effect_col_to_box_then_disable_it(self.raw_effect_cbo_box, self.effect_var_col)
            self._populate_combo_box(self.raw_lower_cbo_box,  self.raw_lower_columns)
            self._populate_combo_box(self.raw_upper_cbo_box,  self.raw_upper_colums)

        for box in self.trans_boxes + self.raw_boxes:
            QObject.connect(box, SIGNAL("currentIndexChanged(int)"), partial(self._update_selection, box))
    
        self._populate_metric_box(self.metric_cbo_box)
        self.metric_cbo_box.currentIndexChanged[int].connect(self._update_metric_choice)
        
    def _update_selection(self, box):
        self.selections[self.box_to_selection_key[box]] = self._selected_column(box)
        
        self.completeChanged.emit()
        
    def _update_metric_choice(self):
        item_data = self.metric_cbo_box.itemData(self.metric_cbo_box.currentIndex())
        self.metric = item_data.toInt()[0]
        
        
        self.completeChanged.emit()
    
    def isComplete(self):
        if self.direction == TRANS_TO_RAW:
            return None not in [self.selections[TRANS_EFFECT], self.selections[TRANS_VAR]]
        elif self.direction == RAW_TO_TRANS:
            return None not in [self.selections[RAW_EFFECT], self.selections[RAW_LOWER], self.selections[RAW_UPPER]]
    
    def get_selections(self):
        return self.selections
    
    def get_metric(self):
        return self.metric
        
    def _selected_column(self, combo_box):
        item_data = combo_box.itemData(combo_box.currentIndex())
        selected_column = item_data.toInt()[0]
        if selected_column == -1:
            return None
        return selected_column
    
    def _populate_combo_box(self, box, columns):
        box.blockSignals(True)
        box.clear()
        box.addItem("", QVariant(-1)) # -1 meaning no choice
        key_fn = lambda col: self.model.get_variable_assigned_to_column(col).get_label() # sort by column label
        for col in sorted(columns, key=key_fn):
            var = self.model.get_variable_assigned_to_column(col)
            box.addItem(var.get_label(), col) # store the chosen col
        box.setCurrentIndex(0)
        box.blockSignals(False)
        
    def _populate_metric_box(self, box):
        metrics = METRIC_TEXT_SIMPLE.keys()
        metrics.sort(key=lambda metric:METRIC_TEXT_SIMPLE[metric])
        
        box.blockSignals(True)
        box.clear()
        for metric in metrics:
            box.addItem(METRIC_TEXT_SIMPLE[metric], metric)
        box.setCurrentIndex(0)
        box.blockSignals(False)
        
        self._update_metric_choice()
        
    def _add_chosen_effect_col_to_box_then_disable_it(self, box, column):
        box.blockSignals(True)
        box.clear()
        var = self.model.get_variable_assigned_to_column(column)
        box.addItem(var.get_label(), column) # store the chosen col
        box.setCurrentIndex(0)
        box.setEnabled(False)
        box.blockSignals(False)
        
        self._update_selection(box)
##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

import ui_transform_effect_summary_page



class TransformEffectSummaryPage(QWizardPage, ui_transform_effect_summary_page.Ui_WizardPage):
    def __init__(self, parent=None):
        super(TransformEffectSummaryPage, self).__init__(parent)
        self.setupUi(self)
        
    def initializePage(self):
        model = self.wizard().model
        chosen_var = model.get_variable_assigned_to_column(self.wizard().get_chosen_column())
        direction = self.wizard().get_transformation_direction()
        verify_transform_direction(direction)
        
        from_str, to_str = "Raw Scale","Transformed Scale"
        if direction == TRANS_TO_RAW:
            from_str, to_str = to_str, from_str # reverse the strings
        
        self.from_column_lbl.setText(chosen_var.get_label())
        self.from_scale_lbl.setText(from_str)
        self.to_scale_lbl.setText(to_str)
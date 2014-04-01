import sys
#from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *
import ui_scatterplot_dataselect_page

# prev_scatterplot_data is a dictionary: {'x':var1, 'y':var2}
#                 
class ScatterplotDataSelectPage(QWizardPage, ui_scatterplot_dataselect_page.Ui_WizardPage):
    def __init__(self, model, prev_scatterplot_data=None, parent=None):
        super(ScatterplotDataSelectPage, self).__init__(parent)
        self.setupUi(self)
        
        if prev_scatterplot_data:
            self.prev_x = prev_scatterplot_data['x']
            self.prev_y = prev_scatterplot_data['y']
        else:
            self.prev_x, self.prev_y, = None, None
            
        self.model = model
        self.prev_scatterplot_data = prev_scatterplot_data
        
        self._populate_combo_boxes()

    def _populate_combo_boxes(self):
        self._populate_combo_box(self.x_cbo_box, self.prev_x)
        self._populate_combo_box(self.y_cbo_box, self.prev_y)
    
    def _populate_combo_box(self, box, prev_var):
        ''' populates combo box with numerical variables '''
        
        cont_vars = self.model.get_variables(var_type=CONTINUOUS)
        count_vars = self.model.get_variables(var_type=COUNT)
        variables = cont_vars + count_vars
        variables.sort(key=lambda var: var.get_label())
        
        default_index = 0
        for var in variables:
            # store column of var in user data
            col = self.model.get_column_assigned_to_variable(var)
            box.addItem(var.get_label(), userData=QVariant(col))
            index_of_item = box.count()-1
            if prev_var == var:
                default_index = index_of_item
        # set default selection if given
        box.setCurrentIndex(default_index)
        
        self.completeChanged.emit()
        
    def get_selected_vars(self):
        idx = self.x_cbo_box.currentIndex()
        data = self.x_cbo_box.itemData(idx)
        xcol = data.toInt()[0]
        xvar = self.model.get_variable_assigned_to_column(xcol)
        
        idx = self.y_cbo_box.currentIndex()
        data = self.y_cbo_box.itemData(idx)
        ycol = data.toInt()[0]
        yvar = self.model.get_variable_assigned_to_column(ycol)
        
        return {'x':xvar,
                'y':yvar}
        
    def isComplete(self):
        return True
    
    def __str__(self):
        return "" # don't want summary data
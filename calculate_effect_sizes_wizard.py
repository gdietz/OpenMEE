#################
#               #
# George Dietz  #
# CEBM@Brown    #
#               #
#################

#from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *
from choose_effect_size_page import ChooseEffectSizePage
from data_location_page import DataLocationPage
from overwrite_effect_sizes_page import OverwriteEffectSizesPage

Page_ChooseEffectSize, Page_DataLocation, Page_OverwriteEffectSizes = range(3)
class CalculateEffectSizeWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(CalculateEffectSizeWizard, self).__init__(parent)
        
        self.model = model
        
        self.setPage(Page_ChooseEffectSize, ChooseEffectSizePage(model=model))
        self.setPage(Page_DataLocation, DataLocationPage(model=model, mode=CALCULATE_EFFECT_SIZE_MODE))
        self.setPage(Page_OverwriteEffectSizes, OverwriteEffectSizesPage(model=model))
        self.setStartId(Page_ChooseEffectSize)
        self.setWizardStyle(QWizard.ClassicStyle)
        
        self.selected_data_type = None
        self.selected_metric = None
        self.data_location = None
        self.cols_to_overwrite = None # cols (effect and var to overwrite) if any
        
        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size) # adjust window to proper size

        self.setWindowTitle("Calculate Effect Size Wizard")
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()
        
    def nextId(self):
        if self.currentId() == Page_ChooseEffectSize:
            return Page_DataLocation
        elif self.currentId() == Page_DataLocation:
            if self.effect_and_var_cols_exist():
                return Page_OverwriteEffectSizes
            else:
                return -1
        elif self.currentId() == Page_OverwriteEffectSizes:
            return -1
        
    def effect_and_var_cols_exist(self):
        self.trans_effect_columns = self.model.get_trans_effect_columns()
        self.trans_var_columns = self.model.get_trans_var_columns()
        
        if (len(self.trans_effect_columns) > 0) and (len(self.trans_var_columns) > 0):
            return True
        return False

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = CalculateEffectSizeWizard(None)
    wizard.show()
    sys.exit(app.exec_())
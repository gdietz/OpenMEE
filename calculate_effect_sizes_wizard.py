#################
#               #
# George Dietz  #
# CEBM@Brown    #
#               #
#################

#from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *
from common_wizard_pages.choose_effect_size_page import ChooseEffectSizePage
from common_wizard_pages.data_location_page import DataLocationPage
from common_wizard_pages.overwrite_effect_sizes_page import OverwriteEffectSizesPage

Page_ChooseEffectSize, Page_DataLocation, Page_OverwriteEffectSizes = range(3)


class CalculateEffectSizeWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(CalculateEffectSizeWizard, self).__init__(parent)

        self.model = model
        last_analysis = model.get_last_analysis_selections()
        
        self.choose_effect_size_page = ChooseEffectSizePage(
                        data_type=last_analysis['data_type'],
                        metric=last_analysis['metric'])
        self.data_location_page = DataLocationPage(model=model,
                                                   linkage_checkbox=True,
                                                   effect_size=False)
        self.overwrite_effect_sizes_page = OverwriteEffectSizesPage(model=model)
        
        self.setPage(Page_ChooseEffectSize, self.choose_effect_size_page)
        self.setPage(Page_DataLocation, self.data_location_page)
        self.setPage(Page_OverwriteEffectSizes, self.overwrite_effect_sizes_page)
        self.setStartId(Page_ChooseEffectSize)
        self.setWizardStyle(QWizard.ClassicStyle)

        # adjust window to proper size
        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size)

        self.setWindowTitle("Calculate Effect Size Wizard")

    def _change_size(self):
        print("changing size")
        self.adjustSize()
        
    def get_data_location(self):
        return self.data_location_page.get_data_locations()
    
    def get_columns_to_overwrite(self):
        return self.overwrite_effect_sizes_page.get_columns_to_overwrite()

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
        
    def get_data_type_and_metric(self):
        ''' returns tuple (data_type, metric) '''
        return self.choose_effect_size_page.get_data_type_and_metric()
    
    def make_link(self):
        return self.data_location_page.should_make_link()
    
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

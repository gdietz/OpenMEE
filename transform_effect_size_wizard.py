
#from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *
from choose_effect_size_page import ChooseEffectSizePage
#from data_location_page import DataLocationPage USE new locations page for this purpose

Page_ChooseEffectSize, Page_DataLocation = range(2)
class TransformEffectSizeWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(TransformEffectSizeWizard, self).__init__(parent)
        
        self.setPage(Page_ChooseEffectSize, ChooseEffectSizePage())
        
        #self.setPage(Page_DataLocation, DataLocationPage(model=model))
        self.setStartId(Page_ChooseEffectSize)
        self.setWizardStyle(QWizard.ClassicStyle)
        
        self.selected_data_type = None
        self.selected_metric = None
        self.data_location = None
        
        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size)
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()
        
    def nextId(self):
        if self.currentId() == Page_ChooseEffectSize:
            return Page_DataLocation
        elif self.currentId() == Page_DataLocation:
            return -1
        

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = CalculateEffectSizeWizard(None)
    wizard.show()
    sys.exit(app.exec_())
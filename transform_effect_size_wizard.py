
#from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *
from choose_effect_col_for_transformation_page import ChooseEffectColForTransformationPage
from new_column_group_transform_effect_page import NewColumnGroupTransformEffectPage

(Page_ChooseEffectColForTransformation, Page_NewColumnGroupTransformEffect) = range(1)
class TransformEffectSizeWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(TransformEffectSizeWizard, self).__init__(parent)
    
        self.setPage(Page_ChooseEffectColForTransformation, ChooseEffectColForTransformationPage(model=model))
        self.setPage(Page_NewColumnGroupTransformEffect, NewColumnGroupTransformEffectPage(model=model))
        
        self.setStartId(Page_ChooseEffectColForTransformation)
        self.setWizardStyle(QWizard.ClassicStyle)
        
        self.get_chosen_column = None #will be a callable
        self.get_new_column_group_column_selections = None
        self.new_column_group = False
        
        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size)
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()
        
    def nextId(self):
        if self.currentId() == Page_ChooseEffectColForTransformation:
            if self._col_belongs_to_group(self.get_chosen_column()): 
                return -1
            else:
                return Page_NewColumnGroupTransformEffect
        elif self.currentId() == Page_NewColumnGroupTransformEffect:
            return -1
        
    def _col_belongs_to_group(self, col):
        var = self.model.get_variable_assigned_to_column(col)
        return var.get_column_group() is not None
        
    def get_tranformation_direction(self):
        var = self.model.get_variable_assigned_to_column(self.get_chosen_column())
        var_subtype = var.get_subtype()
        if var_subtype == TRANS_EFFECT:
            return TRANS_TO_RAW
        elif var_subtype == RAW_EFFECT:
            return RAW_TO_TRANS
        else:
            raise Exception("Unrecognized transformation direction")
        
        return None
        

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = TransformEffectSizeWizard(None)
    wizard.show()
    sys.exit(app.exec_())
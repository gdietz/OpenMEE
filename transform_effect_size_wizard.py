##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
##################

#from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *
from common_wizard_pages.choose_effect_col_for_transformation_page import ChooseEffectColForTransformationPage
from common_wizard_pages.new_column_group_transform_effect_page import NewColumnGroupTransformEffectPage
from common_wizard_pages.transform_effect_summary_page import TransformEffectSummaryPage

(Page_ChooseEffectColForTransformation, Page_NewColumnGroupTransformEffect,
Page_TransformEffectSummary) = range(3)
class TransformEffectSizeWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(TransformEffectSizeWizard, self).__init__(parent)
        
        self.model=model
    
        
        self.choose_effect_col_for_transformation_page = ChooseEffectColForTransformationPage(model=model)
        self.new_col_grp_transform_effect_page = NewColumnGroupTransformEffectPage(model=model)
        self.tranform_effect_summary_page = TransformEffectSummaryPage()
        
        self.setPage(Page_ChooseEffectColForTransformation, self.choose_effect_col_for_transformation_page)
        self.setPage(Page_NewColumnGroupTransformEffect, self.new_col_grp_transform_effect_page)
        self.setPage(Page_TransformEffectSummary, self.tranform_effect_summary_page)
        
        self.setStartId(Page_ChooseEffectColForTransformation)
        self.setWizardStyle(QWizard.ClassicStyle)
        
        self.setWindowTitle("Transform Effect Size")
        
        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size)
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()
    
    ############### new col group transform effect page #######################
    #                                                                         #
    def make_new_column_group(self):
        return self.new_col_grp_transform_effect_page.make_new_column_group()
    
    def get_new_column_group_column_selections(self):
        return self.new_col_grp_transform_effect_page.get_selections()
    
    def get_new_column_group_metric(self):
        return self.new_col_grp_transform_effect_page.get_metric()
    #                                                                         #
    ############ end of new col group transform effect page ###################
        
    def nextId(self):
        if self.currentId() == Page_ChooseEffectColForTransformation:
            print("on page choose effect col for transformation")
            if self.get_chosen_column is None:
                print("  get chosen column undefined, next page is sumary")
                return Page_TransformEffectSummary
            elif self._col_belongs_to_group(self.get_chosen_column()):
                print("  col belongs to group, next page is summary")
                return Page_TransformEffectSummary
            else:
                print("next page is Page_NewColumnGroupTransformEffect")
                return Page_NewColumnGroupTransformEffect
        elif self.currentId() == Page_NewColumnGroupTransformEffect:
            print("on page new column group transform effect")
            return Page_TransformEffectSummary
        elif self.currentId() == Page_TransformEffectSummary:
            return -1
        
    def _col_belongs_to_group(self, col):
        if col is None:
            return False
        var = self.model.get_variable_assigned_to_column(col)
        return self.model.get_variable_group_of_var(var) is not None

    def get_transformation_direction(self):
        return self.choose_effect_col_for_transformation_page.get_transformation_direction()
    
    def get_chosen_column(self):
        return self.choose_effect_col_for_transformation_page.get_chosen_column()
        

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = TransformEffectSizeWizard(None)
    wizard.show()
    sys.exit(app.exec_())
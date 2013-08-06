from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *

from choose_effect_size_page import ChooseEffectSizePage
from data_location_page import DataLocationPage
from refine_studies_page import RefineStudiesPage
from methods_and_parameters_page import MethodsAndParametersPage

Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies, Page_MethodsAndParameters = range(4)
class MetaAnalysisWizard(QtGui.QWizard):
    def __init__(self, model, meta_f_str=None, parent=None):
        super(MetaAnalysisWizard, self).__init__(parent)
        
        self.model = model
        self.meta_f_str = meta_f_str
        
        self.selected_data_type = None
        self.selected_metric = None
        self.data_location = None
        self.studies_included_table = None # dict mapping studies to if their inclusion state
        
        
        self.methods_and_params_page_instance = MethodsAndParametersPage(model=model, meta_f_str=meta_f_str)
        
        self.setPage(Page_ChooseEffectSize, ChooseEffectSizePage(add_generic_effect=True))
        self.setPage(Page_DataLocation,     DataLocationPage(model=model, enable_ma_wizard_options=True))
        self.setPage(Page_RefineStudies,    RefineStudiesPage(model=model))
        self.setPage(Page_MethodsAndParameters, self.methods_and_params_page_instance)
        
        self.setStartId(Page_ChooseEffectSize)
        self.setWizardStyle(QWizard.ClassicStyle)
        

        
        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size)
    
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()
        
    def get_plot_params(self):
        return self.methods_and_params_page_instance.get_plot_params()
    
    def get_current_method(self):
        return self.methods_and_params_page_instance.get_current_method()
        
    def get_included_studies_in_proper_order(self):
        all_studies = self.model.get_studies_in_current_order()
        included_studies = [study for study in all_studies if self.studies_included_table[study]==True]
        return included_studies


    def nextId(self):
        if self.currentId() == Page_ChooseEffectSize:
            return Page_DataLocation
        elif self.currentId() == Page_DataLocation:
            return Page_RefineStudies
        elif self.currentId() == Page_RefineStudies:
            return Page_MethodsAndParameters
        elif self.currentId() == Page_MethodsAndParameters:
            return -1
        

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = MetaAnalysisWizard(parent=None)
    wizard.show()
    sys.exit(app.exec_())
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *

import python_to_R
import ui_methods_and_parameters_page

class MethodsAndParametersPage(QWizardPage, ui_methods_and_parameters_page.Ui_WizardPage):
    def __init__(self, model, parent=None):
        super(MethodsAndParametersPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        
    def initializePage(self):
        self.data_type = self.wizard().data_type
        self.metric = self.wizard().metric
        
        if self.data_type != TWO_BY_TWO_CONTINGENCY_TABLE:
            self.disable_bin_only_fields()
            
    def disable_bin_only_fields(self):
        self.col3_str_edit.setEnabled(False)
        self.col4_str_edit.setEnabled(False)
        self.show_3.setChecked(False)
        self.show_3.setEnabled(False)
        self.show_4.setChecked(False)
        self.show_4.setEnabled(False)
        
    def populate_cbo_box(self):
        # we first build an R object with the current data. this is to pass off         
        # to the R side to check the feasibility of the methods over the current data.
        # i.e., we do not display methods that cannot be performed over the 
        # current data.
        tmp_obj_name = "tmp_obj" 
        if self.data_type == "binary":
            python_to_R.ma_dataset_to_simple_binary_robj(self.model, var_name=tmp_obj_name)
        elif self.data_type == "continuous":
            python_to_R.ma_dataset_to_simple_continuous_robj(self.model, var_name=tmp_obj_name)
            
        self.available_method_d = python_to_R.get_available_methods(
                                                for_data_type=self.data_type,
                                                data_obj_name=tmp_obj_name,
                                                metric=self.metric)
        print "\n\navailable %s methods: %s" % (self.data_type, ", ".join(self.available_method_d.keys()))
        method_names = self.available_method_d.keys()
        method_names.sort(reverse=True)
        
        for method in method_names:
            self.method_cbo_box.addItem(method)
        self.current_method = self.available_method_d[str(cbo_box.currentText())]
        self.setup_params()
        self.parameter_grp_box.setTitle(self.current_method)

        
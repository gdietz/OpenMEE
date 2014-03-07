'''
Created on Jan 11, 2014

@author: George
'''




from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from meta_regression_wizard import *
from model_building.instructions import InstructionsPage
from model_building.add_models_page import AddModelsPage

(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
Page_MetaRegDetails, Page_SelectCovariates, Page_ReferenceValues,
Page_Bootstrap, Page_Summary, Page_CondMeans, Page_AddModels,
Page_Instructions) = range(11)

class ModelBuildingWizard(MetaRegressionWizard):
    def __init__(self, model, parent=None):
        MetaRegressionWizard.__init__(self, model=model, parent=parent)
        
        self.analysis_label="Model Building"
        self.setWindowTitle(self.analysis_label)
        
        # Add models page
        self.add_models_page = AddModelsPage()
        self.setPage(Page_AddModels, self.add_models_page)
        
        # Instructions page
        self.instructions_page = InstructionsPage()
        self.setPage(Page_Instructions, self.instructions_page)
        
        # Reconfigure meta regression details page a  bit
        self.meta_reg_details_page.parametric_radioButton.setChecked(True)
        self.meta_reg_details_page.analysis_type_groupBox.setEnabled(False)
        self.meta_reg_details_page.conditional_means_checkBox.setChecked(False)
        self.meta_reg_details_page.output_type_groupBox.setEnabled(False)
        
    def nextId(self):
        current_id = self.currentId()
        
        return self.nextId_helper(current_id)
        
    def nextId_helper(self, page_id):
        if page_id == Page_ChooseEffectSize:
            return Page_DataLocation
        elif page_id == Page_DataLocation:
            return Page_RefineStudies
        elif page_id == Page_RefineStudies:
            return Page_MetaRegDetails
        elif page_id == Page_MetaRegDetails:
            return Page_Instructions
        elif page_id == Page_Instructions:
            return Page_SelectCovariates
        elif page_id == Page_SelectCovariates:
            if self._categorical_covariates_selected():
                return Page_ReferenceValues
            else:
                return Page_AddModels
        elif page_id == Page_ReferenceValues:
            return Page_AddModels
        elif page_id == Page_AddModels:
            return Page_Summary
        elif page_id == Page_Summary:
            return -1
    
    def get_models_info(self):
        return self.add_models_page.get_models_info()
        
# Old ideas. They might be useful in the future. 
# Pages:
# 1) Specify saturated model covariates and add interaction terms
# 2) Specify models by on a dialog. The models will show up in a list on the
#    left. There will be a button "new model" which will pop-up a dialog which
#    prompts the user for a name and which covariates and interaction terms
#    will be used. The combination of covariates and interaction terms must be
#    unique for each model. Also, each subsequent model must be a subset of the
#    previous model
# 3) The rest will be like the meta-regression wizard but:
#    a) The list of available studies to include will be filtered by those that
#       have data for all the covariates specified.
#    b) The "Select covariates for regression" page will not be present. (The
#       params previously specified there (conf. level and fixed vs. random
#       effects will be found on page #2 (the specify models dialog)
#
# 4) The rest will be like the normal meta-regression wizard
#
# Results:
#   Option A: Show results in a table (see jessica email) with each successive
#     model i.e. the reverse of the order that they were entered.
#
#
#   Option B: For all possible combinations: (NO LONGER GOING TO IMPLEMENT, for now ....)
# A lower-triangular table labeled with model names on each axis. The main
# diagonal will be blank. Clicking a square will show the results output on the
# right hand side of the dialog. (exportable like the results_window)
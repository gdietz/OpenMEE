'''
Created on Jan 11, 2014

@author: George
'''

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
# Progress:
# Page  ui-designed page_code
#  1       [X]         [ ] 
#  2       [X]         [ ]
#  3a      [ ]         [ ]
#  3b      [X]         [ ]
#  4       [ ]         [ ]
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
#

# from PyQt4 import QtCore, QtGui
# from PyQt4.Qt import *
# 
# # Should use relative import here but eclipse doesn't seem to like it
# from common_wizard_pages.choose_effect_size_page import ChooseEffectSizePage
# #from data_location_page import DataLocationPage
# from common_wizard_pages.refine_studies_page import RefineStudiesPage, StudyFilter
# from common_wizard_pages.reference_value_page import ReferenceValuePage
# from common_wizard_pages.summary_page import SummaryPage
# 
# 
# # Histogram wizard ids
# [Page_SaturatedModelPage, Page_AddModelsPage,
# Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
# Page_PageReferenceValues, Page_Summary] = range(7)
# 
# class ModelBuildingWizard(QtGui.QWizard):
#     def __init__(self, model, parent=None):
#         super(ModelBuildingWizard, self).__init__(parent)
#         
#         last_analysis = model.get_last_analysis_selections()
#         self.saturated_model_page = SaturatedModelPage(model=model)
#         self.add_models_page = AddModelsPage()
#         self.choose_effect_size_page = ChooseEffectSizePage(
#             add_generic_effect=True,
#             data_type=last_analysis['data_type'],
#             metric=last_analysis['metric']
#             var_groups = model.get_variable_groups())
#         self.data_location_page = EffectSizeAndVarLocationPage(model=model)
#         self.refine_studies_page = RefineStudiesPage(model=model)
#         self.summary_page = SummaryPage()
#         
#         self.setPage(Page_SaturatedModelPage, self.saturated_model_page)
#         self.setPage(Page_AddModelsPage, self.add_models_page)
#         self.setPage(Page_ChooseEffectSize, self.choose_effect_size_page)
#         self.setPage(Page_DataLocation, self.data_location_page)
#         self.setPage(Page_RefineStudies, self.refine_studies_page)
#         self.setPage(Page_Summary, self.summary_page)
#         
#     def nextID(self):
#         if self.currentId() == Page_TreePage:
#             return -1
#         
#     def get_phylo_object(self):
#         return self.tree_page.get_phylo_object()
#     
#     



from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from meta_regression_wizard import *
from model_building.instructions import InstructionsPage

(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies,
Page_MetaRegDetails, Page_SelectCovariates, Page_ReferenceValues,
Page_Bootstrap, Page_Summary, Page_CondMeans, Page_AddModels,
Page_Instructions) = range(11)

class ModelBuildingWizard(MetaRegressionWizard):
    def __init__(self, model, parent=None):
        MetaRegressionWizard.__init__(self, model=model, parent=parent)
        
        self.analysis_label="Model Building"
        self.setWindowTitle(self.analysis_label)
        
        # Reconfigure meta regression details page a  bit
        self.meta_reg_details_page.parametric_radioButton.setChecked(True)
        self.meta_reg_details_page.analysis_type_groupBox.setEnabled(False)
        self.meta_reg_details_page.conditional_means_checkBox.setChecked(False)
        self.meta_reg_details_page.output_type_groupBox.setEnabled(False)
        
    def nextId(self):
        current_id = self.currentId()
        
        return self.nextId_helper(current_id)
        
    def nextId_helper(self, page_id):
        #analysis_type = PARAMETRIC # PARAMETRIC or BOOTSTRAP
        #output_type = NORMAL     # NORMAL or CONDITIONAL_MEANS
        
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
        
    def get_analysis_type(self): # NORMAL or BOOTSTRAP
        return NORMAL
    def get_output_type(self): # PARAMETRIC or CONDITIONAL_MEANS
        return PARAMETRIC
        
        

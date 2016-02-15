'''
Created on Mar 21, 2014

@author: george
'''

##################
#                #
# George Dietz   #
# CEBM@Brown     #
#                #
# Date: 3/7/14   #
#                #
##################

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import wizard_summary, CATEGORICAL
import python_to_R

# meta analysis pages
from common_wizard_pages.choose_effect_size_page import ChooseEffectSizePage
from common_wizard_pages.data_location_page import DataLocationPage
from common_wizard_pages.refine_studies_page import RefineStudiesPage
from common_wizard_pages.summary_page import SummaryPage
from common_wizard_pages.meta_analysis_parameters_page import MetaAnalysisParametersPage
from common_wizard_pages.reference_value_page import ReferenceValuePage
from common_wizard_pages.select_covariates_page import SelectCovariatesPage

# mice pages
from imputation.covariate_select_page import CovariateSelectPage
from imputation.mice_parameters_page import MiceParametersPage
from imputation.mice_output_page import MiceOutputPage

(Page_ChooseEffectSize, Page_DataLocation, Page_RefineStudies, Page_Summary,
 Page_Parameters, Page_SelectCovariates, Page_ReferenceValues,
 Page_MiceParameters, Page_CovariateSelect, Page_MiceOutput) = range(10)

class MiMaWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(MiMaWizard, self).__init__(parent)
        
        self.analysis_label = "Multiply-Imputed Meta Analysis/Regression"
        self.model = model
        self.imp_results = None
        
        last_analysis = model.get_last_analysis_selections() # selections from last analysis of whatever type
        
        # Initialize pages that we will need to access later
        self.parameters_page = MetaAnalysisParametersPage(method="FE" if last_analysis['fixed_effects'] else last_analysis['random_effects_method'],
                                                          level=model.get_conf_level(),
                                                          digits=model.get_precision(),
                                                          knha=last_analysis['knha'])
        self.setPage(Page_Parameters, self.parameters_page)
        
        # choose effect size
        self.choose_effect_size_page = ChooseEffectSizePage(add_generic_effect=True,
                data_type=last_analysis['data_type'],
                metric=last_analysis['metric'],
                var_groups = model.get_variable_groups())
        self.setPage(Page_ChooseEffectSize, self.choose_effect_size_page)
        
        # data location page
        self.data_location_page = DataLocationPage(model=model)
        self.setPage(Page_DataLocation, self.data_location_page)
        
        # refine studies page
        self.refine_studies_page = RefineStudiesPage(model=model)
        self.setPage(Page_RefineStudies, self.refine_studies_page)
        
        # summary page
        self.summary_page = SummaryPage()
        self.setPage(Page_Summary, self.summary_page)
         
        # Mice Parameters Page
        self.mice_params_page = MiceParametersPage()
        self.setPage(Page_MiceParameters, self.mice_params_page)
         
        # Covariate Select Page (for choosing covariates to impute with)
        self.cov_select_page = CovariateSelectPage(model = self.model)
        self.setPage(Page_CovariateSelect, self.cov_select_page)
        
        # Select Covariates page (for choosing covariates to do with regression with)
        self.select_covariates_page = SelectCovariatesPage(
                model=model,
                previously_included_covs=last_analysis['included_covariates'],
                min_covariates=0,
                allow_covs_with_missing_data=True)
        self.setPage(Page_SelectCovariates, self.select_covariates_page)
        
        
        # Reference Value Page
        self.reference_value_page = ReferenceValuePage(
                    model=model,
                    prev_cov_to_ref_level=last_analysis['cov_2_ref_values'])
        self.setPage(Page_ReferenceValues, self.reference_value_page)
         
        # Mice Output page
        self.mice_output_page = MiceOutputPage()
        self.setPage(Page_MiceOutput, self.mice_output_page)
            
        self.setWizardStyle(QWizard.ClassicStyle)
        self.setStartId(Page_ChooseEffectSize)
        self.setOption(QWizard.HaveFinishButtonOnEarlyPages,True)
        QObject.connect(self, SIGNAL("currentIdChanged(int)"), self._change_size)
        
        self.setWindowTitle("Multiply-Imputed Meta-Analysis")
        
    # Meta analysis nextID
    def nextId_helper(self, page_id):
        if page_id == Page_ChooseEffectSize:
            return Page_DataLocation
        elif page_id == Page_DataLocation:
            return Page_RefineStudies
        elif page_id == Page_RefineStudies:
            return Page_Parameters
        elif page_id == Page_Parameters: # meta analysis parameters
            return Page_MiceParameters
        elif page_id == Page_MiceParameters: # mice parameters
            return Page_CovariateSelect
        elif page_id == Page_CovariateSelect:
            return Page_MiceOutput
        elif page_id == Page_MiceOutput:
            return Page_SelectCovariates
        elif page_id == Page_SelectCovariates:
            if self._categorical_covariates_selected():
                return Page_ReferenceValues
            else:
                return Page_Summary
        elif page_id == Page_ReferenceValues:
            return Page_Summary
        elif page_id == Page_Summary:
            return -1
        
    def nextId(self):
        next_id = self.nextId_helper(self.currentId())
        return next_id
        
    def _change_size(self, pageid):
        print("changing size")
        self.adjustSize()
        
    def _require_categorical(self): # just to make select covariates page happy
        return False
    
    def _categorical_covariates_selected(self):
        '''are categorical variables selected?'''
        
        included_covariates = self.get_included_covariates()
        categorical_covariates = [cov for cov in included_covariates if cov.get_type()==CATEGORICAL]
        return len(categorical_covariates) > 0

    # My details page
    def get_analysis_parameters(self):
        return self.parameters_page.get_parameters()
    
    # refine studies page
    def get_included_studies_in_proper_order(self):
        all_studies = self.model.get_studies_in_current_order()
        included_studies = self.refine_studies_page.get_included_studies()
        included_studies_in_order = [study for study in all_studies if study in included_studies]
        return included_studies_in_order

    # data location page
    def get_data_location(self):
        return self.data_location_page.get_data_locations()
    
    # choose effect size page
    def get_data_type_and_metric(self):
        ''' returns tuple (data_type, metric) '''
        return self.choose_effect_size_page.get_data_type_and_metric()
    
    def _run_imputation(self):
        imp_results = python_to_R.impute(
            model=self.model,
            studies=self.get_included_studies_in_proper_order(),
            covariates=self.get_covariates_for_imputation(),
            m=self.get_m(),
            maxit=self.get_maxit(),
            defaultMethod_rstring=self.get_defaultMethod_rstring(),
        )
        self.imp_results = imp_results
        return imp_results
 
    def get_imputation_summary(self):
        return self.imp_results['summary']
         
#     def get_imputation_choices(self):
#         covariates = self.get_included_covariates() # covariates in original order
#          
#         imputation_choices = python_to_R.imputation_dataframes_to_pylist_of_ordered_dicts(
#                                         self.imp_results['imputations'],
#                                         covariates)
#         return imputation_choices
     
    def get_source_data(self):
        # an ordered dict mapping covariates --> values to see which ones are
        # none
        return self.imp_results['source_data']
    
    def get_imputations(self):
        return self.imp_results['imputations'] # R list of imputations
 
    ######## getters ###########
     
    ### Covariate Select Page
    def get_covariates_for_imputation(self):
        return self.cov_select_page.get_included_covariates()
     
    ### Mice Parameters Page
    def get_m(self): # number of multiple imputations
        return self.mice_params_page.get_m()
    def get_maxit(self): # number of iterations
        return self.mice_params_page.get_maxit()
    def get_defaultMethod_rstring(self):
        return self.mice_params_page.get_defaultMethod_rstring()

    ### Reference values page
    def get_covariate_reference_levels(self):
        return self.reference_value_page.get_covariate_reference_levels()
    
    # Select covariates Page
    def get_included_covariates(self): # covariates for regression (not imputation)
        return self.select_covariates_page.get_included_covariates()
    def get_included_interactions(self):
        return self.select_covariates_page.get_interactions()

    # Summary page
    def save_selections(self):
        return self.summary_page.save_selections()
    
    # Summary Page
    def get_summary(self):
        ''' Make a summary string to show the user at the end of the wizard summarizing most of the user selections '''
        return wizard_summary(wizard=self, next_id_helper=self.nextId_helper,
                              summary_page_id=Page_Summary,
                              analysis_label=self.analysis_label)
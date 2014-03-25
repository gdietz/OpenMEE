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

import python_to_R

#from ome_globals import *

(Page_MiceParameters, Page_CovariateSelect, Page_MiceOutput, Page_ImpResChoices) = range(4)

from covariate_select_page import CovariateSelectPage
from mice_parameters_page import MiceParametersPage
from mice_output_page import MiceOutputPage
from imputation_results_choice_page import ImputationResultsChoicePage

class ImputationWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(ImputationWizard, self).__init__(parent)
        
        self.model = model
        self.studies = self.model.get_studies_in_current_order()
        self.imp_results = None
        
        # Mice Parameters Page
        self.mice_params_page = MiceParametersPage()
        self.setPage(Page_MiceParameters, self.mice_params_page)
        
        # Covariate Select Page
        self.cov_select_page = CovariateSelectPage(model = self.model)
        self.setPage(Page_CovariateSelect, self.cov_select_page)
        
        # Output page
        self.mice_output_page = MiceOutputPage()
        self.setPage(Page_MiceOutput, self.mice_output_page)
        
        # Imputation results select page
        self.imputation_results_choice_page = ImputationResultsChoicePage()
        self.setPage(Page_ImpResChoices, self.imputation_results_choice_page)
        
    def get_included_studies_in_proper_order(self):
        return self.studies
        
    def nextId(self):
        current_id = self.currentId()
        
        page_order_map = {Page_MiceParameters:Page_CovariateSelect,
                          Page_CovariateSelect:Page_MiceOutput,
                          Page_MiceOutput:Page_ImpResChoices,
                          Page_ImpResChoices:-1}
        
        return page_order_map[current_id]
    
    def _run_imputation(self):
        imp_results = python_to_R.impute(model=self.model,
                                         studies=self.studies,
                                         covariates=self.get_included_covariates(),
                                         m=self.get_m(),
                                         maxit=self.get_maxit(),
                                         defaultMethod_rstring=self.get_defaultMethod_rstring())
        self.imp_results = imp_results
        return imp_results

    def get_imputation_summary(self):
        return self.imp_results['summary']
        
    def get_imputation_choices(self):
        covariates = self.get_included_covariates() # covariates in original order
        
        imputation_choices = python_to_R.imputation_dataframes_to_pylist_of_ordered_dicts(
                                        self.imp_results['imputations'],
                                        covariates)
        return imputation_choices
    
    def get_source_data(self):
        # an ordered dict mapping covariates --> values to see which ones are
        # none
        return self.imp_results['source_data']


    
    ######## getters ###########
    
    ### Covariate Select Page
    def get_included_covariates(self):
        return self.cov_select_page.get_included_covariates()
    
    ### Mice Parameters Page
    def get_m(self): # number of multiple imputations
        return self.mice_params_page.get_m()
    def get_maxit(self): # number of iterations
        return self.mice_params_page.get_maxit()
    def get_defaultMethod_rstring(self):
        return self.mice_params_page.get_defaultMethod_rstring()
    
    # Imputation Results Choice Page
    def get_imputed_values(self):
        return self.imputation_results_choice_page.get_imputed_values()
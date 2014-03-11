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

(Page_MiceParameters, Page_CovariateSelect, Page_MiceOutput) = range(3)

from covariate_select_page import CovariateSelectPage
from mice_parameters_page import MiceParametersPage
from mice_output_page import MiceOutputPage

class ImputationWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(ImputationWizard, self).__init__(parent)
        
        self.model = model
        self.studies = self.model.get_studies_in_current_order()
        
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
        
        
        
    def nextId(self):
        current_id = self.currentId()
        
        page_order_map = {Page_MiceParameters:Page_CovariateSelect,
                          Page_CovariateSelect:Page_MiceOutput,
                          Page_MiceOutput:-1}
        
        return page_order_map[current_id]
    
    def _run_imputation(self):
        imp_results = python_to_R.impute(model=self.model,
                                         studies=self.studies,
                                         covariates=self.get_included_covariates(),
                                         m=self.get_m(),
                                         maxit=self.get_maxit(),
                                         defaultMethod_rstring=self.get_defaultMethod_rstring())
        return imp_results
    
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
    
    # Mice Output page (holds the imputation choices)
    def get_imputation_choices(self):
        choices_list =  self.mice_output_page.get_imputation_choices()
         
        
        return choices_list
        
        
    
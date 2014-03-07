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

#from ome_globals import *

(Page_MiceParameters, Page_CovariateSelect) = range(2)

from covariate_select_page import CovariateSelectPage
from mice_parameters_page import MiceParametersPage

class ImputationWizard(QtGui.QWizard):
    def __init__(self, model, parent=None):
        super(ImputationWizard, self).__init__(parent)
        
        self.model = model
        
        # Mice Parameters Page
        self.mice_params_page = MiceParametersPage()
        self.setPage(Page_MiceParameters, self.mice_params_page)
        
        # Covariate Select Page
        self.cov_select_page = CovariateSelectPage(model = self.model)
        self.setPage(Page_CovariateSelect, self.cov_select_page)
        
    def nextId(self):
        current_id = self.currentId()
        
        page_order_map = {Page_MiceParameters:Page_CovariateSelect,
                          Page_CovariateSelect:-1}
        
        return page_order_map[current_id]
    
    ######## getters ###########
    
    ### Covariate Select Page
    def get_included_covariates(self):
        return self.cov_select_page.get_included_covariates()
    
    ### Mice Parameters Page
    def get_m(self): # number of multiple imputations
        self.mice_params_page.get_m()
    def get_maxit(self): # number of iterations
        self.mice_params_page.get_maxit()
    def get_defaultMethod_rstring(self):
        self.mice_params_page.get_defaultMethod_rstring()
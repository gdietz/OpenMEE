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

import ui_mice_parameters_page

# imputation methods for missing values of any time
ANY_IMP_METHODS = ['pmm','2lonly.pmm','rf','cart','sample','fastpmm']

# numeric
NUMERIC_IMP_METHODS = any + ['norm', 'norm.nob','norm.boot','norm.predict',
                             'mean','2l.norm','2l.pan','2lonly.mean',
                             '2lonly.norm','quadratic','ri']
# factor with 2 levels
FACTOR_2LEVEL_IMP_METHODS = any + ['logreg Logistic','logreg.boot']

# factor w/ more than 2 levels
FACTOR_MANY_IMP_METHODS = any + ['polyreg', 'lda']

# These descriptions were taken from the mice documentation at:
# http://cran.r-project.org/web/packages/mice/mice.pdf
IMP_METHOD_TO_PRETY_NAME = {
'pmm'       : 'Predictive mean matching',                              # (any)
'2lonly.pmm': 'Imputation at level-2 by Predictive mean matching',     # (any)
'rf'        : 'Random forest imputations',                             # (any)
'cart'      : 'ClassiÞcation and regression trees',                    # (any)
'sample'    : 'Random sample from the observed values',                # (any)
'fastpmm'   : 'Experimental: Fast predictive mean matching using C++', # (any)
##############################################################################
'norm'        : 'Bayesian linear regression',                          # (numeric),
'norm.nob'    : 'Linear regression ignoring model error',              # (numeric),
'norm.boot'   : 'Linear regression using bootstrap',                   # (numeric),
'norm.predict': 'Linear regression, predicted values',                 # (numeric),
'mean'        : 'Unconditional mean imputation',                       # (numeric),
'2l.norm'     : 'Two-level normal imputation',                         # (numeric),
'2l.pan'      : 'Two-level normal imputation using pan',               # (numeric),
'2lonly.mean' : 'Imputation at level-2 of the class mean',             # (numeric),
'2lonly.norm' : 'Imputation at level-2 by Bayesian linear regression', # (numeric),
'quadratic'   : 'Imputation of quadratic terms',                       # (numeric),
'ri'          : 'Random indicator method for nonignorable data',       # (numeric),
##############################################################################
'logreg'      : 'Logistic regression',                # (factor, 2 levels)
'logreg.boot' : 'Logistic regression with bootstrap', # (factor, 2 levels)
##############################################################################
'polyreg': 'Polytomous logistic regression',  # (factor, >= 2 levels)
'lda'    : 'Linear discriminant analysis',    # (factor, >= 2 categories)
##############################################################################
'polr' : 'Proportional odds model', # (ordered, >=2 levels)
}




class MiceParametersPage(QWizardPage, ui_mice_parameters_page.Ui_WizardPage):
    def __init__(self, parent=None): # todo: set defaults of previous parameters to None
        super(MiceParametersPage, self).__init__(parent)
        self.setupUi(self)
        
        # Populate methods combo boxes
        # defaults from mice: defaultMethod = c("pmm","logreg", "polyreg", "polr")
        self._populate_methods_combobox(self.numeric_comboBox, methods=NUMERIC_IMP_METHODS, default_method="pmm")
        self._populate_methods_combobox(self.factor_2_levels_comboBox, methods=FACTOR_2LEVEL_IMP_METHODS, default_method="logreg")
        self._populate_methods_combobox(self.factor_gt_2_levels_comboBox, methods=FACTOR_MANY_IMP_METHODS, default_method="polyreg")
        
    
    def _populate_methods_combobox(self, box, methods, default_method):
        
        for x in methods:
            name = x
            pretty_name = IMP_METHOD_TO_PRETY_NAME[x]
            self.box.addItem(pretty_name, userData=QVariant(name))
        default_idx = self.box.findData(QVariant(default_method))
        if default_idx == -1:
            raise("Default method '%s' not found" % default_method)
        self.box.setCurrentIndex(default_idx)
    
    ################################# Getters #################################
    def get_m(self): # number of multiple imputations
        return self.m_spinBox.value()
    def get_maxit(self): # number of iterations
        return self.maxit_spinBox.value()
    
    def get_defaultMethod_rstring(self):
        # from mice doc: defaultMethod = c("pmm","logreg", "polyreg", "polr")
        # 1st is numeric, 2nd is factor 2 level, 3rd is factor >2 levels, 3rd is ordered factor >2 levels
        
        numeric_data = self.numeric_comboBox.itemData(self.numeric_comboBox.currentIndex())
        factor2_data = self.factor_2_levels_comboBox.itemData(self.factor_2_levels_comboBox.currentIndex())
        factor_gt2_data = self.factor_gt_2_levels_comboBox.itemData(self.factor_gt_2_levels_comboBox.currentIndex())
         
        numeric_method    = str(numeric_data.toString())
        factor2_method    = str(factor2_data.toString())
        factor_gt2_method = str(factor_gt2_data.toString())
        
        # We don't deal with ordered factors with >2 levels (4th argument)
        return 'c("%s","%s","%s","polr")' % (numeric_method, factor2_method, factor_gt2_method)
        
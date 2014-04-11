import random
import unittest
import os
import os.path
import pickle

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ee_model
import python_to_R
from main_form import default_user_prefs
from ome_globals import CONTINUOUS


working_directory = os.getcwd()
test_sample_data_dir = os.path.join(working_directory, 'test_sample_data')

# Load user prefs
user_prefs = default_user_prefs()


###############################################################################
def load_R_libraries():
    ''' Loads the R libraries while updating the splash screen'''
    
    rloader = python_to_R.RlibLoader()

    rloader.load_metafor()
    rloader.load_openmetar()
    rloader.load_igraph()
    rloader.load_grid()
    rloader.load_ape()
    rloader.load_mice()
load_R_libraries()
###############################################################################

def load_testfile_model_and_setup_things_on_R_side(file_name):
    ''' Load up a model for testing, clear out objects from R and reset conf level
        Returns the model '''
    
    # load pickled testing ome file
    file_path = os.path.join(test_sample_data_dir,file_name)
    print("Loaded %s" % file_path)
    with open(file_path, 'r') as f:
        model_state = pickle.load(f)
        
    # load model
    undo_stack = QUndoStack()
    model = ee_model.EETableModel(undo_stack=undo_stack,
                                       user_prefs=user_prefs,
                                       model_state=model_state)
    # reset workspace
    python_to_R.exR.execute_in_R("rm(list=ls())")
    python_to_R.set_conf_level_in_R(model.get_conf_level())
    
    return model

def get_covs_from_names(cov_names, model):
    ''' returns a list of covariate objects from the model that have the given names '''
    covs = [cov for cov in model.get_variables() if cov.get_label() in cov_names]
    return covs

def get_cov_ref_values_from_names_to_refvals(names_to_ref_vals, model):
    ''' Returns dict mapping covariates to ref. values '''
    
    cov_ref_values = {}
    covs = model.get_variables()
    for label,ref_val in names_to_ref_vals.items():
        cov = get_variable_by_label(label, model=model)
        cov_ref_values[cov]=ref_val
    return cov_ref_values

def get_variable_by_label(label, model):
    ''' returns AN instance of of a variable in the model having the given label
    raises Exception otherwise '''
    # Helper for get_cov_ref_values_from_names_to_refvals
    
    variables = model.get_variables()
    for var in variables:
        if var.get_label()==label:
            return var
    raise Exception("No variable with label '%s' found in the model" % label)
    
            
class TestStandardMetaAnalysis(unittest.TestCase):
    def setUp(self):
        filename = "test_dataset_w_OR_and_d.ome"
        self.model = load_testfile_model_and_setup_things_on_R_side(filename)
    
    def test_binaryMetaAnalysis(self):
        #result = None
        
        studies = self.model.get_studies_in_current_order()
        data_location = {'control_noresponse': None, 'effect_size': 16, 'experimental_response': None, 'experimental_noresponse': None, 'variance': 17, 'control_response': None}
        python_to_R.dataset_to_simple_binary_robj(model=self.model,
                                                  included_studies=studies,
                                                  data_location=data_location,
                                                  covs_to_include=[])
        method = "binary.random"
        params = {'conf.level': 95.0, 'digits': 3, 'fp_col2_str': u'[default]', 'fp_show_col4': True, 'to': 'only0', 'fp_col4_str': u'Ev/Ctrl', 'fp_xticks': '[default]', 'fp_col3_str': u'Ev/Trt', 'fp_show_col3': True, 'fp_show_col2': True, 'fp_show_col1': True, 'fp_plot_lb': '[default]', 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'adjust': 0.5, 'fp_plot_ub': '[default]', 'fp_col1_str': u'Studies', 'measure': 'OR', 'fp_xlabel': u'[default]', 'fp_show_summary_line': True}
        result = python_to_R.run_binary_ma(function_name=method,
                                           params=params)

        self.assertIsNotNone(result, "Result is unexpectedly none!")
        
    def test_continuousMetaAnalysis(self):
        # assert result is not None
        
        studies = self.model.get_studies_in_current_order()
        data_location = {'experimental_mean': 2, 'effect_size': 18, 'experimental_std_dev': 5, 'experimental_sample_size': 1, 'control_std_dev': 5, 'control_sample_size': 1, 'variance': 19, 'control_mean': 4}
        data_type = CONTINUOUS
        python_to_R.dataset_to_simple_continuous_robj(model=self.model,
                                                      included_studies=studies,
                                                      data_location=data_location,
                                                      data_type=data_type, 
                                                      covs_to_include=[])
        method = "continuous.random"
        params = {'conf.level': 95.0, 'digits': 3, 'fp_col2_str': u'[default]', 'fp_show_col4': False, 'fp_xlabel': u'[default]', 'fp_col4_str': u'Ev/Ctrl', 'fp_xticks': '[default]', 'fp_col3_str': u'Ev/Trt', 'fp_show_col3': False, 'fp_show_col2': True, 'fp_show_col1': True, 'fp_plot_lb': '[default]', 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'fp_plot_ub': '[default]', 'fp_col1_str': u'Studies', 'measure': 'SMD', 'fp_show_summary_line': True}
        result = python_to_R.run_continuous_ma(function_name=method,
                                               params=params)
        self.assertIsNotNone(result, "Result is unexpectedly none!")

class TestMetaMethods(unittest.TestCase):
    def setUp(self):
        # load pickled testing ome file
        filename = "test_dataset_w_OR_and_d.ome"
        self.model = load_testfile_model_and_setup_things_on_R_side(filename)
         
    def test_cumulative(self):
        ''' cumulative meta analysis '''
        studies = self.model.get_studies_in_current_order()
        method = "continuous.random"
        current_param_vals = {'conf.level': 95.0, 'digits': 3, 'fp_col2_str': u'[default]', 'fp_show_col4': False, 'fp_xlabel': u'[default]', 'fp_col4_str': u'Ev/Ctrl', 'fp_xticks': '[default]', 'fp_col3_str': u'Ev/Trt', 'fp_show_col3': False, 'fp_show_col2': True, 'fp_show_col1': True, 'fp_plot_lb': '[default]', 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'fp_plot_ub': '[default]', 'fp_col1_str': u'Studies', 'measure': 'SMD', 'fp_show_summary_line': True}
        data_location = {'experimental_mean': 2, 'effect_size': 18, 'experimental_std_dev': 5, 'experimental_sample_size': 1, 'control_std_dev': 5, 'control_sample_size': 1, 'variance': 19, 'control_mean': 4}
        meta_f_str = "cum.ma.continuous"
        
        python_to_R.dataset_to_simple_continuous_robj(model=self.model,
                                                      included_studies=studies,
                                                      data_location=data_location,
                                                      data_type=CONTINUOUS, 
                                                      covs_to_include=[])
        result = python_to_R.run_meta_method(meta_function_name = meta_f_str,
                                             function_name = method,
                                             params = current_param_vals)
        # assert result is not None
        self.assertIsNotNone(result, "Result is unexpectedly none!")
        
        
        
     
    def test_loo(self): # leave one out
        ''' leave_one_out meta analysis '''
        studies = self.model.get_studies_in_current_order()
        method = "continuous.random"
        current_param_vals = {'conf.level': 95.0, 'digits': 3, 'fp_col2_str': u'[default]', 'fp_show_col4': False, 'fp_xlabel': u'[default]', 'fp_col4_str': u'Ev/Ctrl', 'fp_xticks': '[default]', 'fp_col3_str': u'Ev/Trt', 'fp_show_col3': False, 'fp_show_col2': True, 'fp_show_col1': True, 'fp_plot_lb': '[default]', 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'fp_plot_ub': '[default]', 'fp_col1_str': u'Studies', 'measure': 'SMD', 'fp_show_summary_line': True}
        data_location = {'experimental_mean': 2, 'effect_size': 18, 'experimental_std_dev': 5, 'experimental_sample_size': 1, 'control_std_dev': 5, 'control_sample_size': 1, 'variance': 19, 'control_mean': 4}
        meta_f_str = "loo.ma.continuous"
        
        python_to_R.dataset_to_simple_continuous_robj(model=self.model,
                                                      included_studies=studies,
                                                      data_location=data_location,
                                                      data_type=CONTINUOUS, 
                                                      covs_to_include=[])
        result = python_to_R.run_meta_method(meta_function_name = meta_f_str,
                                             function_name = method,
                                             params = current_param_vals)
        # assert result is not None
        self.assertIsNotNone(result, "Result is unexpectedly none!")
     
    def test_subgroup(self):
        ''' subgroup meta analysis '''
        studies = self.model.get_studies_in_current_order()
        method = "continuous.random"
        current_param_vals = {'conf.level': 95.0, 'digits': 3, 'fp_col2_str': u'[default]', 'fp_show_col4': False, 'fp_xlabel': u'[default]', 'fp_col4_str': u'Ev/Ctrl', 'fp_xticks': '[default]', 'fp_col3_str': u'Ev/Trt', 'fp_show_col3': False, 'fp_show_col2': True, 'fp_show_col1': True, 'fp_plot_lb': '[default]', 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'fp_plot_ub': '[default]', 'fp_col1_str': u'Studies', 'cov_name': 'Gender', 'measure': 'SMD', 'fp_show_summary_line': True}
        data_location = {'experimental_mean': 2, 'effect_size': 18, 'experimental_std_dev': 5, 'experimental_sample_size': 1, 'control_std_dev': 5, 'control_sample_size': 1, 'variance': 19, 'control_mean': 4}
        meta_f_str = "subgroup.ma.continuous"
        cov_names_to_include = ["Gender",]
        covs_to_include = get_covs_from_names(cov_names_to_include, model=self.model)
        
        python_to_R.dataset_to_simple_continuous_robj(model=self.model,
                                                      included_studies=studies,
                                                      data_location=data_location,
                                                      data_type=CONTINUOUS, 
                                                      covs_to_include=covs_to_include)
        result = python_to_R.run_meta_method(meta_function_name = meta_f_str,
                                             function_name = method,
                                             params = current_param_vals)
        # assert result is not None
        self.assertIsNotNone(result, "Result is unexpectedly none!")
         
    def test_bootstrapped_ma(self):
        ''' bootstrapped meta analysis '''
        studies = self.model.get_studies_in_current_order()
        method = "continuous.random"
        current_param_vals = {'conf.level': 95.0, 'histogram.xlab': 'Effect Size', 'fp_xticks': '[default]', 'fp_show_col4': False, 'fp_show_col3': False, 'fp_xlabel': u'[default]', 'fp_show_col1': True, 'fp_show_col2': True, 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'fp_plot_ub': '[default]', 'fp_col1_str': u'Studies', 'measure': 'SMD', 'fp_plot_lb': '[default]', 'bootstrap.plot.path': '/Users/george/git/OpenMEE/r_tmp/bootstrap.png', 'digits': 3, 'fp_col2_str': u'[default]', 'num.bootstrap.replicates': 1000, 'fp_col4_str': u'Ev/Ctrl', 'histogram.title': 'Bootstrap Histogram', 'fp_col3_str': u'Ev/Trt', 'fp_show_summary_line': True, 'bootstrap.type': 'boot.ma'}
        data_location = {'experimental_mean': 2, 'effect_size': 18, 'experimental_std_dev': 5, 'experimental_sample_size': 1, 'control_std_dev': 5, 'control_sample_size': 1, 'variance': 19, 'control_mean': 4}
        meta_f_str = "bootstrap.continuous"
        
        python_to_R.dataset_to_simple_continuous_robj(model=self.model,
                                                      included_studies=studies,
                                                      data_location=data_location,
                                                      data_type=CONTINUOUS, 
                                                      covs_to_include=[])
        result = python_to_R.run_meta_method(meta_function_name = meta_f_str,
                                             function_name = method,
                                             params = current_param_vals)
        # assert result is not None
        self.assertIsNotNone(result, "Result is unexpectedly none!")
 
class TestMetaRegressionMethods(unittest.TestCase):
    def setUp(self):
        # load pickled testing ome file
        filename = "test_dataset_w_OR_and_d.ome"
        self.model = load_testfile_model_and_setup_things_on_R_side(filename)
        
        # shared parameters
        self.studies = self.model.get_studies_in_current_order()
        self.data_location = {'experimental_mean': 2, 'effect_size': 18, 'experimental_std_dev': 5, 'experimental_sample_size': 1, 'control_std_dev': 5, 'control_sample_size': 1, 'variance': 19, 'control_mean': 4}
        
        cov_names = ['Age', 'Gender']
        self.covariates = get_covs_from_names(cov_names, model=self.model)
        
        cov_names_to_ref_vals = {"Gender":'M'}
        self.cov_ref_values = get_cov_ref_values_from_names_to_refvals(cov_names_to_ref_vals, model=self.model)
        self.interactions = []
        self.fixed_effects = False
        self.random_effects_method = "REML"
        self.digits = 3
        self.conf_level = 95.0
        self.btt = (None, None) # this will vary in the omnibus test
         
    def test_metaReg(self): # regular meta regression
        
        python_to_R.dataset_to_dataframe(model=self.model,
                                         included_studies=self.studies,
                                         data_location=self.data_location,
                                         covariates=self.covariates,
                                         cov_ref_values=self.cov_ref_values,
                                         var_name="tmp_obj")
                
        result = python_to_R.run_gmeta_regression(
                                  covariates=self.covariates,
                                  interactions=self.interactions,
                                  fixed_effects=self.fixed_effects,
                                  random_effects_method=self.random_effects_method,
                                  digits=self.digits,
                                  conf_level=self.conf_level,
                                  btt=self.btt,
                                  data_name="tmp_obj")

        # assert result is not None
        self.assertIsNotNone(result, "Result is unexpectedly none!")
         
    def test_metaReg_omnibus(self):
        btt_wName = ("Age" , 'covariate')
        btt = (get_variable_by_label(btt_wName[0], model=self.model), 'covariate')
        
        python_to_R.dataset_to_dataframe(model=self.model,
                                 included_studies=self.studies,
                                 data_location=self.data_location,
                                 covariates=self.covariates,
                                 cov_ref_values=self.cov_ref_values,
                                 var_name="tmp_obj")
                
        result = python_to_R.run_gmeta_regression(
                                  covariates=self.covariates,
                                  interactions=self.interactions,
                                  fixed_effects=self.fixed_effects,
                                  random_effects_method=self.random_effects_method,
                                  digits=self.digits,
                                  conf_level=self.conf_level,
                                  btt=btt,
                                  data_name="tmp_obj")
        

        # assert result is not None
        self.assertIsNotNone(result, "Result is unexpectedly none!")
#          
#     def test_metaReg_bootstrapped(self):
#         # assert result is not None
#          
#     def test_metaReg_cond_means(self):
#         # assert result is not None
#          
#     def test_metaReg_bootstrapped_cond_means(self):
#         # assert result is not None
 
# class TestPhylogeneticMetaAnalysis(unittest.TestCase):
#     def setUp(self):
#         # load pickled testing ome for phylogenetics file
#         # load phylogeny tree
#     
#     def test_phylo(self):
#         # assert result is not None
#         
# class TestMultipleImputationMetaAnalysis(unittest.TestCase):
#     def setUp(self):
#         # load pickled testing ome with missing data
#         
#     def test_MIMA(self): # just do a continuous mi meta analysis
#         # assert result is not None
#         
# class TestModelBuilding(unittest.TestCase):
#     def setUp(self):
#         # load pickled testing ome
#         
#     def test_modelbuild_ma(self):
#         # assert result is not None

if __name__ == '__main__':
    standard_ma_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestStandardMetaAnalysis)
    meta_method_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMetaMethods)
    meta_reg_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMetaRegressionMethods)
#     phylo_ma_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestPhylogeneticMetaAnalysis)
#     mima_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMultipleImputationMetaAnalysis)
#     model_building_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestModelBuilding)
    alltests = unittest.TestSuite([standard_ma_test_suite,
                                    meta_method_test_suite,
                                    meta_reg_test_suite,
#                                    phylo_ma_test_suite,
#                                    mima_test_suite,
#                                    model_building_test_suite
                                   ])
    unittest.TextTestRunner(verbosity=2, buffer=True).run(alltests)
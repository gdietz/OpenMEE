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

            
class TestStandardMetaAnalysis(unittest.TestCase):
    def setUp(self):
        # load pickled testing ome file
        file_path = os.path.join(test_sample_data_dir,'test_dataset_w_OR_and_d.ome')
        print("Loaded %s" % file_path)
        with open(file_path, 'r') as f:
            model_state = pickle.load(f)
            
        # load model
        undo_stack = QUndoStack()
        self.model = ee_model.EETableModel(undo_stack=undo_stack,
                                           user_prefs=user_prefs,
                                           model_state=model_state)
        # reset workspace
        python_to_R.exR.execute_in_R("rm(list=ls())")
        python_to_R.set_conf_level_in_R(self.model.get_conf_level())
    
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

# class TestMetaMethods(unittest.TestCase):
#     def setUp(self):
#         # load pickled testing ome file
#         
#     def test_cumulative(self):
#         # assert result is not None
#     
#     def test_loo(self): # leave one out
#         # assert result is not None
#     
#     def test_subgroup(self):
#         # assert result is not None
#         
#     def test_bootstrapped_ma(self):
#         # assert result is not None
# 
# class TestMetaRegressionMethods(unittest.TestCase):
#     def setUp(self):
#         # load pickled testing ome file
#         
#     def test_metaReg(self): # regular meta regression
#         # assert result is not None
#         
#     def test_metaReg_omnibus(self):
#         # assert result is not None
#         
#     def test_metaReg_bootstrapped(self):
#         # assert result is not None
#         
#     def test_metaReg_cond_means(self):
#         # assert result is not None
#         
#     def test_metaReg_bootstrapped_cond_means(self):
#         # assert result is not None
# 
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
#     meta_method_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMetaMethods)
#     meta_reg_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMetaRegressionMethods)
#     phylo_ma_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestPhylogeneticMetaAnalysis)
#     mima_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMultipleImputationMetaAnalysis)
#     model_building_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestModelBuilding)
    alltests = unittest.TestSuite([standard_ma_test_suite,
#                                    meta_method_test_suite,
#                                    meta_reg_test_suite,
#                                    phylo_ma_test_suite,
#                                    mima_test_suite,
#                                    model_building_test_suite
                                   ])
    unittest.TextTestRunner(verbosity=2).run(alltests)
import python_to_R


import unittest

class TestRunMABasedMethods(unittest.TestCase):

    def test_meta_analysis(self):
        '''
        meta_analysis() just spawns a wizard and calls run_ma
        maybe write a real test later
        '''
        pass
    def test_run_ma(self):
        pass
    def test_cum_ma(self):
        pass
    def test_loo_ma(self):
        pass
    def test_subroup_ma(self):
        pass
    def test_bootstrap_ma(self):
        pass


class TestGmetaRegressionMethods(unittest.TestCase):
    def test_gmeta_regression(self):
        pass
    def test_run_gmeta_regression(self):
        pass
    def test_run_gmeta_regression_cond_means(self):
        pass
    def test_run_gmeta_regression_bootstrapped(self):
        pass
    def test_run_gmeta_regression_bootstrapped_cond_means(self):
        pass

class TestFailSafeMethods(unittest.TestCase):
    def test_failsafe_analysis(self):
        pass

class TestFunnelPlotMethods(unittest.TestCase):
    def test_funnel_plot_analysis(self):
        pass

class TestHistogramMethods(unittest.TestCase):
    def test_histogram(self):
        pass

class TestModelBuildingMethods(unittest.TestCase):
    def test_model_building(self):
        pass
    def test_run_model_building(self):
        pass

class TestPhyloMethods(unittest.TestCase):
    def test_phylo_ma(self):
        pass
    def test_run_phylo_ma(self):
        pass

class TestPermutationAnalysis(unittest.TestCase):
    def test_PermutationAnalysis(self):
        pass
    def test_run_permutation_analysis(self):
        pass

class TestScatterPlotMethods(unittest.TestCase):
    def test_scatterplot(self):
        pass

class TestMultipleImputationMetaAnalysisMethods(unittest.TestCase):
    def test_mi_meta_analysis(self):
        pass
    def test_run_mi_ma(self):
        pass

class TestDynamicDataExplorationAnalysis(unittest.TestCase):
    def test_dynamic_data_exploration_analysis(self):
        pass

class TestAnalysisUtilities(unittest.TestCase):
    def test__display_results(self):
        pass

if __name__ == '__main__': 
    unittest.main()
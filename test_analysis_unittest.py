import random
import unittest

# class TestSequenceFunctions(unittest.TestCase):
# 
#     def setUp(self):
#         self.seq = range(10)
# 
#     def test_shuffle(self):
#         # make sure the shuffled sequence does not lose any elements
#         random.shuffle(self.seq)
#         self.seq.sort()
#         self.assertEqual(self.seq, range(10))
# 
#         # should raise an exception for an immutable sequence
#         self.assertRaises(TypeError, random.shuffle, (1,2,3))
# 
#     def test_choice(self):
#         element = random.choice(self.seq)
#         self.assertTrue(element in self.seq)
# 
#     def test_sample(self):
#         with self.assertRaises(ValueError):
#             random.sample(self.seq, 20)
#         for element in random.sample(self.seq, 5):
#             self.assertTrue(element in self.seq)
            
class TestStandardMetaAnalysis(unittest.TestCase):
    def setUp(self):
        # load pickled testing ome file
    
    def test_binaryMetaAnalysis(self):
        
        # assert result is not None
        
    def test_continuousMetaAnalysis(self):
        # assert result is not None


class TestMetaMethods(unittest.TestCase):
    def setUp(self):
        # load pickled testing ome file
        
    def test_cumulative(self):
        # assert result is not None
    
    def test_loo(self): # leave one out
        # assert result is not None
    
    def test_subgroup(self):
        # assert result is not None
        
    def test_bootstrapped_ma(self):
        # assert result is not None

class TestMetaRegressionMethods(unittest.TestCase):
    def setUp(self):
        # load pickled testing ome file
        
    def test_metaReg(self): # regular meta regression
        # assert result is not None
        
    def test_metaReg_omnibus(self):
        # assert result is not None
        
    def test_metaReg_bootstrapped(self):
        # assert result is not None
        
    def test_metaReg_cond_means(self):
        # assert result is not None
        
    def test_metaReg_bootstrapped_cond_means(self):
        # assert result is not None

class TestPhylogeneticMetaAnalysis(unittest.TestCase):
    def setUp(self):
        # load pickled testing ome for phylogenetics file
        # load phylogeny tree
    
    def test_phylo(self):
        # assert result is not None
        
class TestMultipleImputationMetaAnalysis(unittest.TestCase):
    def setUp(self):
        # load pickled testing ome with missing data
        
    def test_MIMA(self): # just do a continuous mi meta analysis
        # assert result is not None
        
class TestModelBuilding(unittest.TestCase):
    def setUp(self):
        # load pickled testing ome
        
    def test_modelbuild_ma(self):
        # assert result is not None

if __name__ == '__main__':
    standard_ma_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestStandardMetaAnalysis)
    meta_method_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMetaMethods)
    meta_reg_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMetaRegressionMethods)
    phylo_ma_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestPhylogeneticMetaAnalysis)
    mima_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestMultipleImputationMetaAnalysis)
    model_building_test_suite = unittest.TestLoader().loadTestsFromTestCase(TestModelBuilding)
    alltests = unittest.TestSuite([standard_ma_test_suite,
                                   meta_method_test_suite,
                                   meta_reg_test_suite,
                                   phylo_ma_test_suite,
                                   mima_test_suite,
                                   model_building_test_suite])
    unittest.TextTestRunner(verbosity=2).run(alltests)
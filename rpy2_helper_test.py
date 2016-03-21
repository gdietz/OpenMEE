'''
Created on Jul 27, 2015

@author: george
'''
import unittest
from rpy2_helper import (
    rvector_to_pystruct,
    parse_r_struct,
    singletonlists_to_scalars,
)

from rpy2 import robjects as ro


# class Test(unittest.TestCase):


#     def setUp(self):
#         pass


#     def tearDown(self):
#         pass


#     def testName(self):
#         pass


class RVectorToPyStruct(unittest.TestCase):
    def test_numeric_vector(self):
        test_vector = ro.r("c(10, 9, 8, 7, 6, 5)")
        expected_result = [10, 9, 8, 7, 6, 5]
        result = rvector_to_pystruct(test_vector)
        self.assertEqual(result, expected_result)

    def test_string_vector(self):
        test_vector = ro.r("c('one', 'two', 'three')")
        expected_result = ['one', 'two', 'three']
        result = rvector_to_pystruct(test_vector)
        self.assertEqual(result, expected_result)

    def test_boolean_vector(self):
        test_vector = ro.r("c(TRUE, FALSE, TRUE)")
        expected_result = [True, False, True]
        result = rvector_to_pystruct(test_vector)
        self.assertEqual(result, expected_result)

    def test_named_vector(self):
        test_vector = ro.r("c(red=1, green=2, blue=3)")
        expected_result = {
            'red': 1,
            'green': 2,
            'blue': 3
        }
        result = rvector_to_pystruct(test_vector)
        self.assertEqual(result, expected_result)


class NamedRlistToPyDict(unittest.TestCase):
    def test_single_level_list(self):
        test_list = ro.r("list(a=1, b=2, c=3)")
        expected_result = {
            'a': [1],
            'b': [2],
            'c': [3],
        }
        result = parse_r_struct(test_list)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    # unittest.main()
    test_list = ro.r(
        '''
            list(
                WEIGHTED.HISTOGRAM=list(
                    # for the menu option in OpenMEE
                    ACTIONTEXT = 'Weighted Histogram',
                    MAIN = 'weighted.histogram',
                    WIZARD.WINDOW.TITLE = 'Weighted Histogram',
                    WIZARD.PAGES = list(
                        DATALOCATION = list(SHOW.RAW.DATA=FALSE),
                        REFINESTUDIES = list(),
                        SUMMARY = list()
                    )
                )
            )
        '''
    )
    parsed_rstruct = parse_r_struct(test_list)
    print "Result: %s" % str(parsed_rstruct)
    converted_result = singletonlists_to_scalars(parsed_rstruct)
    print "After singleton conversion: %s" % str(converted_result)

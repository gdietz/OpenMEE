# Test cases for binary_calculator

import unittest
import sys

import binary_calculator
from ome_globals import *

'''
Due to peculiarities of testing with a PyQt application instance,
(QApplication) this test module may only work properly when called via
python binary_calculator_test.py as a one-off instead of part of a test
discovery
'''

class TestCompute2x2Table(unittest.TestCase):

    def test_empty(self):
        '''
        Initial table:
            +---+---+---+
            |   |   |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
            |   |   |   |
            +---+---+---+
        '''

        init_table = {
            '0,0': None, '0,1': None, '0,2': None,
            '1,0': None, '1,1': None, '1,2': None,
            '2,0': None, '2,1': None, '2,2': None,
        }

        expected_table = init_table.copy()
        result_table = binary_calculator.compute_2x2_table(init_table)
        self.assertEqual(result_table, expected_table)

    def test_firstrow(self):
        '''
        Initial table:       Expected Result:
            +---+---+---+        +---+---+---+
            | 1 | 2 |   |        | 1 | 2 | 3 |
            +---+---+---+        +---+---+---+
            |   |   |   |        |   |   |   |
            +---+---+---+        +---+---+---+
            |   |   |   |        |   |   |   |
            +---+---+---+        +---+---+---+
        '''

        init_table = {
            '0,0': 1,    '0,1': 2,    '0,2': None,
            '1,0': None, '1,1': None, '1,2': None,
            '2,0': None, '2,1': None, '2,2': None,
        }

        expected_table = {
            '0,0': 1,    '0,1': 2,    '0,2': 3,
            '1,0': None, '1,1': None, '1,2': None,
            '2,0': None, '2,1': None, '2,2': None,
        }

        result_table = binary_calculator.compute_2x2_table(init_table)
        self.assertEqual(result_table, expected_table)


    def test_firstrow_middle_column(self):
        '''
        Initial table:       Expected Result:
            +---+---+---+        +---+---+---+
            | 1 | 2 |   |        | 1 | 2 | 3 |
            +---+---+---+        +---+---+---+
            |   | 4 |   |        |   | 4 |   |
            +---+---+---+        +---+---+---+
            |   |   |   |        |   | 6 |   |
            +---+---+---+        +---+---+---+
        '''

        init_table = {
            '0,0': 1,    '0,1': 2,    '0,2': None,
            '1,0': None, '1,1': 4,    '1,2': None,
            '2,0': None, '2,1': None, '2,2': None,
        }

        expected_table = {
            '0,0': 1,    '0,1': 2,    '0,2': 3,
            '1,0': None, '1,1': 4,    '1,2': None,
            '2,0': None, '2,1': 6   , '2,2': None,
        }

        result_table = binary_calculator.compute_2x2_table(init_table)
        self.assertEqual(result_table, expected_table)

    def test_cornersonly(self):
        '''
        Initial table:       Expected Result:
            +---+---+---+        +---+---+---+
            | 1 |   | 5 |        | 1 | 4 | 5 |
            +---+---+---+        +---+---+---+
            |   |   |   |        | 1 | 3 | 4 |
            +---+---+---+        +---+---+---+
            | 2 |   | 9 |        | 2 | 7 | 9 |
            +---+---+---+        +---+---+---+
        '''

        init_table = {
            '0,0': 1,    '0,1': None, '0,2': 5,
            '1,0': None, '1,1': None, '1,2': None,
            '2,0': 2,    '2,1': None, '2,2': 9,
        }

        expected_table = {
            '0,0': 1,    '0,1': 4, '0,2': 5,
            '1,0': 1,    '1,1': 3, '1,2': 4,
            '2,0': 2,    '2,1': 7, '2,2': 9,
        }

        result_table = binary_calculator.compute_2x2_table(init_table)
        self.assertEqual(result_table, expected_table)

    def test_negative_count(self):
        '''
        Initial table:       Expected Result:
            +----+---+----+        +----+----+----+
            |    |   |    |        |    |    |    |
            +----+---+----+        +----+----+----+
            |    |   |    |        |    |    |    |
            +----+---+----+        +----+----+----+
            | 20 |   | 15 |        | 20 | -5 | 15 |
            +----+---+----+        +----+----+----+
        '''

        init_table = {
            '0,0': None, '0,1': None, '0,2': None,
            '1,0': None, '1,1': None, '1,2': None,
            '2,0': 20,   '2,1': None, '2,2': 15,
        }

        expected_table = {
            '0,0': None, '0,1': None, '0,2': None,
            '1,0': None, '1,1': None, '1,2': None,
            '2,0': 20,   '2,1': -5,   '2,2': 15,
        }

        result_table = binary_calculator.compute_2x2_table(init_table)
        self.assertEqual(result_table, expected_table)

class TestBinaryCalculatorFunctions(unittest.TestCase):
    def setUp(self):
        app = QApplication(sys.argv)
        self.form = binary_calculator.BinaryCalculator(
            conf_level=DEFAULT_CONFIDENCE_LEVEL,
            digits=4,
        )

    def test_isconsistent_true_empty(self):
        '''
        An empty table is is consistent
        '''

        init_table = {
            '0,0': None, '0,1': None, '0,2': None,
            '1,0': None, '1,1': None, '1,2': None,
            '2,0': None, '2,1': None, '2,2': None,
        }

        self.assertTrue(self.form.is_consistent(init_table)) 

    def test_isconsistent_true(self):
        '''
        A normal, consistent table.
        '''

        init_table = {
            '0,0': None, '0,1': None, '0,2': None,
            '1,0': None, '1,1': None, '1,2': None,
            '2,0': None, '2,1': None, '2,2': None,
        }

        self.assertTrue(self.form.is_consistent(init_table)) 

    def test_isconsistent_false(self):
        '''
        A normal, consistent table.
        '''

        init_table = {
            '0,0': None, '0,1': None, '0,2': None,
            '1,0': None, '1,1': None, '1,2': None,
            '2,0': 20,   '2,1': -5,   '2,2': 15,
        }

        self.assertFalse(self.form.is_consistent(init_table)) 


if __name__ == '__main__':
    # # unittest.main(verbosity=2)
    # app = QApplication(sys.argv)
    # unittest.main()
    pass
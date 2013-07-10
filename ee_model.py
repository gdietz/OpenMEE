'''
Created on Jul 8, 2013

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *


import pdb
import string

# handrolled
from ee_dataset import EEDataSet

# Some constants
ADDITIONAL_ROWS = 100
ADDITIONAL_COLS = 40

class EETableModel(QAbstractTableModel):
    def __init__(self):
        super(EETableModel, self).__init__()
        
        self.dataset = EEDataSet()
        
        ###self.filename = filename
        self.dirty = False
        
        self.default_headers = self._generate_header_string(ADDITIONAL_COLS)
        
        # For each variable name, store its type and its column location
    

        
        # mapping from row #s (indexed from zero) to studies
        self.rows_2_studies = self._make_arbitrary_mapping_of_rows_to_studies()
        self.cols_2_vars = self._make_arbitrary_mapping_of_cols_to_variables()
        
    def _make_arbitrary_mapping_of_rows_to_studies(self):
        studies = self.dataset.get_all_studies()
        return dict(enumerate(studies))


    def _make_arbitrary_mapping_of_cols_to_variables(self):
        variable_names = self.dataset.get_all_variable_names(),
        cols2vars = {0:'label'}
        cols2vars.update(enumerate(variable_names, start=1))
        return cols2vars
        
        
    def rowCount(self, index=QModelIndex()):
        occupied_rows = self.rows_2_studies.keys()
        max_occupied_row = max(occupied_rows) if occupied_rows is not None else None
        if max_occupied_row is None:
            return ADDITIONAL_ROWS
        return max_occupied_row + ADDITIONAL_ROWS
    
#    def columnCount(self, index=QModelIndex()):
#        max_occupied_col = self.data_table.get_max_col()
#        if max_occupied_col is None:
#            return ADDITIONAL_COLS
#        return max_occupied_col + ADDITIONAL_COLS
    
#    def data(self, index, role=Qt.DisplayRole):
#        if not index.isValid() or not (0 <= index.row() < self.data_table.get_max_row()):
#            return QVariant()
#        
#        if role == Qt.DisplayRole:
#            datum = self.data_table.get_item(index.row(), index.column())
#            if datum is None:
#                return QVariant()
#            return QVariant(QString(datum))
#        return QVariant()
    
#    def headerData(self, section, orientation, role=Qt.DisplayRole):
#        if role != Qt.DisplayRole:
#            return QVariant()
#        if orientation == Qt.Horizontal:
#            return QVariant(self._get_default_header(int(section)))
#        elif orientation == Qt.Vertical:
#            return QVariant(int(section + 1))
        
#    def setData(self, index, value, role=Qt.EditRole):
#        if index.isValid() and 0 <= index.row() < self.data_table.get_max_row():
#            if self.data_table.get_item(index.row(), index.column()).toString() != value.toString():
#                self.data_table.set_item(index, col, value)
#            return True
#        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)|
                            Qt.ItemIsEditable)
        
        
        
    #def insertRows()
    #def removeRows()


    
    def _get_default_header(self, col):
        if col > len(self.default_headers):
            self._generate_header_string(col*2)
        return self.default_headers[col]
    
    def _generate_header_string(self, length):
        self.default_headers = []
        for i,label in zip(range(length), excel_column_headers()):
            self.default_headers.append(QString(label))
        return self.default_headers
        
##generate_blank_list = lambda length: [None for x in range(length)]


########### Generate Excel-style default headers ########################
# inspired by: http://thinkpython.blogspot.com/2006/10/working-with-excel-column-labels.html" '''
#def _letters():
#    ''' yields each character in sequence from the english alphabet '''
#    
#    alphabet = string.ascii_uppercase
#    for x in alphabet:
#        yield x

def excel_column_headers():
    alphabet = string.ascii_uppercase
    
    for x in alphabet:
        yield x
    for exCh in excel_column_headers():
        for x in alphabet:
            yield exCh + x
#########################################################################
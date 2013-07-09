'''
Created on Jul 8, 2013

@author: george
'''

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from sets import Set
import pdb
import string

# Some constants
ADDITIONAL_ROWS = 100
ADDITIONAL_COLS = 20

class EETableModel(QAbstractTableModel):
    def __init__(self, filename=QString()):
        super(EETableModel, self).__init__()
        
        self.filename = filename
        self.dirty = False
        
        self.default_headers = self._generate_header_string(ADDITIONAL_COLS)
        
        
        self.custom_headers = {}
        self.data_table = Table()
        
    def rowCount(self, index=QModelIndex()):
        max_occupied_row = self.data_table.get_max_row()
        if max_occupied_row is None:
            return ADDITIONAL_ROWS
        return max_occupied_row + ADDITIONAL_ROWS
    
    def columnCount(self, index=QModelIndex()):
        max_occupied_col = self.data_table.get_max_col()
        if max_occupied_col is None:
            return ADDITIONAL_COLS
        return max_occupied_col + ADDITIONAL_COLS
    
    def data(self, index, role=Qt.DisplayRole):        
        if not index.isValid() or not (0 <= index.row() < self.rowCount()):
            return QVariant()
        
        if role == Qt.DisplayRole:
            datum = self.data_table.get_item(index.row() + 1, index.column() + 1)
            if datum is None:
                return QVariant()
            return QVariant(QString(datum))
        return QVariant()
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            
            return QVariant(self._get_default_header(int(section)))
        elif orientation == Qt.Vertical:
            return QVariant(int(section + 1))

    #########################################################################
    # inspired by: http://thinkpython.blogspot.com/2006/10/working-with-excel-column-labels.html" '''
    def _letters(self):
        ''' yields each character in sequence from the english alphabet '''
        
        alphabet = string.ascii_uppercase
        for x in alphabet:
            yield x
    
    def _excel_column_letters(self):
        for x in self._letters():
            yield x
        for exCh in self._excel_column_letters():
            for x in self._letters():
                yield exCh + x
    #########################################################################
    
    def _get_default_header(self, col):
        if col > len(self.default_headers):
            self._generate_header_string(col*2)
        return self.default_headers[col]
    
    def _generate_header_string(self, length):
        self.default_headers = ""
        for i,label in zip(range(length), self._excel_column_letters()):
            self.default_headers += label
        self.default_headers = QString(self.default_headers)
        return self.default_headers
        
    #def headerData(self):
##generate_blank_list = lambda length: [None for x in range(length)]

class Table:
    # Implementation of a Table indexed from 1, not zero
    # Interface: Get and set data at row, column indices
    #
    # Invariant: Nones are implied, not stored
    # Invariant: self.rows is a set of rows (row indices) with data,
    #            self.cols is a set of cols (col indices) with data
    def __init__(self):
        self.data = {}
        
        # Set of rows that have data, Set of columns that have data
        self.rows = Set()
        self.cols = Set()
        
    def _verify_index(self, row, col):
        ''' Raises KeyError if index is invalid '''
        
        index_error_msg = "Indices must be integers greater than or equal to 1"
        if (type(row) != int) or (type(col) != int):
            raise ValueError(index_error_msg)
        if not (row,col) >= (1,1):
            raise KeyError(index_error_msg)
        
    def get_item(self, row, col):
        self._verify_index(row, col)
        
        try:
            return self.data[(row,col)]
        except KeyError:
            return None
        
    def set_item(self, row, col, value):
        self._verify_index(row, col)
        
        key = (row,col)
        self.data[key] = value
        
        # housekeeping
        self.rows.add(row)
        self.cols.add(col)
        
        # Delete the reference to the None value and remove the row and/or col
        # from the self.rows and self.cols sets if the corresponding row
        # and/or col is now empty
        if value is None:
            del self.data[key]
            if self._row_empty(row):
                self.rows.discard(row)
            if self._col_empty(col):
                self.cols.discard(col)

    def _row_empty(self, row):
        row_values = [self.get_item(row, col) for col in self.cols]
        row_empty = not any(row_values)
        
    def _col_empty(self, col):
        col_values = [self.get_item(row, col) for row in self.rows]
        col_empty = not any(col_values)
            
            
    def get_max_row(self):
        if len(self.rows) == 0:
            return None
        return max(self.rows)
    
    def get_max_col(self):
        if len(self.cols) == 0:
            return None
        return max(self.cols)        
        
#################
#               #
# George Dietz  #
# CEBM@Brown    #
#               #
#################

import csv
from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_csv_export_dlg
from globals import DEFAULT_FILENAME



class CSVExportDialog(QDialog, ui_csv_export_dlg.Ui_Dialog):
    def __init__(self, model, filepath=DEFAULT_FILENAME, parent=None):
        super(CSVExportDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        filepath = DEFAULT_FILENAME if filepath is None else filepath
        self.filepath = self.adjust_file_path(filepath)
        
    
    def get_parameters(self):
        ''' get the parameters from the state of the ui objects '''
        
        self.excel_dialect = self.excel_dialect_chkbox.isChecked()
        self.quote_text_cells = self.quote_text_cells_chkbox.isChecked()
        self.include_headers = self.include_headers_chkbox.isChecked()
        self.delimiter = str(self.delimeter_le.text())
        self.quotechar = str(self.quotechar_le.text())
    
    
    def accept(self):
        self.get_parameters()
        
        if not self.validate_parameters():
            return False
        
        # get save file name 
        file_path = self.get_save_file_name()
        if not file_path:
            return False
        matrix = self.model_as_matrix(include_headers=self.include_headers)
        
        self.write_out_csv(file_path, matrix)
        QDialog.accept(self)
        
        
    def validate_parameters(self):
        # validate parameters
        if self.quotechar == "":
            QMessageBox.warning(self, "Oops", "The quote character cannot be empty")
            return False
        elif len(self.quotechar) > 1:
            QMessageBox.warning(self, "Oops", "The quote character must be a single character")
            return False
        
        if self.delimiter == "":
            QMessageBox.warning(self, "Oops", "The delimiter cannot be empty")
            return False
        elif len(self.delimiter) > 1:
            QMessageBox.warning(self, "Oops", "The delimiter must be a single character")
            return False
        
        return True
        
    
    def write_out_csv(self, file_path, matrix):
        with open(file_path, 'wb') as f:
            make_spamwriter = partial(csv.writer,
                                      f,
                                      delimiter=self.delimiter,
                                      quotechar=self.quotechar,
                                      quoting=csv.QUOTE_NONNUMERIC if self.quote_text_cells else csv.QUOTE_MINIMAL)
            if self.excel_dialect:
                spamwriter = make_spamwriter(dialect='excel')
            else:
                spamwriter = make_spamwriter()
            
            print("Writing out csv to %s" % str(file_path))
            spamwriter.writerows(matrix)
            
            
    
    def model_as_matrix(self, include_headers=True):
        row_count = self.model.get_max_occupied_row()+1
        col_count = self.model.get_max_occupied_col()+1
        
        matrix = []
        
        if include_headers:
            row = [self.header_data_from_model(column) for column in range(col_count)]
            matrix.append(row)
            
        for row_index in range(row_count):
            row = [self.data_from_model(row_index, column) for column in range(col_count)]
            matrix.append(row)
        
        return matrix
    

    def get_save_file_name(self):
        print("proposed file path: %s" % str(self.filepath))
        
        self.filepath = unicode(QFileDialog.getSaveFileName(self, "OpenMEE - Export CSV",
                                                     self.filepath, "CSV file (.csv)"))
        if self.filepath in ["", None]:
            return False
        
        self.filepath = self.adjust_file_path(self.filepath)
            
        return self.filepath
    
    
    def adjust_file_path(self, fpath):
        try:
            period_index = fpath.index('.')
            fpath = fpath[:period_index] + u".csv"
        except ValueError:
            fpath += u".csv"
        return fpath
    
    def data_from_model(self, row, col):
        is_study_row = row in self.model.rows_2_studies
        is_label_col = col == self.model.label_column
                
        if not is_study_row: # no study for this row
            return None
        
        # Get the study this to which this row refers
        study = self.model.rows_2_studies[row]
        
        if is_label_col:
            label = study.get_label()
            return label
        else: # is a variable column
            if not self.model.column_assigned_to_variable(col):
                return None
            
            # the column is assigned to a variable
            var = self.model.cols_2_vars[col]
            var_value = study.get_var(var)
            return var_value
            
        return None
    
    
    def header_data_from_model(self, column):
        #default case
        unassigned_column = column not in self.model.cols_2_vars and column != self.model.label_column
        if unassigned_column:
            return str(self.model.get_default_header(column))
        
        # there is a study label or variable assignment to the column
        is_label_col = column == self.model.label_column
        if is_label_col:
            col_name = self.model.label_column_name_label
        else: # is a variable column
            col_name = self.model.cols_2_vars[column].get_label()
        return str(col_name)
    
    
    

    
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    form = CSVExportDialog()
    form.show()
    sys.exit(app.exec_())
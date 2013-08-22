import csv

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_csv_import_dlg

from ee_model import EETableModel

class CSVImportDialog(QDialog, ui_csv_import_dlg.Ui_CSVImportDialog):
    def __init__(self, parent=None):
        super(CSVImportDialog, self).__init__(parent)
        self.setupUi(self)
    
        self.connect(self.select_file_btn, SIGNAL("clicked()"), self._select_file)
        self.connect(self.from_excel_chkbx,  SIGNAL("stateChanged(int)"), self._rebuild_display)
        self.connect(self.has_headers_chkbx, SIGNAL("stateChanged(int)"), self._rebuild_display)
        self.reimport_btn.clicked.connect(self._rebuild_display)
        
        self.file_path = None
        self._reset_data()
        
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        
        self.adjustSize()
                
    
    def isOk(self):
        # We must have a file selected
        if not self.file_path:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return
            
        if self.imported_data_ok:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def _reset_data(self):
        self.preview_table.clear()
        self.headers = []
        self.imported_data   = []
        self.imported_data_ok = True
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        
    def _select_file(self):
        self.file_path = unicode(QFileDialog.getOpenFileName(self, "OpenMeta[analyst] - Import CSV", ".", "csv files (*.csv)"))
        if self.file_path is not None and str(self.file_path) != "":
            self.file_path_lbl.setText(QString(self.file_path))
            self._rebuild_display()
            self.reimport_btn.setEnabled(True)
        else:
            self.reimport_btn.setEnabled(False)
    
    def _num_cols_consistent(self, imported_data):
        '''checks if the # columns in the imported data matrix are the same for
        each row'''
        
        num_cols_first_row = len(imported_data[0])
        for row in imported_data:
            num_cols = len(row)
            if num_cols != num_cols_first_row:
                return False
        return True
            
    
    def _rebuild_display(self):
        self._reset_data()
        try:
            self.extract_data()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Whoops", "Something went wrong while trying to import csv, try again")
            self.imported_data_ok = False
            return False
        
        num_rows = len(self.imported_data)
        num_cols = len(self.imported_data[0])
    
        if len(self.imported_data) == 0:
            QMessageBox.warning(self, "Whoops", "No data in CSV!, try again")
            self.imported_data_ok = False
            return False
        
        if not self._num_cols_consistent(self.imported_data):
            QMessageBox.warning(self, "Uh-oh", "The number of columns in the file is not consistent, did you choose the right delimiter?")
            return False
        
        # set up table
        self.preview_table.setRowCount(num_rows)
        self.preview_table.setColumnCount(num_cols)
        if self.headers != []:
            self.preview_table.setHorizontalHeaderLabels(self.headers)
        else:
            preview_header_labels = EETableModel.get_default_header_string_of_length(num_cols)
            self.preview_table.setHorizontalHeaderLabels(preview_header_labels)
        
        # copy extracted data to table
        for row in range(num_rows):
            for col in range(num_cols):
                item = QTableWidgetItem(QString(self.imported_data[row][col]))
                item.setFlags(Qt.NoItemFlags)
                self.preview_table.setItem(row,col,item)
        self.preview_table.resizeRowsToContents()
        self.preview_table.resizeColumnsToContents()
        

        # Enable ok button if the data is ok        
        self.isOk()
    
    def extract_data(self):
        with open(self._get_filepath(), 'rU') as csvfile:
            args_csv_reader = {'delimiter': self._get_delimter(),
                               'quotechar': self._get_quotechar(),
                               }
            if self._isFromExcel():
                #args_csv_reader = {}
                args_csv_reader['dialect']='excel'
            
            # set up reader object
            reader = csv.reader(csvfile, **args_csv_reader)
            
            self.headers = []
            self.imported_data = []
            if self._hasHeaders():
                self.headers = reader.next()
            for row in reader:
                # handle missing missing data string
                missing_data_string = str(self.missing_data_le.text())
                convert_missing_data_to_empty_str = lambda x: '' if x==missing_data_string else x
                row = [convert_missing_data_to_empty_str(cell) for cell in row ]
                self.imported_data.append(row)
                
            
                
        self.print_extracted_data() # just for debugging
        
    def print_extracted_data(self):
        print("Data extracted from csv:")
        print(self.headers)
        for row in self.imported_data:
            print(str(row))
            
    def get_csv_data(self):
        ''' Imported data is a list of rows. A row is a list of
        cell contents (as strings) '''
        
        if self.imported_data_ok:
            return {'headers':self.headers,
                    'data':self.imported_data}
        else:
            print("Something went wrong while trying to import from csv")
            return None

    def _get_filepath(self):
        return str(self.file_path)
    def _isFromExcel(self):
        return self.from_excel_chkbx.isChecked()
    def _hasHeaders(self):
        return self.has_headers_chkbx.isChecked()
    def _get_delimter(self):
        return str(self.delimter_le.text())
    def _get_quotechar(self):
        return str(self.quotechar_le.text())
    
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    form = CSVImportDialog()
    form.show()
    sys.exit(app.exec_())
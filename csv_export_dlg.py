import csv

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_csv_export_dlg

from ee_model import EETableModel

class CSVExportDialog(QDialog, ui_csv_export_dlg.Ui_Dialog):
    def __init__(self, parent=None):
        super(CSVExportDialog, self).__init__(parent)
        self.setupUi(self)
    
        #self.connect(self.from_excel_chkbx,  SIGNAL("stateChanged(int)"), self._rebuild_display)
        #self.connect(self.has_headers_chkbx, SIGNAL("stateChanged(int)"), self._rebuild_display)
        # TODO: finish this
        
        self.file_path = None


    def _get_filepath(self):
        return str(self.file_path)
    def _get_delimter(self):
        return str(self.delimeter_le.text())
    def _get_quotechar(self):
        return str(self.quotechar_le.text())
    
    
    
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    form = CSVExportDialog()
    form.show()
    sys.exit(app.exec_())
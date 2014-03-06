import os.path
from python_to_R import exR

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_rlog_dlg

class RLogDialog(QDialog, ui_rlog_dlg.Ui_Dialog):
    def __init__(self, parent=None):
        super(RLogDialog, self).__init__(parent)
        self.setupUi(self)
        
        # delete dialog on close
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        
        self.plainTextEdit.clear()
        self._clear_filepath()
        self.enable_record_button()
        
        self.recording = False
        self.record_pushButton.clicked.connect(self.record_clicked)
        self.save_file_PushButton.clicked.connect(self.get_filename)
        self.inject_command_pushButton.clicked.connect(self.inject_command)
    
    def inject_command(self):
        command_str = str(self.command_lineEdit.text())
        if command_str == "":
            return
        exR.execute_in_R(command_str, show_output=self.show_output_checkBox.isChecked())
        self.command_lineEdit.clear()
    
    def _clear_filepath(self):
        self.file_path = ""
        self.file_path_Label.setText("No path set")
    
    def get_filename(self):
        home_dir = os.path.expanduser("~")
        default_filepath = os.path.join(home_dir, "open_mee_r_log.txt")
        
        file_path = QFileDialog.getSaveFileName(
                        parent=self,
                        caption=QString("Choose text file for log output."),
                        directory=default_filepath,
                        filter = "Text files (*.txt)",
                        selectedFilter = "Text files (*.txt)",
                        options=QFileDialog.DontConfirmOverwrite)
        file_path = unicode(file_path)
        
        file_path = self._verify_or_ending_to_file_path(file_path, ending=".txt")
        self.file_path = file_path
        
        # set label
        fp_label_txt = file_path if not self._filepath_blank() else "No path set"
        self.file_path_Label.setText(fp_label_txt)

        self.enable_record_button()
        
        print("Will record to %s" % self.file_path)
        
    def _verify_or_ending_to_file_path(self, fpath, ending=".txt"):
        try:
            rightmost_dot_index = fpath.rindex('.')
            no_dot = False
        except:
            no_dot = True
            
        dot_present = not no_dot
        if dot_present: 
            if fpath[rightmost_dot_index:] != ending:
                fpath = fpath[:rightmost_dot_index] + ending
        else:
            fpath = fpath + ending
        return fpath
        
        
    def _filepath_blank(self):
        if self.file_path in [None, ""]:
            return True
        
        if self.file_path.split('.')[0] == "":
            return True
        return False
        
        
    
    def enable_record_button(self):
        if self._filepath_blank():
            self.record_pushButton.setEnabled(False)
        else:
            self.record_pushButton.setEnabled(True)
        
    def append(self, text):
        self.plainTextEdit.appendPlainText("".join([text,"\n"]))
    
        if self.recording and not self._filepath_blank():
            with open(self.file_path, 'a') as f:
                    f.write(text)
                    f.write("\n\n")
        
    def record_clicked(self):
        if self.recording:
            self.recording = False
            self.record_pushButton.setText("Start Recording...")
        else:
            self.recording = True
            self.record_pushButton.setText("Stop Recording...")
            
            
            
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    form = RLogDialog()
    form.show()
    sys.exit(app.exec_())
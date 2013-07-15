'''
Created on Jul 12, 2013

@author: george
'''


# Collection of small but useful dialogs that it would be overkill to make in
# Qt Designer


from PyQt4.QtCore import *
from PyQt4.QtGui import *

class InputForm(QDialog):
    def __init__(self, message="Dummy Message", initial_text="", parent=None):
        super(InputForm, self).__init__(parent=parent)
        
        self.msg_label = QLabel(message)
        self.input_linedit = QLineEdit(initial_text)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.msg_label)
        vlayout.addWidget(self.input_linedit)
        vlayout.addWidget(buttonBox)
        
        
        self.setLayout(vlayout)
        
        self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
        self.connect(buttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
        
    def get_text(self):
        return self.input_linedit.text()
        
     
class UndoViewForm(QDialog):
    ''' Form to view an undo stack visually '''
    
    def __init__(self, undo_stack, model, parent=None):
        super(UndoViewForm, self).__init__(parent=None)
        
        
        self.setWindowTitle(QString("Undo Stack"))
        self.undo_stack = undo_stack
        self.model = model
        
        self.print_model_btn = QPushButton("Print Model", parent=self)
        self.undoView = QUndoView(self.undo_stack)
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.undoView)
        vlayout.addWidget(self.print_model_btn)
        self.setLayout(vlayout)
        
        QObject.connect(self.print_model_btn, SIGNAL("clicked()"), self._print_model_info)
        
    def _print_model_info(self):
        print(self.model)
        
        
        
        
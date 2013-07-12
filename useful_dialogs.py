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
        super(InputForm, self).__init__(parent)
        
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
        
        
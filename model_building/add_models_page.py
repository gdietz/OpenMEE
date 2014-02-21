from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_add_models_page

class AddModelsPage(QWizardPage, ui_add_models_page.Ui_WizardPage):
    
    reduced_model_created = pyqtSignal()
    
    def __init__(self, parent=None):
        super(AddModelsPage, self).__init__(parent)
        self.setupUi(self)
        
    def initializePage(self):
        covariates = self.wizard.get_included_covariates()
        interactions = self.wizard.get_included_interactions()
        
        self.model_listWidget.clear()
        
        # Generate Full model and add to models list
        self.full_model = {'name':"Full Model",
                           'covariates':covariates,
                           'interactions':interactions}
        self.full_model_item = QListWidgetItem(self.full_model['name'])
        self.full_model_item.setFlags(~Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.model_listWidget.addItem(self.full_model_item)
        
        self.reduced_model = None
        
        
        
    def __str__(self):
        full_model_str = ""
        reduced_model_str = ""
        return ""
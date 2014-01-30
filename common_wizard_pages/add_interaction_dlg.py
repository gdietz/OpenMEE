from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_add_interaction
from interaction import Interaction
        
class AddInteractionDlg(QDialog, ui_add_interaction.Ui_Dialog):
    def __init__(self, covariates, existing_interactions, possible_interactions, parent=None):
        super(AddInteractionDlg, self).__init__(parent)
        self.setupUi(self)
        
        self.covariates = covariates
        self.possible_interactions = possible_interactions
        self.existing_interactions = existing_interactions
        
        self.items_to_covs = {}
        self.interaction = None
        
        self.populate_listwidget()
        self.item_selection_changed()
        
        self.listWidget.itemSelectionChanged.connect(self.item_selection_changed)
        self.make_pushButton.clicked.connect(self.make_interaction)
        
    
    def populate_listwidget(self):
        self.listWidget.clear()
        
        sorted_covariates = sorted(self.covariates, key=lambda cov: cov.get_label())
        for cov in sorted_covariates:
            item = QListWidgetItem(cov.get_label())
            self.items_to_covs[item] = cov
            self.list_widget.addItem(item)
            
    def item_selection_changed(self):
        ### enable/disable make interaction button ###
        # right # of covariates selected?
        if len(self.listWidget.selectedItems()) > 2:
            self.status_label.setText("Maximum of two covariates allowed")
            self.make_pushButton.setEnabled(False)
            return
        if len(self.listWidget.selectedItems()) < 2:
            self.status_label.setText("At least two covariates must be selected")
            self.make_pushButton.setEnabled(False)
            return
        
        # Is the interaction already present?
        selected_covs = [self.items_to_covs[item] for item in self.listWidget.selectedItems()]
        candidate_interaction = Interaction(selected_covs)
        if candidate_interaction in self.existing_interactions:
            self.status_label.setText("Interaction already exists.")
            self.make_pushButton.setEnabled(False)
            return
        
        # is the interaction possible?
        if candidate_interaction not in self.possible_interactions:
            self.status_label.setText("Interaction is impossible, don't ask me why")
            self.make_pushButton.setEnabled(False)
            return

        self.status_label.setText("")
        self.make_pushButton.setEnabled(True)
        
    
    def make_interaction(self):
        selected_covs = [self.items_to_covs[item] for item in self.listWidget.selectedItems()]
        self.interaction = Interaction(selected_covs)
        
    ##### Getter ####
    def get_interaction(self):
        return self.interaction
        
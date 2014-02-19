from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_add_interaction
from interaction import Interaction

MIN_NCOV = 2
MAX_NCOV = 2
        
class AddInteractionDlg(QDialog, ui_add_interaction.Ui_Dialog):
    def __init__(self, covariates, existing_interactions, possible_interactions, parent=None):
        super(AddInteractionDlg, self).__init__(parent)
        self.setupUi(self)
        
        self.covariates = covariates
        self.possible_interactions = possible_interactions
        self.existing_interactions = existing_interactions
        
        self.items_to_covs = {}

        self.populate_listwidget()
        self.item_changed()
        
        self.listWidget.itemChanged.connect(self.item_changed)
        
    
    def populate_listwidget(self):
        self.listWidget.clear()
        
        sorted_covariates = sorted(self.covariates, key=lambda cov: cov.get_label())
        for cov in sorted_covariates:
            item = QListWidgetItem(cov.get_label())
            if len(sorted_covariates)==MIN_NCOV:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.items_to_covs[item] = cov
            self.listWidget.addItem(item)
            
    def get_checked_items(self):
        checked = []
        for row in range(self.listWidget.count()):
            item = self.listWidget.item(row)
            if item.checkState() == Qt.Checked:
                checked.append(item)
        return checked
            
    def item_changed(self):
        ### enable/disable ok button ###
        # right # of covariates checked?
        
        checked_items = self.get_checked_items()
        
        if len(checked_items) > 2:
            self.status_label.setText("Maximum of two covariates allowed")
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        if len(checked_items) < 2:
            self.status_label.setText("At least two covariates must be selected")
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        
        # Is the interaction already present?
        checked_covs = [self.items_to_covs[item] for item in checked_items]
        candidate_interaction = Interaction(checked_covs)
        if candidate_interaction in self.existing_interactions:
            self.status_label.setText("Interaction already exists.")
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        
        # is the interaction possible?
        if candidate_interaction not in self.possible_interactions:
            self.status_label.setText("Interaction is impossible, don't ask me why")
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return

        self.status_label.setText("")
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
    
    def make_interaction(self):
        checked_items = self.get_checked_items()
        checked_covs = [self.items_to_covs[item] for item in checked_items]
        return Interaction(checked_covs)
        
    ##### Getter ####
    def get_interaction(self):
        return self.make_interaction()
        
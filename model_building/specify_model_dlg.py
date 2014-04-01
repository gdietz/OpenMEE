from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import ui_specify_model

MAX_MODELS = 2

class SpecifyModelDlg(QDialog, ui_specify_model.Ui_Dialog):
    
    selections_changed = pyqtSignal()
    
    def __init__(self, covariates, interactions, default_name="", parent=None):
        super(SpecifyModelDlg, self).__init__(parent)
        self.setupUi(self)
        
        self.name_lineEdit.setText(default_name)
        
        self.item2cov = {}
        self.item2interaction = {}
        
        self.covariate_choices = covariates
        self.interaction_choices = interactions
        self._populate_covariates_listWidget(covariates)
        self._populate_interactions_listWidget(interactions)
        
        self.selected_covariates = []
        self.selected_interactions = []
        self._make_sure_interactions_allowed()
        
        # connect signals
        self.covariates_listWidget.itemChanged.connect(self.change_selected_covariates)
        self.Interactions_listWidget.itemChanged.connect(self.change_selected_interactions)
        self.selections_changed.connect(self._change_ok_button_enable_status)
    
    def change_selected_covariates(self, item):
        cov = self.item2cov[item]
        if item.checkState() == Qt.Checked:
            if cov not in self.selected_covariates:
                self.selected_covariates.append(cov)
        elif item.checkState() == Qt.Unchecked:
            try:
                self.selected_covariates.remove(cov)
            except ValueError: # cov is not there
                pass
        else:
            raise Exception("This item should not be tristate")
        
        self._make_sure_interactions_allowed()
        
        self.selections_changed.emit()
    
    def _make_sure_interactions_allowed(self):
        # Disables(enables) interactions if the covariates comprising them are
        # not selected
        
        # Make sure that the interactions are allowed, given the chosen covariates
        for inter_item, interaction in self.item2interaction.items():
            variables = set(interaction.get_vars())
            if not all([var in self.selected_covariates for var in variables]):
                # variables in interaction is not a subset of the selected covariates
                # so uncheck and disable the interaction
                inter_item.setFlags(inter_item.flags()&~Qt.ItemIsEnabled)
                inter_item.setCheckState(Qt.Unchecked)
            else:
                inter_item.setFlags(inter_item.flags()|Qt.ItemIsEnabled)
        
    def change_selected_interactions(self, item):
        interaction = self.item2interaction[item]
        if item.checkState() == Qt.Checked:
            if interaction not in self.selected_interactions:
                self.selected_interactions.append(interaction)
        elif item.checkState() == Qt.Unchecked:
            try:
                self.selected_interactions.remove(interaction)
            except ValueError: # interaction not there
                pass
        else:
            raise Exception("This item should not be tristate")
        
        self.selections_changed.emit()
        
    def _change_ok_button_enable_status(self):
        ok_button = self.buttonBox.button(QDialogButtonBox.Ok)
        n_possible_covs = len(self.covariate_choices)
        n_possible_interactions = len(self.interaction_choices)
        n_selected_covs = len(self.selected_covariates)
        n_selected_interactions = len(self.selected_interactions)
        
        # Make sure that the the terms in this model are a strict subset of the
        # possible terms
        n_possible_terms = n_possible_covs + n_possible_interactions
        n_selected_terms = n_selected_covs + n_selected_interactions
        
        if n_selected_terms < n_possible_terms:
            ok_button.setToolTip("")
            ok_button.setEnabled(True)
        else:
            ok_button.setToolTip("The terms you choose must be strict subset of the choices available")
            ok_button.setEnabled(False)
            
        
    def _populate_covariates_listWidget(self, covariates):
        self.covariates_listWidget.blockSignals(True)
        
        for cov in covariates:
            item = QListWidgetItem(cov.get_label())
            item.setCheckState(Qt.Unchecked)
            self.covariates_listWidget.addItem(item)
            self.item2cov[item] = cov
            
        self.covariates_listWidget.blockSignals(False)
        
        
    def _populate_interactions_listWidget(self, interactions):
        self.Interactions_listWidget.blockSignals(True)
        
        for x in interactions:
            item = QListWidgetItem(str(x))
            item.setCheckState(Qt.Unchecked)
            self.Interactions_listWidget.addItem(item)
            self.item2interaction[item]=x
        
        self.Interactions_listWidget.blockSignals(False)
        
    ####### interface out ######
    
    def get_name(self):
        return str(self.name_lineEdit.text())
    
    def get_covariates(self):
        return self.selected_covariates
    
    def get_interactions(self):
        return self.selected_interactions
    
        
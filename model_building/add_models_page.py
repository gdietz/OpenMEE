from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from specify_model_dlg import SpecifyModelDlg
import ui_add_models_page

from ome_globals import *

# We are limited to 2 models for now (just Full and Reduced) but the code has
# been written to allow support for more in the future without too much fuss

MAX_MODELS = 2 

class AddModelsPage(QWizardPage, ui_add_models_page.Ui_WizardPage):
    
    models_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super(AddModelsPage, self).__init__(parent)
        self.setupUi(self)
        
    def initializePage(self):
        covariates = self.wizard().get_included_covariates()
        interactions = self.wizard().get_included_interactions()
        
        self.model_listWidget.clear()
    
        # Dict containing subdict with info about the models:
        # By convention, the model at row zero is the 'Full' Model
        # {0: {'name': "my model",
        #      'covariates':covariates, # list
        #      'interactions':interactions, # a list
        #     },
        # }
        self.row_2_model_info = {}
        
        
        # Generate Full model and add to models dict
        self._add_model("Full Model", covariates, interactions)
        
        
        self._change_buttons_enable_state()
        self._populate_info_area()
        
        # Make connections
        self.models_changed.connect(self._change_buttons_enable_state)
        self.model_listWidget.itemSelectionChanged.connect(self._populate_info_area)
        self.add_model_PushButton.clicked.connect(self.add_model_button_clicked)
        self.remove_last_model_Pushbutton.clicked.connect(self.remove_last_model_button_clicked)

    def _populate_info_area(self):
        current_model_info = self._get_current_model_info()
        covariate_names = self._covariates_labels(current_model_info['covariates'])
        interaction_names = self._interactions_labels(current_model_info['interactions'])
        
        self.model_name_Label.setText(current_model_info['name'])
        self.covariates_list_Label.setText("\n".join(covariate_names))
        self.interactions_list_Label.setText("\n".join(interaction_names))
    
    def _covariates_labels(self, covariates):
        labels = [cov.get_label() for cov in covariates]
        return labels
    
    def _interactions_labels(self, interactions):
        labels = [str(interaction) for interaction in interactions]
        return labels
        
        
    def _change_buttons_enable_state(self):
        # Add enabled when the model count is < MAX_MODELS
        # Remove enabled when the model count is > 1
        nmodels = self.model_listWidget.count()
        
        if nmodels < MAX_MODELS:
            self.add_model_PushButton.setEnabled(True)
        else:
            self.add_model_PushButton.setEnabled(False)
            
        if nmodels > 1:
            self.remove_last_model_Pushbutton.setEnabled(True)
        else:
            self.remove_last_model_Pushbutton.setEnabled(False)
                        
    def add_model_button_clicked(self):
        last_model_info = self._get_last_model_info()
        allowed_covariates = last_model_info['covariates']
        allowed_interactions = last_model_info['interactions']
        
        dlg = SpecifyModelDlg(default_name="Reduced Model",
                              covariates=allowed_covariates,
                              interactions=allowed_interactions)
        if dlg.exec_():
            name = dlg.get_name()
            covariates = dlg.get_covariates()
            interactions = dlg.get_interactions()
            
            self._add_model(name=name,
                            covariates=covariates,
                            interactions=interactions)
            
            self.models_changed.emit()
        
    def _add_model(self, name, covariates, interactions, enabled=True, selectable=True):
        enabled_flag = Qt.ItemIsEnabled if enabled else ~Qt.ItemIsEnabled
        selectable_flag = Qt.ItemIsSelectable if selectable else ~Qt.ItemIsSelectable
        
        item = QListWidgetItem(name)
        item.setFlags(enabled_flag|selectable_flag)
        
        info = {'name': name,
                'covariates':covariates,
                'interactions':interactions}
        
        self.model_listWidget.addItem(item)
        self.row_2_model_info[self.model_listWidget.count()-1] = info
        self.model_listWidget.setCurrentItem(item)
        self.models_changed.emit()
    
    def remove_last_model_button_clicked(self):
        last_index = self.model_listWidget.count() - 1
        self.model_listWidget.takeItem(last_index)
        del self.row_2_model_info[last_index]
        self.models_changed.emit()
        
    def _get_last_model_info(self):
        last_index = self.model_listWidget.count() - 1
        return self.row_2_model_info[last_index]
    
    def _get_current_model_info(self):
        current_row = self.model_listWidget.currentRow()
        return self.row_2_model_info[current_row]
    
    # Use this to get the model info out
    def get_models_info(self):
        model_row_info_tuples = self.row_2_model_info.items()
        # sort by row
        model_row_info_tuples.sort(key=lambda x: x[0])
        
        _, infos = zip(*model_row_info_tuples)
        
        return infos # where info is a dictionary as specified above

    def __str__(self):
        summary = "Models:\n-----------------\n"
        model_summaries = []
        
        for i, info in enumerate(self.get_models_info()):
            name_part = "Name: %s" % info['name']
            if i == 0:
                name_part += "(Full Model)"
            covariate_labels = self._covariates_labels(info['covariates'])
            interaction_labels = self._interactions_labels(info['interactions'])
            covariates_part = "Covariates:\n%s" % indent("\n".join(interaction_labels))
            interactions_part = "Interactions\n%s" % indent("\n".join(covariate_labels))
            model_summary = "\n".join([name_part, covariates_part, interactions_part])
            model_summaries.append(model_summary)
            
        summary += "\n\n".join(model_summaries)
        return summary
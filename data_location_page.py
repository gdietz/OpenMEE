from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *


class DataLocationPage(QWizardPage):
    def __init__(self, model, parent=None):
        super(DataLocationPage, self).__init__(parent)

        
        self.model = model
        self.data_type = None
        self.setSubTitle("In what columns is the data located?")
        
        self.continuous_columns = self.model.get_continuous_columns()
        self.count_columns = self.model.get_count_columns()
        
        
        
    def initializePage(self):
        self.data_type = self.wizard().selected_data_type
        
        layout = self.layout()
        if layout is None:
            layout = QGridLayout()
            self.setLayout(layout)
            
        # clear layout
        unfill_layout(layout)
        
        if self.data_type == MEANS_AND_STD_DEVS:
            self._setup_MEAN_AND_STD_DEV_table(layout)
        elif self.data_type == TWO_BY_TWO_CONTINGENCY_TABLE:
            self._setup_TWO_BY_TWO_CONTINGENCY_table(layout)
        elif self.data_type == CORRELATION_COEFFICIENTS:
            self._setup_CORRELATION_COEFFICIENTS_table(layout)
        else:
            raise Exception("Unrecognized Data type")
            
            
    def _setup_MEAN_AND_STD_DEV_table(self, layout):
        # top row labels
        layout.addWidget(QLabel("Control Group"), 0, 1)
        layout.addWidget(QLabel("Experimental Group"), 0, 2)
        # left column labels
        layout.addWidget(QLabel("Mean"), 1, 0)
        layout.addWidget(QLabel("Stand. Dev."), 2, 0)
        layout.addWidget(QLabel("Sample Size"), 3, 0)
        
        # control group combo boxes
        self.control_mean_combo_box = QComboBox()
        self.control_std_dev_combo_box = QComboBox()
        self.control_sample_size_combo_box = QComboBox()
        
        layout.addWidget(self.control_mean_combo_box       , 1, 1)
        layout.addWidget(self.control_std_dev_combo_box    , 2, 1)
        layout.addWidget(self.control_sample_size_combo_box, 3, 1)
        
        # experimental group combo boxes
        self.experimental_mean_combo_box = QComboBox()
        self.experimental_std_dev_combo_box = QComboBox()
        self.experimental_sample_size_combo_box = QComboBox()
        
        layout.addWidget(self.experimental_mean_combo_box       , 1, 2) 
        layout.addWidget(self.experimental_std_dev_combo_box    , 2, 2)
        layout.addWidget(self.experimental_sample_size_combo_box, 3, 2)
        
        self.continuous_combo_boxes = [self.control_mean_combo_box,
                                       self.control_std_dev_combo_box,
                                       self.experimental_mean_combo_box,
                                       self.experimental_std_dev_combo_box,]
        self.counts_combo_boxes = [self.control_sample_size_combo_box,
                                   self.experimental_sample_size_combo_box,]
        
        self._populate_combo_boxes(self.continuous_combo_boxes, self.continuous_columns)
        self._populate_combo_boxes(self.counts_combo_boxes, self.count_columns)
        
        # connect boxes to update of selections
        for box in self.continuous_combo_boxes + self.counts_combo_boxes:
            QObject.connect(box, SIGNAL("currentIndexChanged(int)"), self._update_current_selections)
            
    
    def _setup_TWO_BY_TWO_CONTINGENCY_table(self, layout):
        # top row labels
        layout.addWidget(QLabel("Control"), 0, 1)
        layout.addWidget(QLabel("Treatment"), 0, 2)
        # left column labels
        layout.addWidget(QLabel("Response"), 1, 0)
        layout.addWidget(QLabel("No Response"), 2, 0)
        
        # control combo boxes
        self.control_response_combo_box = QComboBox()
        self.control_noresponse_combo_box = QComboBox()
        layout.addWidget(self.control_response_combo_box, 1, 1)
        layout.addWidget(self.control_noresponse_combo_box, 2, 1)
        
        # treatment combo_boxes
        self.experimental_response_combo_box = QComboBox()
        self.experimental_noresponse_combo_box = QComboBox()
        layout.addWidget(self.experimental_response_combo_box, 1, 2)
        layout.addWidget(self.experimental_noresponse_combo_box, 2, 2)
        
        self.counts_combo_boxes = [self.control_response_combo_box,
                                   self.control_noresponse_combo_box,
                                   self.experimental_noresponse_combo_box, 
                                   self.experimental_response_combo_box]
        
        self._populate_combo_boxes(self.counts_combo_boxes, self.count_columns)
        
        for box in self.counts_combo_boxes:
            QObject.connect(box, SIGNAL("currentIndexChanged(int)"), self._update_current_selections)

        
    def _setup_CORRELATION_COEFFICIENTS_table(self, layout):
        # top row labels
        layout.addWidget(QLabel("Correlation"), 0, 1)
        layout.addWidget(QLabel("Sample Size"), 0, 2)
        
        self.correlation_combo_box = QComboBox()
        self.sample_size_combo_box = QComboBox()
        layout.addWidget(self.correlation_combo_box, 1, 1)
        layout.addWidget(self.sample_size_combo_box, 1, 2)
        
        self._populate_combo_boxes([self.correlation_combo_box,], self.continuous_columns)
        self._populate_combo_boxes([self.sample_size_combo_box,], self.count_columns)
        
        for box in [self.correlation_combo_box, self.sample_size_combo_box]:
            QObject.connect(box, SIGNAL("currentIndexChanged(int)"), self._update_current_selections)
            
    def _populate_combo_boxes(self, combo_boxes, columns):
        ''' Populates combo boxes that are 'continuous' with list of continuous
        -type columns'''
        
        for box in combo_boxes:
            box.blockSignals(True)
            box.clear()
            box.addItem("", QVariant(-1)) # -1 meaning no choice
            key_fn = lambda col: self.model.get_variable_assigned_to_column(col).get_label() # sort by column label
            for col in sorted(columns, key=key_fn):
                var = self.model.get_variable_assigned_to_column(col)
                box.addItem(var.get_label(), col) # store the chosen col
            box.setCurrentIndex(0)
            box.blockSignals(False)
            
    def _get_current_selections(self):
        ''' Returns a dictionary mapping fields to combo_box_selections(columns) '''
        
        def selected_column(combo_box):
            item_data = combo_box.itemData(combo_box.currentIndex())
            selected_column = item_data.toInt()[0]
            if selected_column == -1:
                return None
            return selected_column
        
        if self.data_type == MEANS_AND_STD_DEVS:
            current_selections = {
                    'control_mean'            : selected_column(self.control_mean_combo_box),
                    'control_std_dev'         : selected_column(self.control_std_dev_combo_box),
                    'control_sample_size'     : selected_column(self.control_sample_size_combo_box),
                    'experimental_mean'       : selected_column(self.experimental_mean_combo_box),
                    'experimental_std_dev'    : selected_column(self.experimental_std_dev_combo_box),
                    'experimental_sample_size': selected_column(self.experimental_sample_size_combo_box),}
        elif self.data_type == TWO_BY_TWO_CONTINGENCY_TABLE:
            current_selections = {'control_response'    : selected_column(self.control_response_combo_box),
                                  'control_noresponse'  : selected_column(self.control_noresponse_combo_box),
                                  'experimental_response'  : selected_column(self.experimental_response_combo_box),
                                  'experimental_noresponse': selected_column(self.experimental_noresponse_combo_box),
                                  }
        elif self.data_type == CORRELATION_COEFFICIENTS:
            current_selections = {'correlation': selected_column(self.correlation_combo_box),
                                  'sample_size': selected_column(self.sample_size_combo_box),}
        
        return current_selections
    
    def _update_current_selections(self):
        current_selections = self._get_current_selections()
        # update data location in wizard
        self.wizard().data_location = current_selections
        self.emit(SIGNAL("completeChanged()"))
            
    def isComplete(self):
        current_selections = self.wizard().data_location
        if current_selections is None:
            return False
        if None in current_selections.values():
            return False
        return True
                
                
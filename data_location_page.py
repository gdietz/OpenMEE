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
        
        #self.continuous_columns = self.model.get_continuous_columns()
        #self.count_columns = self.model.get_count_columns()
        
    def initializePage(self):
        self.data_type = self.wizard().selected_data_type
        
        layout = self.layout()
        if layout is None:
            layout = QGridLayout()
            self.setLayout(layout)
            
        # clear layout
        unfill_layout(layout)
        
        if self.data_type == MEANS_AND_STD_DEVS:
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
            
            
            
            
            
            
            
            
            self.combo_box_list = [self.control_mean_combo_box,
                                   self.control_std_dev_combo_box,
                                   self.control_sample_size_combo_box,
                                   self.experimental_mean_combo_box,
                                   self.experimental_std_dev_combo_box,
                                   self.experimental_sample_size_combo_box,]
            
            self.continuous_combo_boxes = [self.control_mean_combo_box,
                                           self.control_std_dev_combo_box,
                                           self.experimental_mean_combo_box,
                                           self.experimental_std_dev_combo_box,]
            
            self.counts_combo_boxes = [self.control_sample_size_combo_box,
                                       self.experimental_sample_size_combo_box,]
            
            #self.populate_continuous_combo_boxes(self.continuous_combo_boxes)
            #self.populate_counts_combo_boxes(self.counts_combo_boxes)
            
            

            
            
    def _get_selected_columns(self):
        ''' returns a list of the currently selected columns (their indices) '''
        pass
        #TODO
           
            
                                    
            
        
        
        #self._populate_data_type_groupBox()
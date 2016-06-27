#################
#               #
# George Dietz  #
# CEBM@Brown    #
#               #
#################

#from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

class DataLocationPage(QWizardPage):
    def __init__(
        self,
        model,
        show_raw_data=True,
        enable_raw_correlation_data=False,
        linkage_checkbox=False, 
        effect_size=True,
        need_full_raw_data=False,
        parent=None,
    ):
        super(DataLocationPage, self).__init__(parent)

        self.model = model
        self.data_type = None
        self.metric = None
        self.raw_data = show_raw_data
        self.enable_raw_correlation_data = enable_raw_correlation_data
        self.linkage_checkbox = linkage_checkbox
        self.effect_size = effect_size
        self.need_full_raw_data = need_full_raw_data
        
        self.setSubTitle("In what columns is the data located?")
        
        self.continuous_columns = self.model.get_continuous_columns()
        self.count_columns = self.model.get_count_columns()
        self.effect_columns = [col for col in self.continuous_columns if self._col_assigned_to_effect_variable(col)]
        self.variance_columns = [col for col in self.continuous_columns if self._col_assigned_to_variance_variable(col)]

        self.effect_and_var_boxes_exist = False
        
        self.box_names_to_boxes = {}

        print "Raw data: %s" % self.raw_data


        
    def set_show_raw_data(self, show_raw_data):
        self.raw_data = show_raw_data
    
    def _col_assigned_to_effect_variable(self, col):
        var = self.model.get_variable_assigned_to_column(col)
        if var.get_subtype() == TRANS_EFFECT:
            return True
        else:
            return False
    
    def _col_assigned_to_variance_variable(self, col):
        var = self.model.get_variable_assigned_to_column(col)
        if var.get_subtype() == TRANS_VAR:
            return True
        else:
            return False

    
    def initializePage(self):
        if self.raw_data:
            self.data_type, self.metric = self.wizard().get_data_type_and_metric()
        
        vlayout = self.layout()
        if vlayout is None:
            vlayout = QVBoxLayout()
            self.setLayout(vlayout)
            
        # clear layout
        unfill_layout(vlayout)
        
        # make grid layout
        layout = QGridLayout()
        
        calculate_ma_data_loc_instructions = "When performing an analysis only the options in the bottom two boxes need to be chosen. However, choosing options for the boxes above may provide more options when plotting."
        instructions_label = QLabel(calculate_ma_data_loc_instructions)
        instructions_label.setWordWrap(True)
        
        vlayout.addWidget(instructions_label)
            
        vlayout.addLayout(layout) # grid layout with column choices
        
        # Add raw data combo boxes
        if self.raw_data:
            if self.data_type == MEANS_AND_STD_DEVS:
                if self.metric != GENERIC_EFFECT:
                    self._setup_MEAN_AND_STD_DEV_table(
                        layout,
                        startrow=layout.rowCount(),
                    )
                else:
                    pass # don't choose data location columns for generic effect
            elif self.data_type == TWO_BY_TWO_CONTINGENCY_TABLE:
                self._setup_TWO_BY_TWO_CONTINGENCY_table(
                    layout,
                    startrow=layout.rowCount(),
                )
            elif self.data_type == PROPORTIONS:
                self._setup_PROPORTIONS_table(
                    layout,
                    startrow=layout.rowCount(),
                )
            elif self.data_type == CORRELATION_COEFFICIENTS:
                self._setup_CORRELATION_COEFFICIENTS_table(
                    layout,
                    startrow=layout.rowCount(),
                )
            else:
                raise Exception("Unrecognized Data type")
        
        if self.effect_size:
            eff_var_layout = QGridLayout()
            
            # Lables:
            eff_var_layout.addWidget(QLabel("\nEffect Size"), 0, 0)
            eff_var_layout.addWidget(QLabel("\nVariance"), 0, 1)
            self.effect_size_combo_box = QComboBox()
            self.variance_combo_box = QComboBox()
            self.effect_and_var_boxes_exist = True
            eff_var_layout.addWidget(self.effect_size_combo_box, 1, 0)
            eff_var_layout.addWidget(self.variance_combo_box, 1, 1)
            
            # add layout to larger layout
            rowcount = layout.rowCount()
            layout.addLayout(eff_var_layout, rowcount, 0, 1, 2)
            
            self.box_names_to_boxes.update({
                'effect_size': self.effect_size_combo_box,
                'variance'   : self.variance_combo_box,
            })
            
            self._populate_combo_boxes(
                [self.effect_size_combo_box,],
                self.effect_columns,
                preselect_only_one=True,
            )
            self._populate_combo_boxes(
                [self.variance_combo_box,],
                self.variance_columns,
                preselect_only_one=True,
            )
            
            # connect boxes to update of selections
            for box in [self.effect_size_combo_box, self.variance_combo_box]:
                QObject.connect(
                    box,
                    SIGNAL("currentIndexChanged(int)"),
                    self._update_current_selections,
                )
        

        # add clear selections button
        self.clear_selections_btn = QPushButton(QString("Clear Selections"))
        clear_selections_btn_layout = QHBoxLayout()
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        clear_selections_btn_layout.addItem(spacerItem)
        clear_selections_btn_layout.addWidget(self.clear_selections_btn)
        vlayout.addLayout(clear_selections_btn_layout)
        self.clear_selections_btn.clicked.connect(self._clear_selections)
        
        # add make linkage checkbox for when we are calculating effect sizes
        if self.linkage_checkbox:
            self.make_linkage_chkbox = QCheckBox("Establish linkage between raw-data and calculated effects")
            self.make_linkage_chkbox.setCheckState(Qt.Checked)
            vlayout.addWidget(self.make_linkage_chkbox)
        
    def should_make_link(self):
        return self.make_linkage_chkbox.isChecked()
    
    def _clear_selections(self):
        print("Clearing selections")
        
        boxes = self.box_names_to_boxes.values()

        # by convention, the blank choice is the first entry in the combo boxes
        for box in boxes:
            box.blockSignals(True)
            box.setCurrentIndex(0)
            box.blockSignals(False)
        
        self._update_current_selections()
            
    def _get_boxname_for_box(self, box):
        for name,v in self.box_names_to_boxes.items():
            if v == box:
                return name
        return None
        
    
    def _setup_MEAN_AND_STD_DEV_table(self, layout, startrow=0):
        # top row labels
        layout.addWidget(QLabel("Control Group"), startrow, 1)
        layout.addWidget(QLabel("Experimental Group"), startrow, 2)
        # left column labels
        layout.addWidget(QLabel("Mean"), startrow+1, 0)
        layout.addWidget(QLabel("Stand. Dev."), startrow+2, 0)
        layout.addWidget(QLabel("Sample Size"), startrow+3, 0)
        
        # control group combo boxes
        self.control_mean_combo_box = QComboBox()
        self.control_std_dev_combo_box = QComboBox()
        self.control_sample_size_combo_box = QComboBox()
        
        layout.addWidget(self.control_mean_combo_box       , startrow+1, 1)
        layout.addWidget(self.control_std_dev_combo_box    , startrow+2, 1)
        layout.addWidget(self.control_sample_size_combo_box, startrow+3, 1)
        
        # experimental group combo boxes
        self.experimental_mean_combo_box = QComboBox()
        self.experimental_std_dev_combo_box = QComboBox()
        self.experimental_sample_size_combo_box = QComboBox()
        
        layout.addWidget(self.experimental_mean_combo_box       , startrow+1, 2) 
        layout.addWidget(self.experimental_std_dev_combo_box    , startrow+2, 2)
        layout.addWidget(self.experimental_sample_size_combo_box, startrow+3, 2)
        
        self.continuous_combo_boxes = [
            self.control_mean_combo_box,
            self.control_std_dev_combo_box,
            self.experimental_mean_combo_box,
            self.experimental_std_dev_combo_box,
        ]

        self.counts_combo_boxes = [
            self.control_sample_size_combo_box,
            self.experimental_sample_size_combo_box,
        ]
        
        
        self.box_names_to_boxes = {             
            'control_mean'            : self.control_mean_combo_box,
            'control_std_dev'         : self.control_std_dev_combo_box,
            'control_sample_size'     : self.control_sample_size_combo_box,
            'experimental_mean'       : self.experimental_mean_combo_box,
            'experimental_std_dev'    : self.experimental_std_dev_combo_box,
            'experimental_sample_size': self.experimental_sample_size_combo_box,
        }
        
        self._populate_combo_boxes(
            self.continuous_combo_boxes,
            self.continuous_columns,
        )

        self._populate_combo_boxes(
            self.counts_combo_boxes,
            self.count_columns,
        )
        
        # connect boxes to update of selections
        for box in self.continuous_combo_boxes + self.counts_combo_boxes:
            QObject.connect(
                box,
                SIGNAL("currentIndexChanged(int)"),
                self._update_current_selections,
            )

    def _setup_TWO_BY_TWO_CONTINGENCY_table(self, layout, startrow=0):
        # top row labels
        layout.addWidget(QLabel("Control"),   startrow, 1)
        layout.addWidget(QLabel("Treatment"), startrow, 2)
        # left column labels
        layout.addWidget(QLabel("Response"),    startrow+1, 0)
        layout.addWidget(QLabel("No Response"), startrow+2, 0)
        
        # control combo boxes
        self.control_response_combo_box = QComboBox()
        self.control_noresponse_combo_box = QComboBox()
        layout.addWidget(self.control_response_combo_box,   startrow+1, 1)
        layout.addWidget(self.control_noresponse_combo_box, startrow+2, 1)
        
        # treatment combo_boxes
        self.experimental_response_combo_box = QComboBox()
        self.experimental_noresponse_combo_box = QComboBox()
        layout.addWidget(self.experimental_response_combo_box,   startrow+1, 2)
        layout.addWidget(self.experimental_noresponse_combo_box, startrow+2, 2)
        
        self.counts_combo_boxes = [
            self.control_response_combo_box,
            self.control_noresponse_combo_box,
            self.experimental_noresponse_combo_box, 
            self.experimental_response_combo_box
        ]
        
        self.box_names_to_boxes = {
            'control_response'        : self.control_response_combo_box,
            'control_noresponse'      : self.control_noresponse_combo_box,
            'experimental_response'   : self.experimental_response_combo_box,
            'experimental_noresponse' : self.experimental_noresponse_combo_box
        }
        
        self._populate_combo_boxes(self.counts_combo_boxes, self.count_columns)
        
        for box in self.counts_combo_boxes:
            QObject.connect(
                box,
                SIGNAL("currentIndexChanged(int)"),
                self._update_current_selections
            )
            
    def _setup_PROPORTIONS_table(self, layout, startrow=0):
        # Labels
        layout.addWidget(QLabel("# Events"), startrow, 0)
        layout.addWidget(QLabel("Sample Size"), startrow+1, 0)

        # combo boxes
        self.num_events_combobox = QComboBox()
        self.sample_size_combo_box = QComboBox()
        layout.addWidget(self.num_events_combobox, startrow, 1)
        layout.addWidget(self.sample_size_combo_box, startrow+1, 1)

        self.counts_combo_boxes = [
            self.num_events_combobox,
            self.sample_size_combo_box
        ]

        self.box_names_to_boxes = {
            'num_events': self.num_events_combobox,
            'sample_size': self.sample_size_combo_box,
        }

        self._populate_combo_boxes(self.counts_combo_boxes, self.count_columns)

        for box in self.counts_combo_boxes:
            QObject.connect(
                box,
                SIGNAL("currentIndexChanged(int)"),
                self._update_current_selections
            )

    def _setup_CORRELATION_COEFFICIENTS_table(self, layout, startrow=0):
        # top row labels
        layout.addWidget(QLabel("Correlation"), startrow, 1)
        layout.addWidget(QLabel("Sample Size"), startrow, 2)
        
        self.correlation_combo_box = QComboBox()
        self.sample_size_combo_box = QComboBox()
        layout.addWidget(self.correlation_combo_box, startrow+1, 1)
        layout.addWidget(self.sample_size_combo_box, startrow+1, 2)
        
        self.box_names_to_boxes = {
            'correlation': self.correlation_combo_box,
            'sample_size': self.sample_size_combo_box}
        
        
        self._populate_combo_boxes(
            [self.correlation_combo_box,],
            self.continuous_columns,
        )
        self._populate_combo_boxes(
            [self.sample_size_combo_box,],
            self.count_columns,
        )
        
        for box in [self.correlation_combo_box, self.sample_size_combo_box]:
            QObject.connect(
                box,
                SIGNAL("currentIndexChanged(int)"),
                self._update_current_selections,
            )

        # issue #202. Our current continuous data object on the R side doesn't
        # support correlation coeffectient raw data i.e. correlation coefficient
        # + sample size. Workaround is to force user to pre-calculate
        # effect size + variance using the calculation tool and then use these
        # in the meta-analysis
        if not self.enable_raw_correlation_data:
            for box in [self.correlation_combo_box, self.sample_size_combo_box]:
                box.setCurrentIndex(0) # empty choice
                box.setEnabled(False)


    def _populate_combo_boxes(self, combo_boxes, columns, preselect_only_one=False):
        ''' Populates combo boxes that are 'continuous' with list of continuous
        -type columns'''
        
        combo_boxes_in_need_of_default_choice = []
        
        for box in combo_boxes:
            box.blockSignals(True)
            box.clear()
            box.addItem("", QVariant(-1)) # -1 meaning no choice
            key_fn = lambda col: self.model.get_variable_assigned_to_column(col).get_label() # sort by column label
            for col in sorted(columns, key=key_fn):
                var = self.model.get_variable_assigned_to_column(col)
                box.addItem(var.get_label(), col) # store the chosen col
            # if there is only one choice for in columns, select it
            if preselect_only_one and len(columns)==1:
                box.setCurrentIndex(1) # select first and only column
            else:
                box.setCurrentIndex(0)
                combo_boxes_in_need_of_default_choice.append(box)
            box.blockSignals(False)
            
        self._set_default_choices_for_combo_boxes(
            combo_boxes_in_need_of_default_choice,
            columns,
        )
            
    def _set_default_choices_for_combo_boxes(self, combo_boxes, columns):
        ''' Sets the default choice for the combo boxes from the last time the
        dialog was open (assuming that the column is still a valid choice).
        We assume/hope things didn't change to much in the meantime. An improvement
        would be to check if any columns have been added/removed or changed state,
        in which case we would clear the stored choices '''
        
        print("Setting default choices for combo boxes")
        
        for box in combo_boxes:
            box.blockSignals(True)
            previous_col_choice = self._get_default_col_choice_for_box(box)
            default_index = -1
            for index in range(0,box.count()):
                col = box.itemData(index)
                if col == previous_col_choice:
                    default_index = index
                    break
            if default_index != -1:
                box.setCurrentIndex(default_index)
            box.blockSignals(False)
        
        # make sure the selections are recorded
        self._update_current_selections()
            
    def _get_default_col_choice_for_box(self,box):
        box_name = self._get_boxname_for_box(box)
        if self.data_type is None:
            column = None
        else:
            column = self.model.get_data_location_choice(self.data_type, box_name)
        if column is None:
            return -1 # means no column chosen
        return column
            
    def get_data_locations(self):
        ''' Returns a dictionary mapping fields to combo_box_selections(columns) '''
        
        def selected_column(combo_box):
            item_data = combo_box.itemData(combo_box.currentIndex())
            selected_column = item_data.toInt()[0]
            if selected_column == -1:
                return None
            return selected_column
        
        current_selections = {}
        if self.raw_data:
            if self.data_type == MEANS_AND_STD_DEVS:
                if self.metric != GENERIC_EFFECT:
                    current_selections = {
                        'control_mean'            : selected_column(self.control_mean_combo_box),
                        'control_std_dev'         : selected_column(self.control_std_dev_combo_box),
                        'control_sample_size'     : selected_column(self.control_sample_size_combo_box),
                        'experimental_mean'       : selected_column(self.experimental_mean_combo_box),
                        'experimental_std_dev'    : selected_column(self.experimental_std_dev_combo_box),
                        'experimental_sample_size': selected_column(self.experimental_sample_size_combo_box),
                    }
                else: # metric is generic effect
                    current_selections = {}
            elif self.data_type == TWO_BY_TWO_CONTINGENCY_TABLE:
                current_selections = {
                    'control_response': selected_column(
                        self.control_response_combo_box),
                    'control_noresponse': selected_column(
                        self.control_noresponse_combo_box),
                    'experimental_response': selected_column(
                        self.experimental_response_combo_box),
                    'experimental_noresponse': selected_column(
                        self.experimental_noresponse_combo_box),
                }
            elif self.data_type == PROPORTIONS:
                current_selections = {
                    'num_events': selected_column(self.num_events_combobox),
                    'sample_size': selected_column(self.sample_size_combo_box),
                }
            elif self.data_type == CORRELATION_COEFFICIENTS:
                current_selections = {
                    'correlation': selected_column(self.correlation_combo_box),
                    'sample_size': selected_column(self.sample_size_combo_box),
                }
            
        if self.effect_size and self.effect_and_var_boxes_exist:
            current_selections['effect_size'] = selected_column(self.effect_size_combo_box)
            current_selections['variance']    = selected_column(self.variance_combo_box)
                
        
        return current_selections
    
    def _update_current_selections(self):
        #current_selections = self.get_data_locations()
        self.emit(SIGNAL("completeChanged()"))
            
    def isComplete(self):
        current_selections = self.get_data_locations()
        if current_selections is None:
            return False
        if set(current_selections.values()) == set([None]):
            return False # not complete if everything is None
        if self.need_full_raw_data:
            if None in current_selections.values():
                return False
        elif self.effect_size:
            if not self.effect_and_var_boxes_exist:
                return False
            if None in [current_selections['effect_size'], current_selections['variance']]:
                return False
        return True
    
    ################################
    
    def _get_data_location_string(self, data_location):
        ''' helper for summary '''
        
        get_column_name_for_key = lambda key: self.model.get_variable_assigned_to_column(data_location[key]).get_label()
        get_substr_for_key = lambda key: "  " + key.replace('_',' ') + ": " + get_column_name_for_key(key)
        
        sorted_keys = sorted(data_location.keys())
        lines = []
        for key in sorted_keys:
            if key in ['effect_size','variance']:
                continue
            if data_location[key] == None: # skip if no column assigned
                continue
            lines.append(get_substr_for_key(key))
        if 'effect_size' in sorted_keys:
            lines.append(get_substr_for_key('effect_size'))
        if 'variance' in sorted_keys:
            lines.append(get_substr_for_key('variance'))
            
        data_location_str = "\n".join(lines)
        return data_location_str
    
    def __str__(self):
        return "Data Location: \n%s" % self._get_data_location_string(self.get_data_locations())

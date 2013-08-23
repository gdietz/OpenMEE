import os

###### SWITCHES #######
# Enables additional elements of the program useful in debugging
DEBUG_MODE = True           # mostly for printing debugging message to terminal
SHOW_UNDO_VIEW = False
SHOW_PSEUDO_CONSOLE_IN_RESULTS_WINDOW = False
###### END SWITCHES ######

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

# The different types of data that can be associated with studies
CATEGORICAL, CONTINUOUS, COUNT = range(3)
VARIABLE_TYPES = (CATEGORICAL, CONTINUOUS, COUNT)

# Variables can have subtypes
(CALCULATED_RESULT,) = range(1)
VARIABLE_SUBTYPES = (CALCULATED_RESULT,)

# How variable types are represented as short string (for header labels)
VARIABLE_TYPE_SHORT_STRING_REPS = {CATEGORICAL:"cat",
                                   CONTINUOUS:"cont",
                                   COUNT:"count",}

# How variable types are represented as normal length strings
VARIABLE_TYPE_STRING_REPS = {CATEGORICAL:"Categorical",
                             CONTINUOUS:"Continuous",
                             COUNT:"Count",}

# Default # of digits for representing floating point numbers
DEFAULT_PRECISION = 4

# Default variable type
DEFAULT_VAR_TYPE = CATEGORICAL

DEFAULT_BACKGROUND_COLOR = QColor(29,30,25)
DEFAULT_LABEL_COLOR      = QColor(255,204,102)
DEFAULT_VARIABLE_COLORS = {CATEGORICAL: QColor(238,238,230),
                           COUNT:       QColor(242,38,111),
                           CONTINUOUS:  QColor(157,102,253)}
DEFAULT_VARIABLE_SUBTYPE_COLORS = {CALCULATED_RESULT: QColor(222,211,96)}


# Meta Analysis data type enumerations
(MEANS_AND_STD_DEVS,                  # continuous (OMA)
 TWO_BY_TWO_CONTINGENCY_TABLE,        # binary (OMA)
 CORRELATION_COEFFICIENTS) = range(3) # continuous(OMA)
 
# Datatype OMA convention strings
OMA_CONVENTION = {MEANS_AND_STD_DEVS:'continuous',
                  TWO_BY_TWO_CONTINGENCY_TABLE:'binary',
                  CORRELATION_COEFFICIENTS:'continuous'}

# For dealing with covariates in the interface to OpenMetaR
COVARIATE_TYPE_TO_OMA_STR_DICT = {CONTINUOUS:u"continuous",
                                  CATEGORICAL:u"factor",
                                  COUNT:u"continuous",
                                 }

# Data type names mapping data types ---> pretty names
DATA_TYPE_TEXT = {MEANS_AND_STD_DEVS:"Means and Stand. Devs",
                  TWO_BY_TWO_CONTINGENCY_TABLE:"2x2 Contingency Table", 
                  CORRELATION_COEFFICIENTS: "Correlation Coefficients",}

# Metric enumerations
(HEDGES_D, LN_RESPONSE_RATIO,
ODDS_RATIO, RATE_DIFFERENCE, RELATIVE_RATE,
FISHER_Z_TRANSFORM, GENERIC_EFFECT) = range(7)

# Mapping of metrics ---> pretty names
# fix for issue #21 -- adding generic effect
METRIC_TEXT = {HEDGES_D:"Hedges' d",
               LN_RESPONSE_RATIO:"ln Response Ratio",
               ODDS_RATIO:"Log Odds Ratio",
               RATE_DIFFERENCE:"Rate Difference",
               RELATIVE_RATE:"Log Relative Rate",
               FISHER_Z_TRANSFORM:"Fisher's Z-transform",
               GENERIC_EFFECT:"Generic Effect" 
               }

METRIC_TEXT_SHORT = {HEDGES_D:"d",
                     LN_RESPONSE_RATIO:"ln Resp.R",
                     ODDS_RATIO:"ln OR",
                     RATE_DIFFERENCE:"RD",
                     RELATIVE_RATE:"ln RR",
                     FISHER_Z_TRANSFORM:"Zr",
                     GENERIC_EFFECT:"Gen. Eff."
                     }

METRIC_TO_ESCALC_MEASURE = {HEDGES_D: "SMD",
                            LN_RESPONSE_RATIO: "ROM",
                            ODDS_RATIO:"OR",
                            RATE_DIFFERENCE:"RD",
                            RELATIVE_RATE:"RR",
                            FISHER_Z_TRANSFORM:"ZCOR",
                            GENERIC_EFFECT:"GEN", # not for escalc but for rma.uni (see metafor documentation)
                            }


# dictionary mapping data types to available metrics
DATA_TYPE_TO_METRICS = {MEANS_AND_STD_DEVS: [HEDGES_D, LN_RESPONSE_RATIO, GENERIC_EFFECT],
                        TWO_BY_TWO_CONTINGENCY_TABLE: [ODDS_RATIO, RATE_DIFFERENCE, RELATIVE_RATE],
                        CORRELATION_COEFFICIENTS: [FISHER_Z_TRANSFORM,],
                        }

EFFECT_SIZE_KEYS = ('yi','vi')

MAX_RECENT_FILES = 10
USER_PREFERENCES_FILENAME = "user_prefs.dict"
DEFAULT_FILENAME = "untited_dataset.ome"

PROGRAM_NAME = "OpenMEE"

BASE_PATH = str(os.path.abspath(os.getcwd()))

METHODS_WITH_NO_FOREST_PLOT = [] # leftover from OMA

DEFAULT_CONFIDENCE_LEVEL = 95

# this is the (local) path to a (pickled) dictionary containing
# user preferences
PREFS_PATH = "user_prefs.dict"

###################### CUSTOM EXCEPTIONS ##################################

class DuplicateItemError(Exception):
    def __init__(self, arg):
        self.args = arg
        
class CrazyRError(Exception):
    def __init__(self, msg, R_error=None):
        self.msg = msg
        self.R_error = R_error
    
    def __str__(self):
        return self.msg + ": " + str(self.R_error)
        
        

############################# Helper functions #############################

def table_as_str(table):
    ''' Returns a string formatted as a pretty table. 'table' is a list of
    tuples, one tuple per row '''
    
    if len(table) == 0:
        raise ValueError("Table cannot be empty")
    
    output_str = ""
    num_cols = len(table[0])
    row_fmt = "{:>15}"*num_cols
    row_fmt += "\n"
    for row in table:
        output_str += row_fmt.format(*row)
    return output_str

def do_nothing():
    'A very useful function indeed'
    pass

class GenericUndoCommand(QUndoCommand):
    ''' Generic undo command if the undo/redo is REALLY simple i.e. running
        redo/undo doesn't change the state for future executions
        
        on_entry and on_exit are functions that happen before and after the undo/redo
        '''
    
    def __init__(self, redo_fn, undo_fn,
                 on_undo_entry=do_nothing, on_undo_exit=do_nothing,
                 on_redo_entry=do_nothing, on_redo_exit=do_nothing,
                 description="GenericUndo"):
        super(GenericUndoCommand, self).__init__()
        
        self.redo_fn = redo_fn
        self.undo_fn = undo_fn
        
        # functions that occur on 
        self.on_undo_entry = on_undo_entry
        self.on_undo_exit = on_undo_exit
        self.on_redo_entry = on_redo_entry
        self.on_redo_exit = on_redo_exit
        
        
        self.setText(QString(description))
        
    def redo(self):
        self.on_redo_entry()
        self.redo_fn()
        self.on_redo_exit()
    
    def undo(self):
        self.on_undo_entry()
        self.undo_fn()
        self.on_undo_exit()
        
 
#http://www.riverbankcomputing.com/pipermail/pyqt/2009-November/025214.html
def unfill_layout(layout2clear):
    ''' Unfills a layout and any sub-layouts '''
    
    def deleteItems(layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    deleteItems(item.layout())
    deleteItems(layout2clear)
    


############### FOR DEALING WITH PLOT-MAKING ###############################
###
# the following methods are defined statically because
# they are also used by the forest plot editing window,
# which isn't really a 'child' of ma_specs, so inheritance
# didn't feel appropriate
###
def add_plot_params(specs_form):
    specs_form.current_param_vals["fp_show_col1"] = specs_form.show_1.isChecked()
    specs_form.current_param_vals["fp_col1_str"] = unicode(specs_form.col1_str_edit.text().toUtf8(), "utf-8")
    specs_form.current_param_vals["fp_show_col2"] = specs_form.show_2.isChecked()
    specs_form.current_param_vals["fp_col2_str"] = unicode(specs_form.col2_str_edit.text().toUtf8(), "utf-8")
    specs_form.current_param_vals["fp_show_col3"] = specs_form.show_3.isChecked()
    specs_form.current_param_vals["fp_col3_str"] = unicode(specs_form.col3_str_edit.text().toUtf8(), "utf-8")
    specs_form.current_param_vals["fp_show_col4"] = specs_form.show_4.isChecked()
    specs_form.current_param_vals["fp_col4_str"] = unicode(specs_form.col4_str_edit.text().toUtf8(), "utf-8")
    specs_form.current_param_vals["fp_xlabel"] = unicode(specs_form.x_lbl_le.text().toUtf8(), "utf-8")
    specs_form.current_param_vals["fp_outpath"] = unicode(specs_form.image_path.text().toUtf8(), "utf-8")
    
    plot_lb = unicode(specs_form.plot_lb_le.text().toUtf8(), "utf-8")
    specs_form.current_param_vals["fp_plot_lb"] = "[default]"
    if plot_lb != "[default]" and check_plot_bound(plot_lb):
        specs_form.current_param_vals["fp_plot_lb"] = plot_lb

    plot_ub = unicode(specs_form.plot_ub_le.text().toUtf8(), "utf-8")
    specs_form.current_param_vals["fp_plot_ub"] = "[default]"
    if plot_ub != "[default]" and check_plot_bound(plot_ub):
        specs_form.current_param_vals["fp_plot_ub"] = plot_ub

    xticks = unicode(specs_form.x_ticks_le.text().toUtf8(), "utf-8")
    specs_form.current_param_vals["fp_xticks"] = "[default]"
    if xticks != "[default]" and seems_sane(xticks):
        specs_form.current_param_vals["fp_xticks"] = xticks
    
    specs_form.current_param_vals["fp_show_summary_line"] = specs_form.show_summary_line.isChecked()
    
def check_plot_bound(bound):
    try:
        # errrm... this might cause a problem if 
        # bound is 0... 
        return float(bound) 
    except:
        return False
    
def seems_sane(xticks):
    num_list = xticks.split(",")
    if len(num_list) == 1:
        return False
    try:
        num_list = [eval(x) for x in num_list]
    except:
        return False
    return True
    
################### END OF PLOT HELPER FUNCTIONS ################################


# COPY & PASTE
# normalizing new lines, e.g., for pasting
# use QRegExp to manipulate QStrings (rather than re)
newlines_re  = QRegExp('(\r\n|\r|\r)')
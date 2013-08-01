# Enables additional elements of the program useful in debugging
DEBUG_MODE = True

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

# The different types of data that can be associated with studies
CATEGORICAL, CONTINUOUS, COUNT = range(3)
VARIABLE_TYPES = (CATEGORICAL, CONTINUOUS, COUNT)

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


# Meta Analysis data type enumerations
(MEANS_AND_STD_DEVS,                  # continuous (OMA)
 TWO_BY_TWO_CONTINGENCY_TABLE,        # binary (OMA)
 CORRELATION_COEFFICIENTS) = range(3) # continuous(OMA)

# Data type names mapping data types ---> pretty names
DATA_TYPE_TEXT = {MEANS_AND_STD_DEVS:"Means and Stand. Devs",
                  TWO_BY_TWO_CONTINGENCY_TABLE:"2x2 Contingency Table", 
                  CORRELATION_COEFFICIENTS: "Correlation Coefficients",}

# Metric enumerations
(HEDGES_D, LN_RESPONSE_RATIO,
ODDS_RATIO, RATE_DIFFERENCE, RELATIVE_RATE,
FISHER_Z_TRANSFORM) = range(6)

# Mapping of metrics ---> pretty names
METRIC_TEXT = {HEDGES_D:"Hedges' d",
               LN_RESPONSE_RATIO:"ln Response Ratio",
               ODDS_RATIO:"Log Odds Ratio",
               RATE_DIFFERENCE:"Rate Difference",
               RELATIVE_RATE:"Log Relative Rate",
               FISHER_Z_TRANSFORM:"Fisher's Z-transform",
               }
METRIC_TEXT_SHORT = {HEDGES_D:"d",
                     LN_RESPONSE_RATIO:"ln Resp.R",
                     ODDS_RATIO:"ln OR",
                     RATE_DIFFERENCE:"RD",
                     RELATIVE_RATE:"ln RR",
                     FISHER_Z_TRANSFORM:"Zr",
                     }
METRIC_TO_ESCALC_MEASURE = {HEDGES_D: "SMD",
                            #LN_RESPONSE_RATIO: None, # ln RR not in escalc
                            ODDS_RATIO:"OR",
                            RATE_DIFFERENCE:"RD",
                            RELATIVE_RATE:"RR",
                            FISHER_Z_TRANSFORM:"ZCOR",
                            }


# dictionary mapping data types to available metrics
DATA_TYPE_TO_METRICS = {MEANS_AND_STD_DEVS: [HEDGES_D, LN_RESPONSE_RATIO],
                        TWO_BY_TWO_CONTINGENCY_TABLE: [ODDS_RATIO, RATE_DIFFERENCE, RELATIVE_RATE],
                        CORRELATION_COEFFICIENTS: [FISHER_Z_TRANSFORM,],
                        }

EFFECT_SIZE_KEYS = ('yi','vi')

MAX_RECENT_FILES = 10
USER_PREFERENCES_FILENAME = "user_prefs.dict"
DEFAULT_FILENAME = "untited_dataset.ome"

PROGRAM_NAME = "OpenMEE"

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
    
################ Useful Node class ###########################################

#class Node:
#    def __init__(self, aText=None, aParent=None):
#        self.aText=aText
#        self.aParent=aParent
#        self.children = [] # List of nodes as children
#        
#    def data(self):
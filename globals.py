
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

# The different types of data that can be associated with studies
CATEGORICAL, CONTINUOUS, INTEGER = range(3)
VARIABLE_TYPES = (CATEGORICAL, CONTINUOUS, INTEGER)

# How variable types are represented as short string (for header labels)
VARIABLE_TYPE_SHORT_STRING_REPS = {CATEGORICAL:"cat",
                                   CONTINUOUS:"cont",
                                   INTEGER:"int",}

# How variable types are represented as normal length strings
VARIABLE_TYPE_STRING_REPS = {CATEGORICAL:"Categorical",
                             CONTINUOUS:"Continuous",
                             INTEGER:"Integer",}

# Default # of digits for representing floating point numbers
DEFAULT_PRECISION = 4

# Default variable type
DEFAULT_VAR_TYPE = CATEGORICAL

###################### CUSTOM EXCEPTIONS ##################################

class DuplicateItemError(Exception):
    def __init__(self, arg):
        self.args = arg

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
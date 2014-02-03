################
#              #
# George Dietz #
# CEBM@Brown   #
#              #
################

import os
import cProfile

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

###### SWITCHES #######
# Enables additional elements of the program useful in debugging
DEBUG_MODE = True           # mostly for printing debugging message to terminal
SHOW_UNDO_VIEW = False
SHOW_PSEUDO_CONSOLE_IN_RESULTS_WINDOW = False
SOUND_EFFECTS = True
MAKE_TESTS = False
###### END SWITCHES ######

HEADER_LINE_LENGTH = 70 # maximum length of header labels 

DEFAULT_METAREG_RANDOM_EFFECTS_METHOD = "DL"
RANDOM_EFFECTS_METHODS_TO_PRETTY_STRS = {"DL":"DerSimonian-Laird estimator",
                                         "HE":"Hedges estimator",
                                         "SJ":"Sidik-Jonkman estimator",
                                         "ML":"maximum-likelihood estimator",
                                         "REML":"restricted maximum likelihood estimator",
                                         "EB":"empirical Bayes estimator",
                                         "HS":"Hunter-Schmidt estimator",
                                         }


# The different types of data that can be associated with studies
CATEGORICAL, CONTINUOUS, COUNT = range(3)
VARIABLE_TYPES = (CATEGORICAL, CONTINUOUS, COUNT)

MAX_CELL_PASTE_UNDOABLE = 1000

# Variables can have subtypes
(TRANS_EFFECT, TRANS_VAR,
 RAW_EFFECT, RAW_LOWER, RAW_UPPER) = range(5)
VARIABLE_SUBTYPES = (TRANS_EFFECT, TRANS_VAR,
                     RAW_EFFECT,RAW_LOWER, RAW_UPPER)
EFFECT_TYPES = (TRANS_EFFECT, TRANS_VAR,
                RAW_EFFECT,RAW_LOWER, RAW_UPPER)

# How variable types are represented as short string (for header labels)
VARIABLE_TYPE_SHORT_STRING_REPS = {CATEGORICAL:"cat",
                                   CONTINUOUS:"cont",
                                   COUNT:"count",}

# How variable types are represented as normal length strings
VARIABLE_TYPE_STRING_REPS = {CATEGORICAL:"Categorical",
                             CONTINUOUS:"Continuous",
                             COUNT:"Count",}
# How variable subtypes are represented as normal length strings
VARIABLE_SUBTYPE_STRING_REPS = {TRANS_EFFECT: "Trans. Effect",
                                TRANS_VAR   : "Trans. Var",
                                RAW_EFFECT  : "Raw Effect",
                                RAW_LOWER   : "Raw lb.", 
                                RAW_UPPER   : "Raw ub.",
                                }

# Default # of digits for representing floating point numbers
DEFAULT_PRECISION = 3

# Enumerations for calculating effect size and/or back-transform
TRANS_TO_RAW, RAW_TO_TRANS = range(2) #
RAW_SCALE, TRANSFORMED_SCALE = range(2)

def verify_transform_direction(direction):
    if direction not in [TRANS_TO_RAW, RAW_TO_TRANS]:
        raise Exception("Unrecognized Transform Direction")
    
def cancel_macro_creation_and_revert_state(undo_stack):
    ''' Ends creation of macro (in progress) and reverts the state of
    the model to before the macro began to be created '''
    
    #print("Cancelling macro creation and reverting")
    undo_stack.endMacro()
    undo_stack.undo()

# Wizard 'modes'
(CALCULATE_EFFECT_SIZE_MODE, MA_MODE, CUM_MODE, SUBGROUP_MODE, LOO_MODE,
 META_REG_MODE, TRANSFORM_MODE, META_REG_COND_MEANS,
 BOOTSTRAP_MA, BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS,
 FAILSAFE_MODE, FUNNEL_MODE) = range(13)
 
PARAMETRIC, BOOTSTRAP = range(2)     # analysis type
NORMAL, CONDITIONAL_MEANS = range(2) # output type
 
MODE_TITLES = {CALCULATE_EFFECT_SIZE_MODE: "Calculate Effect Size",
               MA_MODE: "Meta Analysis",
               CUM_MODE: "Cumulative Meta Analysis",
               SUBGROUP_MODE: "Subgroup Meta Analysis",
               LOO_MODE: "Leave-One-Out Meta Analysis",
               META_REG_MODE: "Meta Regression",
               TRANSFORM_MODE: "Transform Effect Size",
               META_REG_COND_MEANS: "Meta Regression-Based Conditional Means",
               BOOTSTRAP_MA: "Bootstrapped Meta-Analysis",
               BOOTSTRAP_META_REG: "Bootstrapped Meta-Regression",
               BOOTSTRAP_META_REG_COND_MEANS:"Bootstrapped Meta-Regression based Conditional Means",
               FAILSAFE_MODE:"Fail-Safe N",
               FUNNEL_MODE: "Funnel Plot"}

# For choosing statistic function for bootstrapping
BOOTSTRAP_MODES_TO_STRING = {BOOTSTRAP_MA:'boot.ma',
                             BOOTSTRAP_META_REG: 'boot.meta.reg',
                             BOOTSTRAP_META_REG_COND_MEANS: 'boot.meta.reg.cond.means'}
 
ANALYSIS_MODES = [MA_MODE, CUM_MODE, SUBGROUP_MODE, LOO_MODE,
                  META_REG_MODE, META_REG_COND_MEANS,
                  BOOTSTRAP_MA, BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS,
                  FAILSAFE_MODE, FUNNEL_MODE]

META_ANALYSIS_MODES = [MA_MODE, CUM_MODE, SUBGROUP_MODE, LOO_MODE, BOOTSTRAP_MA, FUNNEL_MODE]
META_REG_MODES      = [META_REG_MODE, META_REG_COND_MEANS, BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS]

# Default variable type
DEFAULT_VAR_TYPE = CATEGORICAL

DEFAULT_BACKGROUND_COLOR = QColor("white") #QColor(29,30,25)
FOREGROUND, BACKGROUND = range(2)
DEFAULT_COLOR_SCHEME = {'DEFAULT_BACKGROUND_COLOR': QColor("white"),
                        'label': {FOREGROUND: QColor(255,204,102),
                                  BACKGROUND: DEFAULT_BACKGROUND_COLOR},
                        'variable' : {
                                      CATEGORICAL:
                                            {FOREGROUND: QColor(0,0,0),
                                             BACKGROUND: DEFAULT_BACKGROUND_COLOR},
                                      COUNT:
                                            {FOREGROUND: QColor(242,38,111),
                                             BACKGROUND: DEFAULT_BACKGROUND_COLOR},
                                      CONTINUOUS:
                                            {FOREGROUND: QColor(157,102,253),
                                             BACKGROUND: DEFAULT_BACKGROUND_COLOR},
                                      },
                        'variable_subtype' : {
                                              'DEFAULT_EFFECT':
                                                    {FOREGROUND: QColor(0,0,0),
                                                     BACKGROUND: QColor(222,211,96)},
                                              },
                        }


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

# transformed (usually log) scale
METRIC_TEXT_SHORT = {HEDGES_D:"d",
                     LN_RESPONSE_RATIO:"ln Resp.R",
                     ODDS_RATIO:"ln OR",
                     RATE_DIFFERENCE:"RD",
                     RELATIVE_RATE:"ln RR",
                     FISHER_Z_TRANSFORM:"Zr",
                     GENERIC_EFFECT:"Gen. Eff."
                     }
# raw scale
METRIC_TEXT_SHORT_RAW_SCALE = {
                     HEDGES_D:"d",
                     LN_RESPONSE_RATIO:"Resp.R",
                     ODDS_RATIO:"OR",
                     RATE_DIFFERENCE:"RD",
                     RELATIVE_RATE:"RR",
                     FISHER_Z_TRANSFORM:"Rz",
                     GENERIC_EFFECT:"Gen. Eff."
                     }

# Text to describe metrics without regard to being transformed or not
METRIC_TEXT_SIMPLE = {HEDGES_D:"Hedges' d",
                      LN_RESPONSE_RATIO:"Response Ratio",
                      ODDS_RATIO:"Odds Ratio",
                      RATE_DIFFERENCE:"Rate Difference",
                      RELATIVE_RATE:"Relative Rate",
                      FISHER_Z_TRANSFORM:"Fisher's Z-transform",
                      GENERIC_EFFECT:"Generic Effect" 
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
def get_data_type_for_metric(metric):
    for d_type, metrics in DATA_TYPE_TO_METRICS.items():
        if metric in metrics:
            return d_type
    raise Exception("Metric matches no known data type")

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

def tabulate(lists, sep=" | ", return_col_widths=False, align=[]):
    ''' Makes a pretty table from the lists in args'''
    ''' each arg is a list '''
    ''' if return_max_col_lenths is true, the return type is a tuple of (str, col_widths) '''
    ''' align is a list the same length as lists telling how the column should be aligned ('L','R') etc '''
    
    if len(align) != len(lists):
        align = ['L',]*len(lists) 
    print("Align is now %s: " % align)
    
    # covert lists in args to string lists
    string_lists = []
    for arg in lists:
        str_arg = [str(x) for x in arg]
        string_lists.append(str_arg)
    
    # get max length of each element in each column
    max_lengths = []
    for arg in string_lists:
        max_len = max([len(x) for x in arg])
        max_lengths.append(max_len)
        
    data = zip(*string_lists)
    out = []
    for row in data:
        row_str = ["{0:{align}{width}}".format(x, width=width,align='<' if row_alignment=='L' else '>') for x,width,row_alignment in zip(row,max_lengths,align)]
        row_str = sep.join(row_str)
        out.append(row_str)
    out_str =  "\n".join(out)
    
    if return_col_widths:
        return (out_str, max_lengths)
    return out_str


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

def profile_this(function):
    def _profile_this(*args, **kw):
        # Profiling Decorator
        pr=cProfile.Profile()
        pr.enable()
        result = function(*args, **kw)
        pr.disable()
        pr.create_stats()
        pr.print_stats(sort='cumulative')
        
        return result
    return _profile_this

# sort-of R-style switch function
# Takes a value to switch on and a bunch of keyword arguments whose values are functions to evaluate
def switch(value, *args, **kw):
    for key,fn in kw.iteriterms():
        if key == value:
            return fn()
    raise Exception("No targets matched for switch")


def are_valid_numbers(num_list):
    for x in num_list:
        try:
            float(x)
        except:
            return False
    return True

def listvals_to_scalars(d):
    ''' converts values of d which are lists to scalars if length is 1 '''
    for k,v in d.iteritems():
        if not isinstance(v, list):
            continue
        if len(v) == 1:
            d[k]=v[0]
    return d

        #print("inspecting r object time")
        #pyqtRemoveInputHook()
        #import pdb; pdb.set_trace()
        
# Sound effects
moment = QSound("sounds/moment.wav")
silly = QSound("sounds/silly.wav")

def manual_word_wrap(x, max_length=HEADER_LINE_LENGTH, sep=' '):
    ''' Returns a wrapped version of x
    max_length is maximum length of the line, sep is the separator to break
    the string with, x is the input string'''
    
    lines = []
    words = str(x).split(sep)
    line = ""
    for word in words:
        if len(line) + len(word) + 1 > max_length:
            lines.append(line)
            line = word
        else:
            line = sep.join([line, word])
    if len(line)>0:
        lines.append(line)
    return '\n'.join(lines)

def boxify(astr, border="#", margin=1):
    ''' Prints the string in a pretty box
    e.g. >> print(boxify("hello"))
         #########
         #       #
         # hello #
         #       #
         ######### '''
    
    if len(border) > 1:
        raise ValueError("border must be one character long")
    
    lstr = astr.split("\n")
    width = max([len(x) for x in lstr])
    lstr_padded = ['{:<{width}}'.format(x, width=width) for x in lstr]
    lstr_content = [border + " "*margin + x + " "*margin + border for x in lstr_padded]
    # add on top and bottom bits
    borderbar_len = width + 2*margin + 2*len(border)
    borderbar = border*borderbar_len
    margin_bar = border + " "*margin + " "*width + " "*margin + border
    top = [borderbar,] + [margin_bar,]*margin
    bottom = [margin_bar,]*margin + [borderbar,]
    all_together_now = top+lstr_content+bottom
    return "\n".join(all_together_now)

def civilized_dict_str(a_dict):
    # prints out a dictionary in a 'civilized' manner e.g.:
    #    {
    #     goodbye: '5'
    #     hello: '4'
    #    }
    content = []
    for k in sorted(a_dict.keys()):
        content.append(" %s: '%s'" % (k, a_dict[k]))
    
    return "{\n%s\n}" % "\n".join(content)

################### Helpers for wizards ########################################    

def wizard_summary(wizard, next_id_helper, summary_page_id, analysis_label):
    # Goes through all the pages that were visited (except summary page)
    # and collects their sub summary info (via str())
    # analysis_label is something like "Meta Regression" e.g.
    
    analysis_label_str = "Analysis: %s\n" % analysis_label
    visited_page_ids = wizard.visitedPages()
    # Remove summary page id
    try:
        visited_page_ids.remove(summary_page_id)
    except ValueError:
        pass
    
    page_strs = (str(wizard.page(id)) for id in visited_page_ids)
    page_strs = filter(lambda x: x!="", page_strs)
    summary_text = "\n\n".join(page_strs)
    summary_text = analysis_label_str + summary_text
    return summary_text
    
    
###############################################################################

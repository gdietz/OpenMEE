
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
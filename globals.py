
# The different types of data that can be associated with studies
CATEGORICAL, CONTINUOUS, INTEGER = range(3)
VARIABLE_TYPES = [CATEGORICAL, CONTINUOUS, INTEGER]

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



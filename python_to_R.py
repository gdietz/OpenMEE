from globals import *
from rpy2 import robjects as ro

#################### R Library Loader ####################
class RlibLoader:
    def __init__(self):
        print("R Libary loader (RlibLoader) initialized...")
    def load_metafor(self):
        return self._load_r_lib("metafor")
#    def load_openmetar(self):
#        return self._load_r_lib("openmetar")
    def _load_r_lib(self, name):
        try:
            ro.r("library(%s)" % name)
            msg = "%s package successfully loaded" % name
            print(msg)
            return (True, msg)
        except:
            raise Exception("The %s R package is not installed.\nPlease \
install this package and then re-start OpenMeta." % name)
#################### END OF R Library Loader ####################


def gather_data(model, data_location):
    ''' Gathers the relevant data in one convenient location for the purpose
    of sending to R '''
    
    # list of studies as currently shown on the spreadsheet
    studies = model.get_studies_in_current_order()
    
    data = {}
    for k, col in data_location.items():
        var = model.get_variable_assigned_to_column(col)
        data[k] = [study.get_var(var) for study in studies]
        
    data['study_labels'] = [study.get_label() for study in studies]
    
    return data

def None_to_NA(value, value_type):
    ''' Convert None value to an R NA object of the appropriate type.
        Returns the value unchanged if it is not none'''
    
    if value is not None:
        return value

    value_type_to_NA = {str:ro.NA_Character,
                        int:ro.NA_Integer,
                        bool:ro.NA_Logical,
                        float:ro.NA_Real,
                        complex:ro.NA_Complex,
                        }
    return value_type_to_NA[value_type]

def NA_to_None(value):
    ''' Converts R NA values to None, return value unchanged if not an NA type'''
    
    NA_types = [type(ro.NA_Character),
                type(ro.NA_Integer),
                type(ro.NA_Logical),
                type(ro.NA_Real),
                type(ro.NA_Complex)]
    NA_types = [type(ro.NA_Character), type(ro.NA_Integer), type(ro.NA_Logical), type(ro.NA_Real), type(ro.NA_Complex)]
    
    if type(value) in NA_types:
        return None
    return value

def effect_size(metric, data_type, data):
    ''' calculates effect sizes for the data given in the data where data
    is a dictionary of values obtained from columns as specified in the
    calculate effect size dialog '''
    
    measure = METRIC_TO_ESCALC_MEASURE[metric]
    
    if data_type == MEANS_AND_STD_DEVS:
        m1i  = data['experimental_mean']
        sd1i = data['experimental_std_dev']
        n1i  = data['experimental_sample_size']
        m2i  = data['control_mean']
        sd2i = data['control_std_dev']
        n2i  = data['control_sample_size']
        
        # convert None entries to R-type NAs
        m1i  = [None_to_NA(x, float) for x in m1i]
        sd1i = [None_to_NA(x, float) for x in sd1i]
        n1i  = [None_to_NA(x, int) for x in n1i]
        m2i  = [None_to_NA(x, float) for x in m1i]
        sd2i = [None_to_NA(x, float) for x in sd2i]
        n2i  = [None_to_NA(x, int) for x in n2i]
        
        # convert to R objects
        m1i  = ro.FloatVector(m1i)
        sd1i = ro.FloatVector(sd1i)
        n1i  = ro.IntVector(n1i)
        m2i  = ro.FloatVector(m2i)
        sd2i = ro.FloatVector(sd2i)
        n2i  = ro.IntVector(n2i)
        
        args = (measure, m1i.r_repr(), sd1i.r_repr(), n1i.r_repr(),
                         m2i.r_repr(), sd2i.r_repr(), n2i.r_repr())
        r_str = "escalc(measure='%s', m1i=%s, sd1i=%s, n1i=%s, m2i=%s, sd2i=%s, n2i=%s)" % args
        
    elif data_type == TWO_BY_TWO_CONTINGENCY_TABLE:
        ai = data['experimental_response']
        bi = data['experimental_noresponse']
        ci = data['control_response']
        di = data['control_noresponse']
        
        # convert None entries to R-type NAs
        ai = [None_to_NA(x, int) for x in ai]
        bi = [None_to_NA(x, int) for x in bi]
        ci = [None_to_NA(x, int) for x in ci]
        di = [None_to_NA(x, int) for x in di]
        
        # convert to R objects
        ai = ro.IntVector(ai)
        bi = ro.IntVector(bi)
        ci = ro.IntVector(ci)
        di = ro.IntVector(di)
        
        args = (measure, ai.r_repr(), bi.r_repr(), ci.r_repr(), di.r_repr())
        r_str = "escalc(measure='%s', ai=%s, bi=%s, ci=%s, di=%s)" % args
        
    elif data_type == CORRELATION_COEFFICIENTS:
        ri = data['correlation']
        ni = data['sample_size']
        
        # convert None entries to R-type NAs
        ri = [None_to_NA(x, float) for x in ri]
        ni = [None_to_NA(x, int)   for x in ni]
        
        # convert to R objects
        ri = ro.FloatVector(ri)
        ni = ro.IntVector(ni)
        
        args = (measure, ri.r_repr(), ni.r_repr())
        r_str = "escalc(measure='%s', ri=%s, ni=%s)" % args
    else:
        raise Exception("Data type not recognized")
    
    print("Executing in R: r_str")
    
    
    escalc_result = try_n_run(lambda: ro.r(r_str))
    
    result = dataframe_to_pydict(escalc_result) #yi, vi
    return result

def try_n_run(fn):
    ''' tries to run a function (a call to R) and raises and error if it fails'''
    
    try:
        return fn()
    except Exception as e:
        raise CrazyRError("Some crazy R error occurred", e)
    
    

def dataframe_to_pydict(dataframe):
    ''' assumes the columns are named '''
    
    keys = ro.r("names(%s)" % dataframe.r_repr())
    keys = tuple(keys)
    
    key_value_pairs = [(key, list(dataframe.rx2(key))) for key in keys]
    pydict = dict(key_value_pairs)
    
    # remove NAs (change to Nones)
    for k, v in pydict.items():
        v = [NA_to_None(x) for x in v]
        pydict[k] = v
    
    return pydict
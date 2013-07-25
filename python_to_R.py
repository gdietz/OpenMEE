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


def gather_data(self, model, data_location):
    ''' Gathers the relevant data in one convenient location for the purpose
    of sending to R '''
    
    # list of studies as currently shown on the spreadsheet
    studies = model.get_studies_in_current_order()
    
    data = {}
    for k, col in data_location:
        var = model.get_variable_assigned_to_column(col)
        data[k] = [study.get_var(var) for study in studies]
        
    data['study_labels'] = [study.get_label() for study in studies]
    
    return data

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
    elif data_type == TWO_BY_TWO_CONTINGENCY_TABLE:
        ai = data['experimental_response']
        bi = data['experimental_noresponse']
        ci = data['control_response']
        di = data['control_noresponse']
    elif data_type == CORRELATION_COEFFICIENTS:
        ri = data['correlation']
        ni = data['sample_size']
    else:
        raise Exception("Data type not recognized")
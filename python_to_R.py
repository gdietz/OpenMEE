import math



from globals import *

import rpy2
import rpy2.robjects
from rpy2 import robjects as ro


#################### R Library Loader ####################
class RlibLoader:
    def __init__(self):
        print("R Libary loader (RlibLoader) initialized...")
        
    def load_metafor(self):
        return self._load_r_lib("metafor")
    
    def load_openmetar(self):
        return self._load_r_lib("openmetar")
    
    def load_igraph(self):
        return self._load_r_lib("igraph")
    
    def load_grid(self):
        return self._load_r_lib("grid")
    
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

try:
    if not ro.r("file.exists('./.r_tmp')")[0]:
        print("creating tmp R directory...")
        ro.r("dir.create('./r_tmp')")
        print("success -- temporary results will be written to ./r_tmp")
except:
    raise Exception, "unable to create temporary directory for R results! make sure you have sufficient permissions."

def reset_Rs_working_dir():
    print("resetting R working dir")

    # Fix paths issue in windows
    r_str = "setwd('%s')" % BASE_PATH
    print("before replacement r_string: %s" % r_str)
    r_str = r_str.replace("\\","\\\\")
    print("about to execute: %s" % r_str)

    # Executing r call with escaped backslashes
    ro.r(r_str)
    
def set_conf_level_in_R(conf_lev):
    
    invalid_conf_lev_msg = "Confidence level needs to be a number between 0 and 100"
    if conf_lev is None:
        raise ValueError(invalid_conf_lev_msg)
    elif not (0 < conf_lev < 100):
        raise ValueError(invalid_conf_lev_msg)


    r_str = "set.global.conf.level("+str(float(conf_lev))+")"
    new_cl_in_R = ro.r(r_str)[0]
    print("Set confidence level in R to: %f" % new_cl_in_R)
    
    return conf_lev

def generate_forest_plot(file_path, side_by_side=False, params_name="plot.data"):
    if side_by_side:
        print "generating a side-by-side forest plot..."
        ro.r("two.forest.plots(%s, '%s')" % (params_name, file_path))
    else:
        print("generating a forest plot....")
        ro.r("forest.plot(%s, '%s')" % (params_name, file_path))
        
def evaluate_in_r(r_str):
    res = ro.r(r_str)
    return str(res)

def load_in_R(fpath):
    ''' loads what is presumed to be .Rdata into the R environment '''
    ro.r("load('%s')" % fpath)
    
def generate_reg_plot(file_path, params_name="plot.data"): 
    ro.r("meta.regression.plot(%s, '%s')" % (params_name, file_path))

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

def studies_have_raw_data(studies, data_type, data_location, model, first_arm_only=False):
    ''' True iff all the studies in 'studies' have 'raw' data for the currently
    selected outcome. If the metric is one-arm, we only check the raw data corresponding to that arm'''
    
    if data_type == MEANS_AND_STD_DEVS:
        columns_to_check = [data_location['experimental_mean'],
                            data_location['experimental_std_dev'],
                            data_location['experimental_sample_size'],]
        if not first_arm_only: # add additional columns to check
            columns_to_check.extend([data_location['control_mean'],
                                     data_location['control_std_dev'],
                                     data_location['control_sample_size'],])
        
    elif data_type == TWO_BY_TWO_CONTINGENCY_TABLE:
        columns_to_check = [data_location['experimental_response'],
                            data_location['experimental_noresponse'],]
        if not first_arm_only:
            columns_to_check.extend([data_location['control_response'],
                                     data_location['control_noresponse'],
                                     ])

    elif data_type == CORRELATION_COEFFICIENTS:
        columns_to_check = [data_location['correlation'],
                            data_location['sample_size'],]
    else:
        raise Exception("Unrecognized data type")
    
    if None in columns_to_check:
        return False
    
    variables_to_check = [model.get_variable_assigned_to_column(col) for col in columns_to_check]
    for var in variables_to_check:
        values = [study.get_var(var) for study in studies]
        if None in values:
            return False
        
    return True # didn't return false from for loop

def studies_have_point_estimates(studies, data_location, model):
    columns_to_check = [data_location['effect_size'], data_location['variance']]
    variables_to_check = [model.get_variable_assigned_to_column(col) for col in columns_to_check]
    for var in variables_to_check:
        values = [study.get_var(var) for study in studies]
        if None in values:
            return False
    return True # didn't return false from for loop
    

def dataset_to_simple_binary_robj(model, included_studies, data_location, var_name="tmp_obj", 
                                  include_raw_data=True, covs_to_include=[], one_arm=False
                                  ):
    '''
    This converts an EETableModel to an OpenMetaData (OMData) R object. We use type EETableModel
    rather than a Dataset model directly to access the current variables.
    
    By 'simple' we mean that this method returns a single outcome single follow-up (defined as the
    the currently selected, as indicated by the model object) data object.

     @TODO
        - implement methods for more advanced conversions, i.e., for multiple outcome
            datasets (althought this will be implemented in some other method)
    '''
    r_str = None
    
    ####study_ids = [study.get_id() for study in included_studies]

    # issue #139 -- also grab the years
    none_to_str = lambda n : str(n) if n is not None else "" # this will produce NA ints
    #study_years = ", ".join(["as.integer(%s)" % none_to_str(study.year) for study in studies])
    study_years = ", ".join(["as.integer(%s)" % none_to_str(None) for study in included_studies])
    study_names = ", ".join(["'" + study.get_label(none_to_empty_string=True) + "'" for study in included_studies])
    
    ests_variable = model.get_variable_assigned_to_column(data_location['effect_size'])
    variance_variable = model.get_variable_assigned_to_column(data_location['variance'])
    
    ests = [study.get_var(ests_variable) for study in included_studies]
    SEs =  [math.sqrt(study.get_var(variance_variable)) for study in included_studies]
    
    ests_str = ", ".join(_to_strs(ests))
    SEs_str = ", ".join(_to_strs(SEs))

    # TODO: add this covariate handling back in 
    # generate the covariate string
    #cov_str = "list()"
    cov_str = list_of_cov_value_objects_str(studies=included_studies, cov_list=covs_to_include)
    

    # first try and construct an object with raw data
    if include_raw_data and studies_have_raw_data(studies=included_studies,
                                                  data_type=TWO_BY_TWO_CONTINGENCY_TABLE,
                                                  data_location=data_location,
                                                  model=model,
                                                  first_arm_only=one_arm):
        print "ok; raw data has been entered for all included studies"
        
        # now figure out the raw data
        g1_events_col = data_location['experimental_response']
        g1_events_var = model.get_variable_assigned_to_column(g1_events_col)
        g1_events = [study.get_var(g1_events_var) for study in included_studies]
        
        g1_no_events_col = data_location['experimental_noresponse']
        g1_no_events_var = model.get_variable_assigned_to_column(g1_no_events_col)
        g1_no_events = [study.get_var(g1_no_events_var) for study in included_studies]
        
        g1O1_str = ", ".join(_to_strs(g1_events))
        g1O2_str = ", ".join(_to_strs(g1_no_events))
    
        # now, for group 2; we only set up the string
        # for group two if we have a two-arm metric
        g2O1_str, g2O2_str = "0", "0" # the 0s are just to satisfy R; not used
        if not one_arm:
            g2_events_col    = data_location['control_response']
            g2_no_events_col = data_location['control_noresponse']
            g2_events_var = model.get_variable_assigned_to_column(g2_events_col)
            g2_no_events_var = model.get_variable_assigned_to_column(g2_no_events_col)
            
            g2_events = [study.get_var(g2_events_var) for study in included_studies]
            g2_no_events = [study.get_var(g2_no_events_var) for study in included_studies]
            
            g2O1_str = ", ".join(_to_strs(g2_events))
            g2O2_str = ", ".join(_to_strs(g2_no_events))
                    
        # actually creating a new object on the R side seems the path of least resistance here.
        # the alternative would be to try and create a representation of the R object on the 
        # python side, but this would require more work and I'm not sure what the benefits
        # would be
        r_str = "%s <- new('BinaryData', g1O1=c(%s), g1O2=c(%s), g2O1=c(%s), g2O2=c(%s), \
                            y=c(%s), SE=c(%s), study.names=c(%s), years=c(%s), covariates=%s)" % \
                            (var_name, g1O1_str, g1O2_str, g2O1_str, g2O2_str, \
                             ests_str, SEs_str, study_names, study_years, cov_str)

    elif studies_have_point_estimates(studies=included_studies, data_location=data_location, model=model):
        print "not sufficient raw data, but studies have point estimates..."

        r_str = "%s <- new('BinaryData', y=c(%s), SE=c(%s), study.names=c(%s), years=c(%s), covariates=%s)" \
                            % (var_name, ests_str, SEs_str, study_names, study_years, cov_str)
        
               
    else:
        print "there is neither sufficient raw data nor entered effects/CIs. I cannot run an analysis."
        # @TODO complain to the user here
    

    ### Relevant for Issue #73
    # ok, it seems R uses latin-1 for its unicode encodings,
    # whereas QT uses UTF8. this can cause situations where
    # rpy2 throws up on this call due to it not being able
    # to parse a character; so we sanitize. This isn't great,
    # because sometimes characters get garbled...
    r_str = _sanitize_for_R(r_str)
    print "executing: %s" % r_str
    ro.r(r_str)
    print "ok."
    return r_str


def dataset_to_simple_continuous_robj(model, included_studies, data_location,
                                      data_type, 
                                      var_name="tmp_obj",
                                      covs_to_include=[], one_arm=False):
    r_str = None
    
    ###study_ids = [study.get_id() for study in included_studies]
    
    study_names = ", ".join(["'" + study.get_label(none_to_empty_string=True) + "'" for study in included_studies])
    none_to_str = lambda n : str(n) if n is not None else "" # this will produce NA ints
    study_years = ", ".join(["as.integer(%s)" % none_to_str(None) for study in included_studies])
    
    ests_variable = model.get_variable_assigned_to_column(data_location['effect_size'])
    variance_variable = model.get_variable_assigned_to_column(data_location['variance'])
    
    ests = [study.get_var(ests_variable) for study in included_studies]
    SEs =  [math.sqrt(study.get_var(variance_variable)) for study in included_studies] 
    
    ests_str = ", ".join(_to_strs(ests))
    SEs_str = ", ".join(_to_strs(SEs))
    
    
    # TODO: add this covariate handling back in 
    #cov_str = "list()"
    # generate the covariate string
    cov_str = list_of_cov_value_objects_str(studies=included_studies, cov_list=covs_to_include)


    # first try and construct an object with raw data -- note that if
    # we're using a one-armed metric for cont. data, we just use y/SE
    if not one_arm and studies_have_raw_data(studies=included_studies,
                                             data_type=data_type,
                                             data_location=data_location,
                                             model=model,
                                             first_arm_only=one_arm):
        print "we have raw data... parsing, parsing, parsing"
        
        Ns1_col    = data_location['experimental_sample_size']
        means1_col = data_location['experimental_mean']
        SDs1_col   = data_location['experimental_std_dev']
        Ns2_col    = data_location['control_sample_size']
        means2_col = data_location['control_mean']
        SDs2_col   = data_location['control_std_dev']
        
        Ns1_var    = model.get_variable_assigned_to_column(Ns1_col)
        means1_var = model.get_variable_assigned_to_column(means1_col)
        SDs1_var   = model.get_variable_assigned_to_column(SDs1_col)
        Ns2_var    = model.get_variable_assigned_to_column(Ns2_col)
        means2_var = model.get_variable_assigned_to_column(means2_col)
        SDs2_var   = model.get_variable_assigned_to_column(SDs2_col)
        
        Ns1    = [study.get_var(Ns1_var) for study in included_studies]
        means1 = [study.get_var(means1_var) for study in included_studies]
        SDs1   = [study.get_var(SDs1_var) for study in included_studies]
        Ns2    = [study.get_var(Ns2_var) for study in included_studies]
        means2 = [study.get_var(means2_var) for study in included_studies]
        SDs2   = [study.get_var(SDs2_var) for study in included_studies]
        
        Ns1_str    = ", ".join(_to_strs(Ns1))
        means1_str = ", ".join(_to_strs(means1))
        SDs1_str   = ", ".join(_to_strs(SDs1))
        Ns2_str    = ", ".join(_to_strs(Ns2))
        means2_str = ", ".join(_to_strs(means2))
        SDs2_str   = ", ".join(_to_strs(SDs2))

        r_str = "%s <- new('ContinuousData', \
                                     N1=c(%s), mean1=c(%s), sd1=c(%s), \
                                     N2=c(%s), mean2=c(%s), sd2=c(%s), \
                                     y=c(%s), SE=c(%s), study.names=c(%s),\
                                    years=c(%s), covariates=%s)" \
                        % (var_name, Ns1_str, means1_str, SDs1_str,
                            Ns2_str, means2_str, SDs2_str,
                            ests_str, SEs_str, study_names, study_years, cov_str)
         
    else:
        print "no raw data (or one-arm)... using effects"
        r_str = "%s <- new('ContinuousData', \
                            y=c(%s), SE=c(%s), study.names=c(%s),\
                            years=c(%s), covariates=%s)" \
                            % (var_name, ests_str, SEs_str, \
                                study_names, study_years, cov_str)
        
    # character encodings for R
    r_str = _sanitize_for_R(r_str)
    print "executing: %s" % r_str
    ro.r(r_str)
    print "ok."
    return r_str

def _to_strs(v):
    return [str(x) for x in v]

def _sanitize_for_R(a_str):
    # may want to do something fancier in the future...
    return a_str.encode('latin-1', 'ignore')


    # Mysterious fix for issue #73. For some reason, R doesn't throw up anymore
    # when non-latin characters are given. Maybe this was fixed in R at some
    # point by a 3rd party.
    #return a_str

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
        m2i  = [None_to_NA(x, float) for x in m2i]
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
    
    print("Executing in R: %s" % r_str)
    
    
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




def get_available_methods(for_data_type=None, data_obj_name=None, metric=None):
    '''
    Returns a list of methods available in OpenMeta for the particular data_type
    (if one is given). Excludes "*.parameters" methods
    '''
    method_list = ro.r("lsf.str('package:openmetar')")

    # the following constitute 'special' or 'reserved' function
    # names that are used by meta-analyst to parse out available
    # methods and their parameters. we exclude these from the list
    # of available meta-analytic routines.
    # 
    # by convention, the methods available for a data type (e.g., binary)
    # start with the name of the data type. furthermore, the parameters
    # for those methods are returned by a method with a name
    # ending in ".parameters"
    special_endings = [".parameters", ".is.feasible", ".overall",
                       ".regression", "transform.f", ".pretty.names"]
    is_special = lambda f: any([f.endswith(ending) for ending in special_endings])
    all_methods = [method for method in method_list if not is_special(method)]
    if for_data_type is not None:
        all_methods = [method for method in all_methods if method.startswith(for_data_type)]

    # now, if a data object handle was provided, check which methods are feasible
    if data_obj_name is not None:
        # we will return a dictionary mapping pretty
        # names (optionally) to method names; if no pretty name exists,
        # then we just map the method name to itself.
        # note that if more than one method exists with the same pretty name
        # it will be overwritten!
        feasible_methods = {}
        for method in all_methods:
            is_feasible = True
            # we check if the author of this method has provided an is.feasible
            # routine; if so, we will call it. otherwise, we assume that we can
            # invoke the corresponding routine (i.e., we assume it's feasible)
            is_feas_f = "%s.is.feasible" % method
            if is_feas_f in method_list:
                # we need to pass along the metric along with the data 
                # object to assess if a given method is feasible (e.g,.
                # PETO for binary data only makes sense for 'OR')
                is_feasible = ro.r("%s(%s, '%s')" % (is_feas_f, data_obj_name, metric))[0]
 
            if is_feasible:
                # do we have a pretty name?
                pretty_names_f = "%s.pretty.names" % method
                if pretty_names_f in method_list:
                    pretty_name = ro.r("%s()$pretty.name" % pretty_names_f)[0]
                    feasible_methods[pretty_name] = method
                else:
                    # no? then just map to the function name
                    feasible_methods[method] = method
    return feasible_methods


def get_params(method_name):
    param_list = ro.r("%s.parameters()" % method_name)
    # note that we're assuming that the last entry of param_list, as provided
    # by the corresponding R routine, is the order to display the variables
    param_d = {}
    for name, r_obj in zip(param_list.names, param_list):    
        param_d[name] = r_obj

    order_vars = None
    if param_d.has_key("var_order"):
        order_vars = list(param_d["var_order"])

    pretty_names_and_descriptions = get_pretty_names_and_descriptions_for_params(
                                        method_name, param_list)

    return (R_parse_tools.recursioner(param_d['parameters']),
            R_parse_tools.recursioner(param_d['defaults']),
            order_vars,
            pretty_names_and_descriptions,
            )

     
def get_pretty_names_and_descriptions_for_params(method_name, param_list):
    method_list = ro.r("lsf.str('package:openmetar')")
    pretty_names_f = "%s.pretty.names" % method_name
    params_d = {}
    if pretty_names_f in method_list:
        # try to match params to their pretty names and descriptions
        pretty_names_and_descriptions = ro.r("%s()" % pretty_names_f)
        # this dictionary is assumed to be as follows:
        #      params_d[param] --> {"pretty.name":XX, "description":XX}
        params_d = R_parse_tools.recursioner(pretty_names_and_descriptions)

    # fill in entries for parameters for which pretty names/descriptions were
    # not provided-- these are just place-holders to make processing this
    # easier
    names_index = param_list.names.index("parameters") 
    param_names = param_list[names_index].names # pull out the list
    for param in param_names:
        if not param in params_d.keys():
            params_d[param] = {"pretty.name":param, "description":"None provided"}
    
    return params_d

def parse_out_results(result):
    # parse out text field(s). note that "plot names" is 'reserved', i.e., it's
    # a special field which is assumed to contain the plot variable names
    # in R (for graphics manipulation).
    text_d = {}
    image_var_name_d, image_params_paths_d, image_path_d  = {}, {}, {}
    image_order = None

    for text_n, text in zip(list(result.names), list(result)):
        # some special cases, notably the plot names and the path for a forest
        # plot. TODO in the case of diagnostic data, we're probably going to 
        # need to parse out multiple forest plot param objects...
        print text_n
        print "\n--------\n"
        if text_n == "images":
            image_path_d = R_parse_tools.recursioner(text)
        elif text_n == "image_order":
            image_order = list(text)
        elif text_n == "plot_names":
            if str(text) == "NULL":
                image_var_name_d = {}
            else:
                image_var_name_d = R_parse_tools.recursioner(text)
        elif text_n == "plot_params_paths":
            if str(text) == "NULL":
                image_params_paths_d = {}
            else:
                image_params_paths_d = R_parse_tools.recursioner(text)
        elif text_n == "References":
            references_list = list(text)
            references_list.append('metafor: Viechtbauer, Wolfgang. "Conducting meta-analyses in R with the metafor package." Journal of 36 (2010).')
            references_list.append('OpenMetaAnalyst: Wallace, Byron C., Issa J. Dahabreh, Thomas A. Trikalinos, Joseph Lau, Paul Trow, and Christopher H. Schmid. "Closing the Gap between Methodologists and End-Users: R as a Computational Back-End." Journal of Statistical Software 49 (2012): 5."')
            ref_set = set(references_list) # removes duplicates
            
            
            references_str = ""
            for i, ref in enumerate(ref_set):
                references_str += str(i+1) + ". " + ref + "\n"
            
            text_d[text_n] = references_str

        else:
            text_d[text_n]=str(text)
            
            #pyqtRemoveInputHook()
            #pdb.set_trace()
            # Construct List of Weights for studies
            (key, astring) = make_weights_list(text_n,text)
            if key is not None:
                text_d[key] = astring

    to_return = {"images":image_path_d,
                 "image_var_names":image_var_name_d,
                 "texts":text_d,
                 "image_params_paths":image_params_paths_d,
                 "image_order":image_order}
    
    return to_return

def make_weights_list(text_n,text):
    # Construct List of Weights for studies
    if text_n.find("Summary") == -1: # 'Summary' not found
        return (None,None)
    
    if not R_parse_tools.haskeys(text): # if the text is not a dictionary it won't have weights, trust me
        return (None, None)
    
    summary_dict = R_parse_tools.rlist_to_pydict(text)
    
    if R_parse_tools.haskeys(summary_dict['MAResults']):
        summary_dict['MAResults'] = R_parse_tools.rlist_to_pydict(summary_dict['MAResults'])
    else:
        return (None,None)
    
    # this is a silly thing to look for but its something I explicitly
    # set in the random methods so I know it's there
    if "study.names" in summary_dict['MAResults']: 
        print("study.names found in maresults")
        text_n_withoutSummary = text_n.replace("Summary","")
        text_n_withoutSummary.strip()
        key_name = text_n_withoutSummary + " Weights"
        key_name = key_name.strip()
        
        study_names = R_parse_tools.R_iterable_to_pylist(summary_dict['MAResults']['study.names'])
        #study_years = R_parse_tools.R_iterable_to_pylist(summary_dict['MAResults']['study.years'])
        study_weights = R_parse_tools.R_iterable_to_pylist(summary_dict['MAResults']['study.weights'])
        
        max_len_name = max([len(name) for name in study_names])
        max_len = max([max_len_name,len("studies")])
        
        weights_txt = unicode("studies" + " "*(max_len-len("studies")+1) + "weights\n")
        
        for name,weight in zip(study_names, study_weights):
            weights_txt += unicode("{0:{name_width}} {1:4.1f}%\n").format(name, weight*100, name_width=max_len)
        return (key_name, weights_txt)
    else:
        print("study.names not found")
    return(None,None)

def run_binary_ma(function_name, params, res_name="result", bin_data_name="tmp_obj"):
    params_df = ro.r['data.frame'](**params)
    r_str = "%s<-%s(%s, %s)" % (res_name, function_name, bin_data_name,\
                                    params_df.r_repr())
    print "\n\n(run_binary_ma): executing:\n %s\n" % r_str
    ro.r(r_str)
    result = ro.r("%s" % res_name)
    return parse_out_results(result)

def run_continuous_ma(function_name, params, res_name = "result", cont_data_name="tmp_obj"):
    params_df = ro.r['data.frame'](**params)
    r_str = "%s<-%s(%s, %s)" % (res_name, function_name, cont_data_name, params_df.r_repr())
    print "\n\n(run_continuous_ma): executing:\n %s\n" % r_str
    ro.r(r_str)
    result = ro.r("%s" % res_name)
    return parse_out_results(result)

def run_meta_method(meta_function_name, function_name, params, \
                        res_name="result", data_name="tmp_obj"):
    '''
    Runs a binary `meta` method over the data in the bin_data_name argument
    (on the R side). The meta-method called is specified by the meta_function_name
    argument. 
    '''
    params_df = ro.r['data.frame'](**params)
    r_str = "%s<-%s('%s', %s, %s)" % \
            (res_name, meta_function_name, function_name, data_name, params_df.r_repr())

    print "\n\n(run_meta_method): executing:\n %s\n" % r_str

    ro.r(r_str)
    result = ro.r("%s" % res_name)
    
    # parse out text field(s). note that "plot names" is 'reserved', i.e., it's
    # a special field which is assumed to contain the plot variable names
    # in R (for graphics manipulation).
    return parse_out_results(result)

def run_meta_regression(metric, fixed_effects=False, data_name="tmp_obj",
                        results_name="results_obj", 
                        conf_level=DEFAULT_CONFIDENCE_LEVEL): 
    
    if conf_level is None:
        raise ValueError("Confidence level must be specified")
                        
    method_str = "FE" if fixed_effects else "DL"    

    # @TODO conf.level, digits should be user-specified
    params = {"conf.level": conf_level,
              "digits": 3,
              "method": method_str,
              "rm.method": "ML",
              "measure": METRIC_TO_ESCALC_MEASURE[metric]}
    params_df = ro.r['data.frame'](**params)

    # create a lit of covariate objects on the R side
    r_str = "%s<- meta.regression(%s, %s)" % \
                            (results_name, data_name, str(params_df.r_repr()))


    print "\n\n(run_meta_regression): executing:\n %s\n" % r_str

    ### TODO -- this is hacky

    ro.r(r_str)
    result = ro.r("%s" % results_name)

    if "try-error" in str(result):
        # uh-oh, there was an error (but the weird
        # RRunTimeError alluded to above; this is a 
        # legit error returned from an R routine)
        return str([msg for msg in result][0])
 

    parsed_results = parse_out_results(result)

    return parsed_results

def get_method_description(method_name):
    pretty_names_f = "%s.pretty.names" % method_name
    method_list = ro.r("lsf.str('package:openmetar')")
    description = "None provided."
    if pretty_names_f in method_list:
        try:
            description = ro.r("%s()$description" % pretty_names_f)[0]
        except:
            pass
    return description


###### R data structure tools #############

class R_parse_tools:
    ''' a set of tools to help parse data structures returned from rpy2 '''
    def __init__(self):
        pass
    
    @staticmethod
    def rlist_to_pydict(named_r_list):
        ''' parse named R list into a python dictionary.'''
            #Only parses one level, is not recursive.'''
            
        keys = named_r_list.names
        if str(keys) == "NULL":
            raise ValueError("No names found in alleged named R list")
        
        data = R_parse_tools.R_iterable_to_pylist(named_r_list)
        d = dict(zip(keys, data))    
        
        return d
    
    @staticmethod
    def recursioner(data):
        '''
        named_r_list --> python dictionary
        not named r_list --> python list
               singleton_r_list ---> python scalar
        '''
        
        if R_parse_tools.haskeys(data): # can be converted to dictionary
            d = R_parse_tools.rlist_to_pydict(data)
            for k,v in d.items():
                d[k] = R_parse_tools.recursioner(v)
            return d
        elif R_parse_tools._isListable(data): # can be converted to list
            l = R_parse_tools.R_iterable_to_pylist(data)
            for i,v in enumerate(l):
                l[i] = R_parse_tools.recursioner(v)
            return l
        else: # is a scalar
            return R_parse_tools._convert_NA_to_None(data) # convert NA to None
        
    
    
            
    @staticmethod
    def R_iterable_to_pylist(r_iterable):
        ''' Converts an r_iterable (i.e. list or vector) to a python list.
            Will convert singleton elements to scalars in the list but not the list
            itself if it is singleton.  '''
        
        def filter_list_element(x):
            ''' if x is a singleton list, converts x to a scalar '''
            if R_parse_tools._isListable(x) and len(x) == 1:
                return R_parse_tools._singleton_list_to_scalar(x)
            else:
                return x
        
        python_list = list(r_iterable)
        python_list = [filter_list_element(x) for x in python_list]
        return python_list
    
    @staticmethod
    def _singleton_list_to_scalar(singleton_list):
        ''' Takes in a singleton R list and returns a scalar value and converts 'NA'
        to None '''
        
        if len(singleton_list) > 1:
            raise ValueError("Expected a singleton list but this list has more than one entry")
        
        # special case of a factor ve
        if type(singleton_list) == rpy2.robjects.vectors.FactorVector:
            return ro.r("as.character(%s)" % singleton_list.r_repr())[0]
        
        scalar = singleton_list[0]
        return R_parse_tools._convert_NA_to_None(scalar)
    
    
    @staticmethod
    def _convert_NA_to_None(scalar):
        if str(scalar) == 'NA':
            return None
        else:
            return scalar
    
    @staticmethod
    def _isListable(element, exclude_strings = True):
        try:
            list(element)
        except TypeError:
            return False
        
        # don't want to treat strings as lists even though they are iterable
        if exclude_strings and type(element) == str:
            return False
        
        return True
        
    @staticmethod
    def haskeys(r_object):
        if not hasattr(r_object,'names'):
            return False
        
        return str(r_object.names) != "NULL"
#### end of R data structure tools #########


def load_vars_for_plot(params_path, return_params_dict=False):
    ''' 
    loads the three necessary (for plot generation) variables
    into R. we assume a naming convention in which params_path
    is the base, data is stored in *.data, params in *.params
    and result in *.res.
    '''
    for var in ("data", "params", "res"):
        cur_path = "%s.%s" % (params_path, var)
        if os.path.exists(cur_path):
            load_in_R(cur_path)
            print "loaded %s" % cur_path
        else:
            print "whoops -- couldn't load %s" % cur_path
            return False

    if return_params_dict:
        robj = ro.r("params")
        params_dict = R_parse_tools.recursioner(robj)
        return params_dict
    return True

def regenerate_plot_data(om_data_name="om.data", res_name="res",           
                            plot_params_name="params", plot_data_name="plot.data"):
    
    ####
    # this is crude, but works for now, and easier than making
    # the results_window keep track of why type of data it's
    # displaying. may need to re-think this ain any case for the
    # general case of plots (what 'type' is a mixed analysis, e.g.?)
    ####
    data_type = str(ro.r("class(%s)" % om_data_name))

    if "BinaryData" in data_type:
        ro.r("plot.data<-create.plot.data.binary(%s, %s, %s)" % \
                            (om_data_name, plot_params_name, res_name))
    elif "ContinuousData" in data_type:
        ro.r("plot.data<-create.plot.data.continuous(%s, %s, %s)" % \
                            (om_data_name, plot_params_name, res_name))
    else:
        ro.r("plot.data<-create.plot.data.diagnostic(%s, %s, %s)" % \
                            (om_data_name, plot_params_name, res_name))
        
def update_plot_params(plot_params, plot_params_name="params", \
                        write_them_out=False, outpath=None):
    # first cast the params to an R data frame to make it
    # R-palatable
    params_df = ro.r['data.frame'](**plot_params)
    ro.r("tmp.params <- %s" % params_df.r_repr())
   
    for param_name in plot_params:
        ro.r("%s$%s <- tmp.params$%s" % \
                (plot_params_name, param_name, param_name))

    if write_them_out:
        ro.r("save(tmp.params, file='%s')" % outpath)
        
def write_out_plot_data(params_out_path, plot_data_name="plot.data"):
    ro.r("save.plot.data(%s, '%s')" % (plot_data_name, params_out_path))
    

######### DEAL WITH COVARIATES #########

def list_of_cov_value_objects_str(studies, cov_list=[]):
    ''' makes r_string of covariate objects with their values '''
    
    r_cov_str = []
    for cov in cov_list:
        r_cov_str.append(_gen_cov_vals_obj_str(cov, studies))
    r_cov_str = "list(" + ",".join(r_cov_str) + ")"

    return r_cov_str


def _gen_cov_vals_obj_str(cov, studies):
    ''' makes an R-evalable string to generate a covariate in R'''
    
    values_str, cov_vals = cov_to_str(cov, studies, named_list=False, return_cov_vals=True)
    ref_var = cov_vals[0].replace("'", "") # arbitrary

    ## setting the reference variable to the first entry
    # for now -- this only matters for factors, obviously

    r_str = "new('CovariateValues', cov.name='%s', cov.vals=%s, \
                    cov.type='%s', ref.var='%s')" % \
                (cov.get_label(), values_str, COVARIATE_TYPE_TO_OMA_STR_DICT[cov.get_type()], ref_var)
    return r_str

def cov_to_str(cov, studies, named_list=True, return_cov_vals=False):
    '''
    The string is constructed so that the covariate
    values are in the same order as the studies
    list.
    '''
    cov_str = None
    if named_list:
        cov_str = "%s=c(" % cov.get_label()
    else:
        cov_str = "c("

    def convert_cov_value(cov_type, value):
        if cov_type == CONTINUOUS:
            if value is None:
                return "NA"
            else:
                return "%s" % str(value)
        elif cov_type == CATEGORICAL:
            if value is None:
                return "NA"
            else:
                return "'%s'" % unicode(str(value).encode('latin1'), 'latin1')
        else:
            raise Exception("Unrecognized covariate type")


    cov_values = [study.get_var(cov) for study in studies]
    cov_values = [convert_cov_value(cov.get_type(), value) for value in cov_values]

    cov_str += ",".join(cov_values) + ")"
    
    if return_cov_vals:
        return (cov_str, cov_values)
    return cov_str

##################### END OF COVARIATE STUFF #################################
##################
#                #
# George Dietz   #
# Byron Wallace  #
# CEBM@Brown     #
#                #
##################

import math
from collections import OrderedDict

from ome_globals import *

import rpy2
import rpy2.robjects
from rpy2 import robjects as ro
import rpy2.rlike.container as rlc

from rpy2.robjects.packages import importr
base = importr('base')


# Need this class to deal with logging R output
class RExecutor:
    def __init__(self):
        self.R_log_dialog = None
        print("New RExecutor created")

    def set_R_log_dialog(self, dialog):
        self.R_log_dialog = dialog

    def unset_R_log_dialog(self):
        self.R_log_dialog = None

    def execute_in_R(self, r_str, show_output=False, reset_wd=True):
        try:
            print("Executing in R: %s" % r_str)

            # send R string to logger
            if self.R_log_dialog:
                self.R_log_dialog.append(r_str)

            res = ro.r(r_str)
            if show_output:
                self.R_log_dialog.append("Output: %s\n" % str(res))
            return res
        except Exception as e:
            print("error in execute in r: %s" % e)
            if reset_wd:
                reset_Rs_working_dir()

            raise CrazyRError("Some crazy R error occurred: %s" % str(e))

exR = RExecutor()

#################### R Library Loader ####################
class RlibLoader:
    def __init__(self):
        print("R Libary loader (RlibLoader) initialized...")

    def load_ape(self):
        return self._load_r_lib("ape")

    def load_mice(self):
        return self._load_r_lib("mice")

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
            exR.execute_in_R("library(%s)" % name)
            msg = "%s package successfully loaded" % name
            print(msg)
            return (True, msg)
        except:
            raise Exception("The %s R package is not installed.\nPlease \
install this package and then re-start OpenMeta." % name)
#################### END OF R Library Loader ####################

def load_ape_file(ape_path, tree_format):
    # uses r package APE to load a tree in to object of class phylo (R object)
    print("loading ape file... {0} of format {1}".format(ape_path, tree_format))
    #ext = ape_path.split(".")[-1]
    #r_str = "phylo.tree <- read."
    if tree_format == "caic":
        print("parsing caic file")
        r_str = 'read.caic("%s")' % ape_path
    elif tree_format == "nexus":
        print("parsing nexus file")
        r_str = 'read.nexus("%s")' % ape_path
    elif tree_format in ["newick", "new_hampshire"]:
        print("parsing either a Newick or New Hampshire file...")
        r_str = 'read.tree("%s")' % ape_path
    else:
        # @TODO return error message to user
        print("I do not know how to parse {0} files!".format(tree_format))
        raise Exception("Unrecognized tree file format")
    phylo_obj = exR.execute_in_R(r_str)

    # Validate tree
    exR.execute_in_R("validate.tree(%s)" % phylo_obj.r_repr())

    print("ok! loaded.")
    return phylo_obj


def reset_Rs_working_dir():
    ''' resets R's working directory to the the application base_path, not to r_tmp!'''
    print("resetting R working dir")

    # Fix paths issue in windows
    base_path = get_base_path()
    base_path = to_posix_path(base_path)

    print("Trying to set base_path to %s" % base_path)
    r_str = "setwd('%s')" % base_path
    # Executing r call with escaped backslashes
    exR.execute_in_R(r_str)

    print("Set R's working directory to %s" % base_path)

def set_conf_level_in_R(conf_lev):

    invalid_conf_lev_msg = "Confidence level needs to be a number between 0 and 100"
    if conf_lev is None:
        raise ValueError(invalid_conf_lev_msg)
    elif not (0 < conf_lev < 100):
        raise ValueError(invalid_conf_lev_msg)


    r_str = "set.global.conf.level("+str(float(conf_lev))+")"
    new_cl_in_R = exR.execute_in_R(r_str)[0]
    print("Set confidence level in R to: %f" % new_cl_in_R)

    return conf_lev

def generate_forest_plot(file_path, side_by_side=False, params_name="plot.data"):
    if side_by_side:
        print "generating a side-by-side forest plot..."
        exR.execute_in_R("two.forest.plots(%s, '%s')" % (params_name, file_path))
    else:
        conf_level = exR.execute_in_R("get.global.conf.level()")[0]
        print("Confidence Level before generation: %s" % str(conf_level))

        print("generating a forest plot....")
        exR.execute_in_R("forest.plot(%s, '%s')" % (params_name, file_path))

def regenerate_phylo_forest_plot(img_path,
                                 params_name="params",
                                 data_name="data",
                                 res_name = "res",
                                 params_path = "NULL",
                                 level_name = "level"):
    
    r_str = "regenerate_phylo_forest_plot(plot.params={params_name}, data={data_name}, res={res_name}, level={level_name}, params.out.path=\"{params_path}\", out.path=\"{img_path}\")".format(
                    params_name=params_name, data_name=data_name,
                    res_name=res_name, level_name=level_name, params_path=params_path,
                    img_path=img_path)
    exR.execute_in_R(r_str)

def regenerate_funnel_plot(params_path, file_path, edited_funnel_params=None):
    if edited_funnel_params:
        funnel_params_r_str = unpack_r_parameters(prepare_funnel_params_for_R(edited_funnel_params))
        r_str = "regenerate.funnel.plot(out.path='%s', plot.path='%s', edited.funnel.params=list(%s))" % (params_path, file_path, funnel_params_r_str)
    else:
        r_str = "regenerate.funnel.plot(out.path='%s', plot.path='%s')" % (params_path, file_path)

    exR.execute_in_R(r_str)

def regenerate_exploratory_plot(params_path, file_path, plot_type, edited_params=None):
    if plot_type == "histogram":
        params_r = histogram_params_toR(edited_params) if edited_params else None
        plot_type = "HISTOGRAM"
    elif plot_type == "scatterplot":
        params_r = scatterplot_params_to_R(edited_params) if edited_params else None
        plot_type = "SCATTERPLOT"
    else:
        raise Exception("Unrecognized plot type")

    if edited_params:
        r_str = "regenerate.exploratory.plot(out.path='%s', plot.path='%s', plot.type='%s', edited.params=%s)" % (params_path, file_path, plot_type, params_r.r_repr())
    else:
        r_str = "regenerate.exploratory.plot(out.path='%s', plot.path='%s', plot.type='%s')" % (params_path, file_path, plot_type)

    exR.execute_in_R(r_str)


def load_in_R(fpath):
    ''' loads what is presumed to be .Rdata into the R environment '''
    r_str = "load('%s')" % fpath
    exR.execute_in_R(r_str)

def generate_reg_plot(file_path, params_name="plot.data"):
    r_str = "meta.regression.plot(%s, '%s')" % (params_name, file_path)
    exR.execute_in_R(r_str)

def gather_data(model, data_location, vars_given_directly=False):
    ''' Gathers the relevant data in one convenient location for the purpose
    of sending to R '''

    # list of studies as currently shown on the spreadsheet
    studies = model.get_studies_in_current_order()

    data = {}
    for k, col_or_var in data_location.items():
        var = col_or_var if vars_given_directly else model.get_variable_assigned_to_column(col_or_var)
        data[k] = [study.get_var(var) for study in studies]

    data['study_labels'] = [study.get_label() for study in studies]

    return data

def gather_data_for_single_study(data_location, study):
    # data_location is mapping location key --> var
    data = dict([(k,study.get_var(var)) for k,var in data_location.items()])
    data['study_labels'] = study.get_label()
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

def keys_in_dictionary(keys, dictionary):
    return set(keys) <= set(dictionary.keys())


def studies_have_raw_data(studies, data_type, data_location, model, first_arm_only=False):
    ''' True iff all the studies in 'studies' have 'raw' data for the currently
    selected outcome. If the metric is one-arm, we only check the raw data corresponding to that arm'''

    if data_type == MEANS_AND_STD_DEVS:
        if not keys_in_dictionary(['experimental_mean',
                                   'experimental_std_dev',
                                   'experimental_sample_size'], data_location):
            return False
        columns_to_check = [data_location['experimental_mean'],
                            data_location['experimental_std_dev'],
                            data_location['experimental_sample_size'],]
        if not first_arm_only: # add additional columns to check
            if not keys_in_dictionary(['control_mean',
                                       'control_std_dev',
                                       'control_sample_size'], data_location):
                return False
            columns_to_check.extend([data_location['control_mean'],
                                     data_location['control_std_dev'],
                                     data_location['control_sample_size'],])

    elif data_type == TWO_BY_TWO_CONTINGENCY_TABLE:
        if not keys_in_dictionary(['experimental_response',
                                   'experimental_noresponse'], data_location):
            return False

        columns_to_check = [data_location['experimental_response'],
                            data_location['experimental_noresponse'],]

        if not first_arm_only:
            if not keys_in_dictionary(['control_response',
                                       'control_noresponse'], data_location):
                return False
            columns_to_check.extend([data_location['control_response'],
                                     data_location['control_noresponse'],
                                     ])

    elif data_type == CORRELATION_COEFFICIENTS:
        if not keys_in_dictionary(['correlation',
                                   'sample_size'], data_location):
            return False
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
                                  include_raw_data=True, covs_to_include=[],
                                  covariate_reference_values={},
                                  one_arm=False
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

    study_years = joiner(["as.integer(%s)" % none_to_str(None) for study in included_studies])
    study_names = joiner(['"' + study.get_label(none_to_empty_string=True) + '"' for study in included_studies])

    ests_variable = model.get_variable_assigned_to_column(data_location['effect_size'])
    variance_variable = model.get_variable_assigned_to_column(data_location['variance'])

    ests = [study.get_var(ests_variable) for study in included_studies]
    SEs =  [math.sqrt(study.get_var(variance_variable)) for study in included_studies]

    ests_str = joiner(_to_strs(ests))
    SEs_str  = joiner(_to_strs(SEs))

    cov_str = list_of_cov_value_objects_str(studies=included_studies,
                                            cov_list=covs_to_include,
                                            cov_to_ref_var=covariate_reference_values)


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

        g1O1_str = joiner(_to_strs(g1_events))
        g1O2_str = joiner(_to_strs(g1_no_events))



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

            g2O1_str = joiner(_to_strs(g2_events))
            g2O2_str = joiner(_to_strs(g2_no_events))


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
    exR.execute_in_R(r_str)
    print "ok."

    #print("Inspecting R object time")
    #pyqtRemoveInputHook()
    #import pdb; pdb.set_trace()


    return r_str


def dataset_to_simple_continuous_robj(model, included_studies, data_location,
                                      data_type,
                                      var_name="tmp_obj",
                                      covs_to_include=[],
                                      covariate_reference_values={},
                                      one_arm=False, generic_effect=False):
    r_str = None

    ###study_ids = [study.get_id() for study in included_studies]

    ####study_names = ", ".join(["'" + study.get_label(none_to_empty_string=True) + "'" for study in included_studies])
    study_names = ['"' + study.get_label(none_to_empty_string=True) + '"' for study in included_studies]
    study_names = joiner(study_names)

    none_to_str = lambda n : str(n) if n is not None else "" # this will produce NA ints
    ###study_years = ", ".join(["as.integer(%s)" % none_to_str(None) for study in included_studies])
    study_years = ["as.integer(%s)" % none_to_str(None) for study in included_studies]
    study_years = joiner(study_years)

    ests_variable = model.get_variable_assigned_to_column(data_location['effect_size'])
    variance_variable = model.get_variable_assigned_to_column(data_location['variance'])

    ests = [study.get_var(ests_variable) for study in included_studies]
    SEs =  [math.sqrt(study.get_var(variance_variable)) for study in included_studies]

    ests_str = joiner(_to_strs(ests))
    SEs_str = joiner(_to_strs(SEs))

    cov_str = list_of_cov_value_objects_str(studies=included_studies,
                                            cov_list=covs_to_include,
                                            cov_to_ref_var=covariate_reference_values)


    # first try and construct an object with raw data -- note that if
    # we're using a one-armed metric for cont. data, we just use y/SE
    if not generic_effect and not one_arm and studies_have_raw_data(studies=included_studies,
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

        Ns1_str    = joiner( _to_strs(Ns1)    )
        means1_str = joiner( _to_strs(means1) )
        SDs1_str   = joiner( _to_strs(SDs1)   )
        Ns2_str    = joiner( _to_strs(Ns2)    )
        means2_str = joiner( _to_strs(means2) )
        SDs2_str   = joiner( _to_strs(SDs2)   )


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
    exR.execute_in_R(r_str)
    print "ok."
    return r_str


NUMERIC_AND_CATEGORICAL, INT_CONTINUOUS_FACTOR = range(2)
def sort_covariates_by_type(covs, sort_method=NUMERIC_AND_CATEGORICAL):
    ''' Sorts covariates in to categories:
    if sort_method == NUMERIC_AND_CATEGORICAL:
        'numeric' and 'categorical'
    elif sort_method == INT_CONTINUOUS_FACTOR:
        'int', 'continuous', 'factor'
    Then, within those categories, sort the covariates alphabetically why not '''

    label_of_cov = lambda x: x.get_label()

    if sort_method == NUMERIC_AND_CATEGORICAL:
        type_cov_num = [COUNT, CONTINUOUS] # Numerical covariate types
        type_cov_cat = [CATEGORICAL,]      # Categorical covariate type

        cov_num = [cov for cov in covs if cov.get_type() in type_cov_num]
        cov_cat = [cov for cov in covs if cov.get_type() in type_cov_cat]

        if len(cov_num) + len(cov_cat) != len(covs):
            raise Exception("Something is wrong with the covariate types")

        # sort the covariates alphabetically in each section
        cov_num.sort(key = label_of_cov)
        cov_cat.sort(key = label_of_cov)

        return {'numeric':cov_num,
                'categorical':cov_cat}
    elif sort_method == INT_CONTINUOUS_FACTOR:
        type_int = [COUNT,]
        type_cont = [CONTINUOUS,] # continuous
        type_factor = [CATEGORICAL,]

        cov_int    = [cov for cov in covs if cov.get_type() in type_int]
        cov_cont   = [cov for cov in covs if cov.get_type() in type_cont]
        cov_factor = [cov for cov in covs if cov.get_type() in type_factor]

        if len(cov_int) + len(cov_cont) + len(cov_factor) != len(covs):
            raise Exception("Something is wrong with the covariate types")

        # sort the covariates alphabetically in each section
        cov_int.sort(key = label_of_cov)
        cov_cont.sort(key = label_of_cov)
        cov_factor.sort(key = label_of_cov)

        return {'int':cov_int,
                'continuous':cov_cont,
                'factor':cov_factor}
    else:
        raise Exception("Unrecognized sorting method")

def dataset_to_dataframe(model, included_studies, data_location, covariates=[],
                         cov_ref_values={}, var_name="tmp_obj"):
    # Creates an R dataframe with the portion of the dataset of interest as
    # specified by included_studies and covariates. Categorical variables in the
    # dataframe are converted to factors with referenece values set as specified
    # in cov_ref_values

    yi_var = model.get_variable_assigned_to_column(data_location['effect_size'])
    vi_var = model.get_variable_assigned_to_column(data_location['variance'])

    # For issue #15 (phylogenetics) need a "species" column
    include_species = "species" in data_location.keys()
    if include_species:
        species_var = model.get_variable_assigned_to_column(data_location['species'])

    # Gathers values of the variable from amongst the included studies
    var_values = lambda x: [study.get_var(x) for study in included_studies]

    # Gather data
    yi = var_values(yi_var)
    vi = var_values(vi_var)
    slab = [study.get_label() for study in included_studies] # study labels

    # Covariates sorted into 'numeric' and 'categorical' categories
    sorted_covariates = sort_covariates_by_type(covariates)

    # Convert covariates to R representation
    def cov_to_FloatVector(cov):
        values = var_values(cov)
        # convert Nones to NA
        values = [None_to_NA(x, float) for x in values]
        return ro.FloatVector(values)
    def cov_to_Factor(cov):
        ref_value = cov_ref_values[cov] if cov in cov_ref_values else None
        values = var_values(cov)
        values = [None_to_NA(x, str) for x in values]
        levels = list(set(values))
        levels.sort()
        if ref_value:
            # stick ref_value at the beginning
            levels.remove(ref_value)
            levels = [ref_value,]+levels

        rfactor = ro.FactorVector(values,levels=ro.StrVector(levels))
        return rfactor


    numeric_covs = dict([(cov.get_label(),cov_to_FloatVector(cov)) for cov in sorted_covariates['numeric']])
    cat_covs = dict([(cov.get_label(),cov_to_Factor(cov)) for cov in sorted_covariates['categorical']])
    if include_species:
        # species covariate as an R-format factor
        species_rcov = cov_to_Factor(species_var)

    # Inhibit transformation of vectors upon insertion into dataframe
    for name, rvector in numeric_covs.iteritems():
        numeric_covs[name] = base.I(rvector)
    for name, rvector in cat_covs.iteritems():
        cat_covs[name] = base.I(rvector)


    cov_labels = numeric_covs.keys()+cat_covs.keys()
    if ('yi' in cov_labels) or ('vi' in cov_labels):
        raise Exception("Forbidden covariate label present")

    init_dict = {'slab': base.I(ro.StrVector(slab)),
                 'yi'  : ro.FloatVector(yi),
                 'vi'  : ro.FloatVector(vi)}
    if include_species:
        init_dict['species']=species_rcov
    init_dict.update(numeric_covs)
    init_dict.update(cat_covs)

    dataf = ro.DataFrame(init_dict)
    if var_name: # don't put the dataframe into the workspace if var_name is None
        exR.execute_in_R("%s<-%s" % (var_name,dataf.r_repr())) # create dataframe in r workspace
    return dataf

def dataset_to_simple_fsn_data_robj(model, included_studies, data_location,
                                    var_name="tmp_obj"):
    # Package dataset for use with failsafe.wrapper() in R

    ests_variable = model.get_variable_assigned_to_column(data_location['effect_size'])
    variance_variable = model.get_variable_assigned_to_column(data_location['variance'])

    ests = [study.get_var(ests_variable) for study in included_studies]
    variances = [study.get_var(variance_variable) for study in included_studies]

    ests_str = joiner(_to_strs(ests))
    variances_str = joiner(_to_strs(variances))

    r_str = "%s <- data.frame(yi=c(%s), vi=c(%s))" % (var_name, ests_str, variances_str)

    # character encodings for R
    r_str = _sanitize_for_R(r_str)
    exR.execute_in_R(r_str)
    print "ok."
    return r_str

def run_failsafe_analysis(model, included_studies, data_location, failsafe_params,
                          res_name="result", var_name="tmp_obj"):
    make_dataset_r_str = dataset_to_simple_fsn_data_robj(
                                                        model,
                                                        included_studies,
                                                        data_location,
                                                        var_name=var_name)
    # build-up failsafe parameters string
    params_as_strs = []
    for param, val in failsafe_params.items():
        rkey, rval = param, str(val)
        if param == "method":
            rkey = "type"
            rval = '"%s"' % val
        if param=="target" and val=="":
            rval = 'NULL'
        params_as_strs.append("%s=%s" % (rkey,rval))

    r_str = "%s <- failsafe.wrapper(%s, %s)" % (res_name, var_name, ", ".join(params_as_strs))
    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % res_name)
    return parse_out_results(result)

def run_histogram(model, var, params, res_name = "result", var_name = "tmp_obj", summary=""):
    var_type = var.get_type()

    # get data
    studies = model.get_studies_in_current_order()
    data = [study.get_var(var) for study in studies if study.get_var(var) not in [None,""]]
    # put data into R format
    if var_type == COUNT:
        data_r = ro.IntVector(data)
    elif var_type == CONTINUOUS:
        data_r = ro.FloatVector(data)
    elif var_type == CATEGORICAL:
        data_r = ro.StrVector(data)

    # params in R format
    params_r = histogram_params_toR(params)
    # exploratory.plotter <- function(data, params, plot.type)
    r_str = "%s<-exploratory.plotter(%s, %s, plot.type=\"HISTOGRAM\")" % (res_name, data_r.r_repr(), params_r.r_repr())

    result = exR.execute_in_R(r_str)
    return parse_out_results(result)

# put data into R format
def col_data_to_R_fmt(col_data, data_type):
    if data_type == COUNT:
        col_data = ro.IntVector(col_data)
    elif data_type == CONTINUOUS:
        col_data = ro.FloatVector(col_data)
    else:
        raise Exception("Unrecognized data type")
    return col_data

def cols_to_data_frame(model):
    '''
    Create an R data from the model.
    '''
    var_col_d = {}
    col_variables = model.get_variables()
    for col_var in col_variables:
        col_var_name = col_var.get_label()
        var_col_d[col_var_name] = [
                study.get_var(col_var) for study in
                model.get_studies_in_current_order()]

    data_r = ro.DataFrame(var_col_d)
    return data_r

def run_scatterplot(model, xvar, yvar, params, label_points_with_study_names,
                        res_name="result", var_name="tmp_obj"):
    xvar_type = xvar.get_type()
    yvar_type = yvar.get_type()

    # get data
    studies = model.get_studies_in_current_order()
    x_data = [study.get_var(xvar) for study in studies]
    y_data = [study.get_var(yvar) for study in studies]
    labels = [study.get_label() for study in studies]

    # get rid of entries where either x or y is None
    data = [(x,y,label) for (x,y,label) in zip(x_data,y_data,labels)
                if x is not None and y is not None]
    x_data,y_data,labels = zip(*data)

    x_data = col_data_to_R_fmt(x_data, xvar_type)
    y_data = col_data_to_R_fmt(y_data, yvar_type)
    labels = ro.StrVector(labels)
    data = {'x':x_data, 'y':y_data}
    if label_points_with_study_names:
        data['slab']=labels
    data_r = ro.DataFrame(data)

    # params in R format
    params_r = scatterplot_params_to_R(params)
    # exploratory.plotter <- function(data, params, plot.type)
    r_str = "%s<-exploratory.plotter(%s, %s, plot.type=\"SCATTERPLOT\")" % (
            res_name, data_r.r_repr(), params_r.r_repr())

    result = exR.execute_in_R(r_str)
    return parse_out_results(result)


def histogram_params_toR(params):
    ''' converts params to a properly formatted R-list of the params'''

    r_params = {}

    for k, v in params.items():
        if k in ['xlim','ylim']:
            r_params[k]=ro.FloatVector(v)
        if k in ['xlab','ylab', 'name','low','high','fill','color']:
            r_params[k]=ro.StrVector([v])
        if k=='GRADIENT':
            r_params[k] = ro.BoolVector([v])
        if k=='binwidth':
            r_params[k]=ro.FloatVector([v])

    r_param_list = ro.ListVector(r_params)
    return r_param_list

def scatterplot_params_to_R(params):
    ''' converts params to a properly formatted R-list of the params'''

    r_params = {}

    for k, v in params.items():
        if k in ['xlim','ylim']:
            r_params[k]=ro.FloatVector(v)
        if k in ['xlab','ylab']:
            r_params[k]=ro.StrVector([v])

    r_param_list = ro.ListVector(r_params)
    return r_param_list

def run_funnelplot_analysis(model,
                            included_studies,
                            data_type,
                            metric,
                            data_location,
                            ma_params,
                            funnel_params,
                            fname,
                            res_name = "result",
                            var_name = "tmp_obj",
                            summary=""):
    # also add the metric to the parameters
    # -- this is for scaling
    ma_params["measure"] = METRIC_TO_ESCALC_MEASURE[metric]

    # dispatch on type; build an R object, then run the analysis
    if OMA_CONVENTION[data_type] == "binary":
        make_dataset_r_str = dataset_to_simple_binary_robj(model=model,
                                                  included_studies=included_studies,
                                                  data_location=data_location,
                                                  var_name=var_name)
    elif OMA_CONVENTION[data_type] == "continuous":
        make_dataset_r_str = dataset_to_simple_continuous_robj(model=model,
                                                      included_studies=included_studies,
                                                      data_location=data_location,
                                                      data_type=data_type,
                                                      var_name=var_name)
    # build up funnel parameters
    ma_params_df = ro.DataFrame(ma_params)
    funnel_params_r_str = unpack_r_parameters(prepare_funnel_params_for_R(funnel_params))
    r_str = "%s<-funnel.wrapper('%s',%s,%s, %s)" % (res_name,fname,var_name,ma_params_df.r_repr(),funnel_params_r_str)

    result = exR.execute_in_R(r_str)
    return parse_out_results(result)

def prepare_funnel_params_for_R(params):
    '''Format the results such that they can be used in a call to R without
    any further formatting like adding quotes around strings or whatnot '''

    paramsR = {}

    try:
        paramsR['xlim'] = "c(%f,%f)" % tuple(params['xlim'])
    except KeyError:
        pass
    try:
        paramsR['ylim'] = "c(%f,%f)" % tuple(params['ylim'])
    except KeyError:
        pass
    try:
        paramsR['xlab'] = '"%s"' % params['xlab']
    except KeyError:
        pass
    try:
        paramsR['ylab'] = '"%s"' % params['ylab']
    except KeyError:
        pass
    try:
        paramsR['steps'] = '%d' % params['steps']
    except KeyError:
        pass
    try:
        paramsR['digits'] = '%d' % params['steps']
    except KeyError:
        pass
    try:
        paramsR['addtau2'] = "TRUE" if params['addtau2'] == True else "FALSE"
    except KeyError:
        pass
    try:
        paramsR['refline'] = '%f' % params['refline']
    except KeyError:
        pass

    return paramsR

def unpack_r_parameters(params_dict):
    ''' takes a dictionary of parameters and returns a string suitable for use
    in an r-function call '''

    params_strs = ["%s=%s" % (k,v) for k,v in params_dict.items()]
    return ", ".join(params_strs)



def _to_strs(v):
    return [str(x) for x in v]

def joiner(alist, sep=", ", nchars_per_line=80):
    # same as str.join except will insert a newline every nchars_per_line characters
    # This is to address a stupid issue in R, and by the transitive property, rpy2,
    # whereby if the input to the terminal is very very long, it just won't work without
    # a newline here and there (assumed due to buffering issue)

    result_string = ""
    current_line_length = 0
    last_index = len(alist)-1

    for i,x in enumerate(alist):
        x_length = len(x)

        str_to_add = x
        if i != last_index:
            str_to_add += sep

        potential_line_length = current_line_length + len(str_to_add)
        if current_line_length>0 and potential_line_length >= nchars_per_line:
            result_string += "\n"
            current_line_length=0

        result_string += str_to_add
        current_line_length += len(str_to_add)
    return result_string




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

    if type(value) in NA_types:
        return None
    return value


def transform_effect_size(metric, source_data, direction, conf_level):
    metric_str = METRIC_TO_ESCALC_MEASURE[metric]

    verify_transform_direction(direction)

    # Convert Nones to NAs
    for k in [TRANS_EFFECT, TRANS_VAR, RAW_EFFECT, RAW_LOWER, RAW_UPPER]:
        if k not in source_data:
            continue
        None_to_NA = lambda x: ro.NA_Real if x is None else x
        source_data[k]=[None_to_NA(x) for x in source_data[k]]
    # end convert Nones to NAs

    if direction == TRANS_TO_RAW:
        d = {'yi': ro.FloatVector(source_data[TRANS_EFFECT]),
             'vi': ro.FloatVector(source_data[TRANS_VAR]),
             }
        source_dataf = ro.DataFrame(d)
        r_str = "trans.to.raw(metric='%s', source.data=%s, conf.level=%f)" % (metric_str, source_dataf.r_repr(), conf_level)
    elif direction == RAW_TO_TRANS:
        d = {'yi': ro.FloatVector(source_data[RAW_EFFECT]),
             'lb': ro.FloatVector(source_data[RAW_LOWER]),
             'ub': ro.FloatVector(source_data[RAW_UPPER]),
             }
        source_dataf = ro.DataFrame(d)
        r_str = "raw.to.trans(metric='%s', source.data=%s, conf.level=%f)" % (metric_str, source_dataf.r_repr(), conf_level)

    print("Executing in R: %s" % r_str)
    result = exR.execute_in_R(r_str)
    result = dataframe_to_pydict(result)

    # rekey result
    if direction == RAW_TO_TRANS:
        result = {TRANS_EFFECT:result['yi'],
                  TRANS_VAR:result['vi']}
    elif direction == TRANS_TO_RAW:
        result = {RAW_EFFECT:result['yi'],
                  RAW_LOWER:result['lb'],
                  RAW_UPPER:result['ub']}

    return result





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
        n1i  = [None_to_NA(x, int)   for x in n1i]
        m2i  = [None_to_NA(x, float) for x in m2i]
        sd2i = [None_to_NA(x, float) for x in sd2i]
        n2i  = [None_to_NA(x, int)   for x in n2i]

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

    escalc_result = exR.execute_in_R(r_str)
    result = dataframe_to_pydict(escalc_result) #yi, vi
    return result

def try_n_run(fn):
    ''' tries to run a function (a call to R) and raises an error if it fails'''

    try:
        return fn()
    except Exception as e:
        raise CrazyRError("Some crazy R error occurred", e)



def dataframe_to_pydict(dataframe):
    ''' assumes the columns are named '''

    keys = exR.execute_in_R("names(%s)" % dataframe.r_repr())
    keys = tuple(keys)

    key_value_pairs = [(key, list(dataframe.rx2(key))) for key in keys]
    pydict = dict(key_value_pairs)

    # remove NAs (change to Nones)
    for k, v in pydict.items():
        v = [NA_to_None(x) for x in v]
        pydict[k] = v

    return pydict




def get_available_methods(for_data_type=None, data_obj_name=None, metric=None, funnel_mode=False):
    '''
    Returns a list of methods available in OpenMeta for the particular data_type
    (if one is given). Excludes "*.parameters" methods
    '''

    method_list = exR.execute_in_R("lsf.str('package:openmetar')")


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
                       ".regression", "transform.f", ".pretty.names", ".value.info", "is.feasible.for.funnel"]
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
                is_feasible = exR.execute_in_R("%s(%s, '%s')" % (is_feas_f, data_obj_name, metric))[0]
                if funnel_mode:
                    is_feas_4_funnel_f = "%s.is.feasible.for.funnel" % method
                    is_feasible_for_funnel = exR.execute_in_R("%s()" % (is_feas_4_funnel_f))[0]
                    is_feasible = is_feasible and is_feasible_for_funnel

            if is_feasible:
                # do we have a pretty name?
                pretty_names_f = "%s.pretty.names" % method
                if pretty_names_f in method_list:
                    pretty_name = exR.execute_in_R("%s()$pretty.name" % pretty_names_f)[0]
                    feasible_methods[pretty_name] = method
                else:
                    # no? then just map to the function name
                    feasible_methods[method] = method
    return feasible_methods


def get_params(method_name):
    param_list = exR.execute_in_R("%s.parameters()" % method_name)
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

def get_random_effects_methods_descriptions(method_name):
    pretty_names_and_descriptions = get_params(method_name)[3]
    if 'rm.method' not in pretty_names_and_descriptions:
        raise ValueError("'rm.method' not in pretty_names_and_descriptions")

    return pretty_names_and_descriptions['rm.method']['rm.method.names']


def get_pretty_names_and_descriptions_for_params(method_name, param_list):
    method_list = exR.execute_in_R("lsf.str('package:openmetar')")
    pretty_names_f = "%s.pretty.names" % method_name
    params_d = {}
    if pretty_names_f in method_list:
        # try to match params to their pretty names and descriptions
        pretty_names_and_descriptions = exR.execute_in_R("%s()" % pretty_names_f)
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

def parse_out_results(result, function_name=None, meta_function_name=None):
    # parse out text field(s). note that "plot names" is 'reserved', i.e., it's
    # a special field which is assumed to contain the plot variable names
    # in R (for graphics manipulation).
    text_d = {}
    image_var_name_d, image_params_paths_d, image_path_d  = {}, {}, {}
    image_order = None

    # Turn result into a nice dictionary
    result = dict(zip(list(result.names), list(result)))

    for text_n, text in result.items():
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
        elif text_n == "res":
            # Construct text file with output values
            if 'res.info' in result:
                res_info = result['res.info']
                results_data = extract_additional_values(text, res_info)
        elif text_n == "input_data":
            pass # This is the data that was passed to the analysis function
        elif text_n == "input_params":
            pass # these are the input parameters that were passed to the analysis function
        elif text_n =="res.info":
            pass
        elif text_n =="res.cond.means":
            pass
        elif "gui.ignore" in text_n: # 'gui.ignore' is a directive to the gui to ignore the data
            pass
        elif text_n == "weights":
            text_d[text_n] = make_weights_str(result)

        else:
            if type(text)==rpy2.robjects.vectors.StrVector:
                text_d[text_n] = text[0]
            else:
                text_d[text_n]=str(text)

    to_return = {"images":image_path_d,
                 "image_var_names":image_var_name_d,
                 "texts":text_d,
                 "image_params_paths":image_params_paths_d,
                 "image_order":image_order}
    try:
        to_return["results_data"]=results_data
    except NameError:
        pass

    return to_return

def extract_additional_values(res, res_info, sublist_prefix = "__"):
    # returns a list of tuples:
    #     [('b',{'type':fdfffd, 'description':fdfffd, 'value':%}),
    #       .... ]
    # If the first element of a tuple begins with the sublist_prefix it will be
    # treated as the beginning of a sublist in the results_window (a tree element
    # will be made)

    if _is_grouped_result(res_info):
        subgroup_header_names = list(res_info.names)
        grouped_values_and_value_info = OrderedDict()
        for i,subgroup_name in enumerate(subgroup_header_names):
            j = i+1# R indexes from 1 not 0
            sub_res = res.rx2(j)
            sub_res_info = res_info.rx2(j)
            grouped_values_and_value_info[subgroup_name] = extract_values_for_results_data_single_result(sub_res, sub_res_info)
        #return grouped_values_and_value_info
        flattened_group_output = []
        for subgroup_name, values in grouped_values_and_value_info.items():
            title_tuple = (sublist_prefix+subgroup_name,
                           {'value':'######################################',
                            'type':"label",
                            'description':""})
            flattened_group_output.extend([title_tuple,] + values.items())
        print("extracted grouped values")
        return flattened_group_output
    else:
        additional_values_dict = extract_values_for_results_data_single_result(res, res_info)
        return additional_values_dict.items()

def _is_grouped_result(res_info):
    res_info_keys = list(res_info.names)

    # Is this a grouped result? If so, all the sublists must have 'type' and
    # 'description' keys
    def type_and_description_keys_in_sublist(r_sublist):
        sublist_keys = list(r_sublist.names)
        return 'type' in sublist_keys and 'description' in sublist_keys

    # list of booleans
    type_and_description_present_list = []
    for key in res_info_keys:
        sublist = res_info.rx2(key)
        type_and_description_present = type_and_description_keys_in_sublist(sublist)
        type_and_description_present_list.append(type_and_description_present)
    if all(type_and_description_present_list): # all the sublists have 'type' and 'description'
        grouped_result = False
    else:
        grouped_result = True
    return grouped_result



def extract_values_for_results_data_single_result(res, res_info):
    # Extracts results for a single result (as opposed to result groups as in
    # subgroup analysis)
    # notes: res info is an R list:
    #     res.info <- list('b'=list('type'="vector", description="blahblah"),...)

    # Get info about all the values
    value_info = OrderedDict()
    value_names = list(res_info.names)
    for key in value_names:
        value_info[key]= {'type':res_info.rx2(key).rx2('type')[0],
                          'description':res_info.rx2(key).rx2('description')[0]}
    values_for_csv = OrderedDict([(key, res.rx2(key)) for key in value_names])

    # Convert values to something suitable for printing on the python side
    for k,v in values_for_csv.iteritems():
        if value_info[k]['type'] != 'vector':
            ### Set width large to avoid wrapping
            old_width = ro.r('getOption("width")')[0]
            ro.r('options(width=10000)')
            # get string representtion of object
            values_for_csv[k]=str(v)
            ### Set width back
            ro.r('options(width=%d)' % old_width)
        else:
            try:
                values_for_csv[k]=list(v)
            except TypeError as e: # for cases of TypeError: 'rpy2.rinterface.RNULLType' object is not iterable
                if str(v)=="NULL":
                    values_for_csv[k]="NULL"
                else:
                    raise e

    # Condense value_info and values in to one dictionary to simply the structures and logic
    # e.g. toReturn = {'b':{'type':'vector','description':"pretty vector",'value': 5}
    toReturn = OrderedDict()
    for key in value_names:
        value = values_for_csv[key]
        val_type = value_info[key]['type']
        val_description = value_info[key]['description']
        toReturn[key] = {'value':value, 'type':val_type,'description':val_description}

    return toReturn

def make_weights_str(results):
    ''' Make a string representing the weights due to each study in the meta analysis '''

    # This function assumes that 'weights' and 'input_data' are actually in the results
    if not ("weights" in results and "input_data" in results and "input_params" in results):
        raise Exception("make_weights_str() requires 'weights' and 'input_data' in the results")

    digits = results["input_params"].rx2("digits")[0]
    weights = list(results["weights"])
    weights = ["{0:.{digits}f}%".format(x, digits=digits) for x in weights]
    study_names = list(results["input_data"].do_slot("study.names"))

    table,widths = tabulate([study_names, weights],
                            sep=": ", return_col_widths=True,
                            align=['L','R'])
    header = "{0:<{widths[0]}}  {1:<{widths[1]}}".format("study names", "weights", widths=widths)
    table = "\n".join([header, table]) + "\n"
    return table



def run_binary_ma(function_name, params, res_name="result", bin_data_name="tmp_obj"):
    params_df = ro.r['data.frame'](**params)
    r_str = "%s<-%s(%s, %s)" % (res_name, function_name, bin_data_name,\
                                    params_df.r_repr())
    print "\n\n(run_binary_ma): executing:\n %s\n" % r_str
    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % res_name)
    return parse_out_results(result, function_name=function_name)

def run_continuous_ma(function_name, params, res_name = "result", cont_data_name="tmp_obj"):
    params_df = ro.r['data.frame'](**params)
    r_str = "%s<-%s(%s, %s)" % (res_name, function_name, cont_data_name, params_df.r_repr())
    print "\n\n(run_continuous_ma): executing:\n %s\n" % r_str
    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % res_name)
    return parse_out_results(result, function_name=function_name)

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

    ###print "\n\n(run_meta_method): executing:\n %s\n" % r_str

    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % res_name)

    # parse out text field(s). note that "plot names" is 'reserved', i.e., it's
    # a special field which is assumed to contain the plot variable names
    # in R (for graphics manipulation).
    return parse_out_results(result, function_name=function_name, meta_function_name=meta_function_name)

def run_gmeta_regression(metric,
                         covariates=[],
                         interactions=[],
                         data_name="tmp_obj",
                         fixed_effects = False,
                         random_effects_method="DL",
                         digits=4,
                         conf_level=DEFAULT_CONFIDENCE_LEVEL,
                         btt=None,
                         results_name="results_obj"):

    # Set fixed-effects vs. random effects
    method_str = "FE" if fixed_effects else random_effects_method
    # Get measure i.e. OR etc.
    measure_str = METRIC_TO_ESCALC_MEASURE[metric]

    # Mods is a Listvector (see description in _make_mods_listVector)
    mods = _make_mods_listVector(covariates, interactions)

    # get btt indices for omnibus test of moderators
    choice, choice_type = btt
    btt_indices = get_btt_indices(data=ro.r(data_name),
                                  mods=mods,
                                  choice=choice, choice_type=choice_type)
    if len(btt_indices) > 0:
        btt_indices_vector_str = ro.IntVector(btt_indices).r_repr()
    else:
        btt_indices_vector_str = str(ro.NULL)
    #g.meta.regression <- function(data, mods, method, level, digits, measure, btt=NULL)
    r_str = "{results} <- g.meta.regression(data={data}, mods={mods}, method=\"{method}\", level={level}, digits={digits}, measure=\"{measure}\", btt={btt})".format(
                results=results_name,
                data=data_name,
                mods=mods.r_repr(),
                method=random_effects_method,
                level=conf_level,
                digits=digits,
                measure=measure_str,
                btt=btt_indices_vector_str)

    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % results_name)

    parsed_results = parse_out_results(result)
    return parsed_results

def _make_mods_listVector(covariates, interactions):
    #### Create mods list (model moderators) as specified in g.meta.regression
    ####     on the R side like so:
    # mods: list(numeric=c(...numeric moderators...),
    #            categorical=c(...categorical moderators...),
    #            interactions=list("A:B"=c("A","B"),"B:C"=c("B",C"),...)
    #            )
    # Build numeric moderators string
    sorted_covariates = sort_covariates_by_type(covariates)

    def make_mod_vector(covlist):
        # Per issue #76, R converts the following characters: {' ','-'} to '.',
        # i.e. a period so we must do the same

        return ro.StrVector(["%s" % cov.get_label_R_compatible() for cov in covlist])
    def make_interactions_listVector(interactions):
        # e.g. list("A:B"=c("A","B"),"B:C"=c("B",C"),...)

        string_fragments = []
        for interaction in interactions:
            interaction_str = '"%s"=%s' % (interaction.r_colon_name(), interaction.r_vector_of_covs())
            string_fragments.append(interaction_str)
        r_str = "list(%s)" % ", ".join(string_fragments)
        interaction_listVector = exR.execute_in_R(r_str)
        return interaction_listVector

    numeric_mods_vector = make_mod_vector(sorted_covariates['numeric'])
    cat_mods_vector = make_mod_vector(sorted_covariates['categorical'])
    interactions_listVector = make_interactions_listVector(interactions)

    mods = ro.ListVector({'numeric':numeric_mods_vector,
                          'categorical':cat_mods_vector,
                          'interactions':interactions_listVector})
    #### end of building mods listVector #####
    return mods

def get_btt_indices(data, mods, choice, choice_type):
    # mods is the output of _make_mods_listVector() above
    # choice is a covariate or interaction inside one of the lists of inside of mods
    if choice is None:
        return []
    # Choice as it exists in mods
    choice_R = choice.get_label_R_compatible() if choice_type == "covariate" else choice.r_colon_name()

    #########
    # Take mods and for each element (numeric, categorical, interactions) build
    # an ordered dictionary mapping each cov/interacton to # of generated coefficients
    n_coeffs_odict = OrderedDict([('numeric',     OrderedDict()),
                                  ('categorical', OrderedDict()),
                                  ('interactions',OrderedDict())])
    # count numeric mods
    numeric_mods = list(mods.rx2("numeric"))
    n_coeffs_odict["numeric"]=OrderedDict([(x, 1) for x in numeric_mods])
    # count categorical mods
    categorical_mods = list(mods.rx2("categorical"))
    for cat_mod in categorical_mods:
        levels = data.rx2(cat_mod).levels
        n_coeffs_odict["categorical"][cat_mod] = len(levels) - 1 # minus 1 for the intercept term
    # count interaction mods
    def n_coeffs(cov_name):
        # count number of coeffs that cov_name generates
        if cov_name in n_coeffs_odict['numeric']:
            return n_coeffs_odict['numeric'][cov_name]
        elif cov_name in n_coeffs_odict['categorical']:
            return n_coeffs_odict['categorical'][cov_name]
        else:
            raise Exception("Covariate %s not found" % cov_name)
    interactions_listVector = mods.rx2("interactions")
    if len(interactions_listVector) == 0:
        interaction_names = []
    else:
        interaction_names = interactions_listVector.names
    for inter_name in interaction_names:
        cov1, cov2 = list(interactions_listVector.rx2(inter_name))
        n_coeffs_odict["interactions"][inter_name] = n_coeffs(cov1) * n_coeffs(cov2)
    # counting complete
    ############

    # Find choice_R in n_coeffs_odict, summing along the way to find the indices
    # of interest
    start_less_one = 1 # intercept at index 1
    for main_category in ["numeric", "categorical","interactions"]:
        for coeff_name, num_coefficients in n_coeffs_odict[main_category].items():
            if coeff_name == choice_R:
                start_idx = start_less_one+1
                last_idx = start_idx + num_coefficients-1
                return range(start_idx, last_idx+1)
            else:
                start_less_one += num_coefficients

    raise Exception("Should've finished before now")







def run_gmeta_regression_cond_means(selected_cov, covs_to_values,
                         covariates=[],
                         interactions=[],
                         data_name="tmp_obj",
                         fixed_effects = False,
                         random_effects_method="DL",
                         digits=4,
                         conf_level=DEFAULT_CONFIDENCE_LEVEL,
                         btt=None,
                         results_name="results_obj"):

    # Set fixed-effects vs. random effects
    method_str = "FE" if fixed_effects else random_effects_method

    # Mods is a Listvector (see description in _make_mods_listVector)
    mods = _make_mods_listVector(covariates, interactions)

    # get btt indices for omnibus test of moderators
    choice, choice_type = btt
    btt_indices = get_btt_indices(data=ro.r(data_name),
                                  mods=mods,
                                  choice=choice, choice_type=choice_type)
    if len(btt_indices) > 0:
        btt_indices_vector_str = ro.IntVector(btt_indices).r_repr()
    else:
        btt_indices_vector_str = str(ro.NULL)



    cond_data = _make_conditional_data_listVector(covs_to_values)

    r_str = "{results} <- g.meta.regression.cond.means(data={data},   \
    mods={mods}, method=\"{method}\", level={level}, digits={digits}, \
    strat.cov=\"{strat_cov}\", cond.means.data={cond_means_data}, btt={btt})".format(
                results=results_name, data=data_name, mods=mods.r_repr(),
                method=random_effects_method, level=conf_level, digits=digits,
                strat_cov=selected_cov.get_label(),
                cond_means_data=cond_data.r_repr(), btt=btt_indices_vector_str)

    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % results_name)

    parsed_results = parse_out_results(result)
    return parsed_results

def _make_conditional_data_listVector(covs_to_values):
    cov_names_to_values = {}
    for cov, value in covs_to_values.iteritems():
        cov_names_to_values[cov.get_label()] = value

    cdata = ro.ListVector(cov_names_to_values)
    return cdata

def run_gmeta_regression_bootstrapped(
                         num_replicates,
                         covariates=[],
                         interactions=[],
                         data_name="tmp_obj",
                         fixed_effects = False,
                         random_effects_method="DL",
                         digits=4,
                         histogram_title="",
                         conf_level=DEFAULT_CONFIDENCE_LEVEL,
                         btt=None,
                         results_name="results_obj"):

    # TODO: Set this to be some timestamped file path later?
    # save bootstrap outout data on R side for 'save-as png + pdf functions'
    bootstrap_plot_path = "./r_tmp/bootstrap.png"

    # Set fixed-effects vs. random effects
    method_str = "FE" if fixed_effects else random_effects_method

    # Mods is a Listvector (see description in _make_mods_listVector)
    mods = _make_mods_listVector(covariates, interactions)

    r_str = "{results} <- g.bootstrap.meta.regression(data={data}, mods={mods}, \
method=\"{method}\", level={level}, digits={digits}, \
n.replicates={num_replicates}, histogram.title=\"{histogram_title}\", \
bootstrap.plot.path=\"{bootstrap_plot_path}\")".format(
                results=results_name, data=data_name, mods=mods.r_repr(),
                method=random_effects_method, level=conf_level, digits=digits,
                num_replicates=num_replicates, histogram_title=histogram_title,
                bootstrap_plot_path=bootstrap_plot_path)

    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % results_name)

    parsed_results = parse_out_results(result)
    return parsed_results

def run_gmeta_regression_bootstrapped_cond_means(selected_cov, covs_to_values,
                         num_replicates,
                         covariates=[],
                         interactions=[],
                         data_name="tmp_obj",
                         fixed_effects = False,
                         random_effects_method="DL",
                         digits=4,
                         histogram_title="",
                         conf_level=DEFAULT_CONFIDENCE_LEVEL,
                         btt=None,
                         results_name="results_obj"):

    # TODO: Set this to be some timestamped file path later?
    # save bootstrap outout data on R side for 'save-as png + pdf functions'
    bootstrap_plot_path = "./r_tmp/bootstrap.png"

    # Set fixed-effects vs. random effects
    method_str = "FE" if fixed_effects else random_effects_method

    # Mods is a Listvector (see description in _make_mods_listVector)
    mods = _make_mods_listVector(covariates, interactions)
    cond_data = _make_conditional_data_listVector(covs_to_values)

    r_str = "{results} <- g.bootstrap.meta.regression.cond.means(data={data}, mods={mods}, \
method=\"{method}\", level={level}, digits={digits}, \
n.replicates={num_replicates}, histogram.title=\"{histogram_title}\", \
bootstrap.plot.path=\"{bootstrap_plot_path}\", strat.cov=\"{strat_cov}\", \
cond.means.data={cond_means_data})".format(
                results=results_name, data=data_name, mods=mods.r_repr(),
                method=random_effects_method, level=conf_level, digits=digits,
                num_replicates=num_replicates, histogram_title=histogram_title,
                bootstrap_plot_path=bootstrap_plot_path,
                strat_cov=selected_cov.get_label(),
                cond_means_data=cond_data.r_repr())

    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % results_name)

    parsed_results = parse_out_results(result)
    return parsed_results


def run_meta_regression(metric, fixed_effects=False, data_name="tmp_obj",
                        results_name="results_obj",
                        conf_level=DEFAULT_CONFIDENCE_LEVEL,
                        random_effects_method = "DL",
                        selected_cov=None, covs_to_values = None):  # for meta-reg cond means

    if conf_level is None:
        raise ValueError("Confidence level must be specified")

    # Set fixed-effects vs. random effects
    method_str = "FE" if fixed_effects else random_effects_method

    # TODO: digits should be user-specified
    params = {"conf.level": conf_level,
              "digits": 3,
              #"method": method_str,
              "rm.method": method_str, #"ML",
              "measure": METRIC_TO_ESCALC_MEASURE[metric]}
    params_df = ro.r['data.frame'](**params)


    if (selected_cov, covs_to_values) != (None, None):
        meta_reg_d = {'chosen.cov.name':selected_cov.get_label()}
        for cov, value in covs_to_values.items():
            meta_reg_d[cov.get_label()]=value

        r_str = "%s<- meta.regression(%s, %s, %s)" % \
                    (results_name, data_name, str(params_df.r_repr()), ro.DataFrame(meta_reg_d).r_repr())
    else:
        # create a list of covariate objects on the R side
        r_str = "%s<- meta.regression(%s, %s)" % \
                                (results_name, data_name, str(params_df.r_repr()))


    #print "\n\n(run_meta_regression): executing:\n %s\n" % r_str
    ### TODO -- this is hacky
    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % results_name)

    if "try-error" in str(result):
        # uh-oh, there was an error (but the weird
        # RRunTimeError alluded to above; this is a
        # legit error returned from an R routine)
        return str([msg for msg in result][0])


    parsed_results = parse_out_results(result)

    return parsed_results


def run_bootstrap_meta_regression(metric,
                                  fixed_effects=False,
                                  data_name="tmp_obj",
                                  results_name="results_obj",
                                  conf_level=DEFAULT_CONFIDENCE_LEVEL,
                                  random_effects_method = "DL",
                                  selected_cov=None, covs_to_values = None,
                                  data_type="binary",
                                  bootstrap_params={}):

    # Set fixed-effects vs. random effects
    method_str = "FE" if fixed_effects else random_effects_method

    params = {"conf.level": conf_level,
              "digits": 3,
              "rm.method": method_str, #"ML",
              "measure": METRIC_TO_ESCALC_MEASURE[metric],
              }
    params.update(bootstrap_params)
    params_df = ro.r['data.frame'](**params)

#    if (selected_cov, covs_to_values) != (None, None):
#        meta_reg_d = {'chosen.cov.name':selected_cov.get_label()}
#        for cov, value in covs_to_values.items():
#            meta_reg_d[cov.get_label()]=value
#
#        r_str = "%s<- meta.regression(%s, %s, %s)" % \
#                    (results_name, data_name, str(params_df.r_repr()), ro.DataFrame(meta_reg_d).r_repr())
#    else:
#        r_str = "%s<- meta.regression(%s, %s)" % \
#                                (results_name, data_name, str(params_df.r_repr()))


    if (selected_cov, covs_to_values) != (None, None):
        meta_reg_d = {'chosen.cov.name':selected_cov.get_label()}
        for cov, value in covs_to_values.items():
            meta_reg_d[cov.get_label()]=value

        r_str = "%s<-bootstrap(%s, %s, %s, %s)" % (results_name, "'boeuf'", data_name, str(params_df.r_repr()), str(ro.DataFrame(meta_reg_d).r_repr()))
    else:
        r_str = "%s<-bootstrap(%s, %s, %s)" % (results_name, "'boeuf'", data_name, str(params_df.r_repr()))

    #print "\n\n(run_meta_regression): executing:\n %s\n" % r_str
    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % results_name)

    if "try-error" in str(result):
        # uh-oh, there was an error (but the weird
        # RRunTimeError alluded to above; this is a
        # legit error returned from an R routine)
        return str([msg for msg in result][0])

    parsed_results = parse_out_results(result)
    return parsed_results

def get_method_description(method_name):
    pretty_names_f = "%s.pretty.names" % method_name
    method_list = exR.execute_in_R("lsf.str('package:openmetar')")
    description = "None provided."
    if pretty_names_f in method_list:
        try:
            description = exR.execute_in_R("%s()$description" % pretty_names_f)[0]
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
            #simple: if True, the data doesn't get messed with at all, otherwise singletons are converted to scalars

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
            return exR.execute_in_R("as.character(%s)" % singleton_list.r_repr())[0]

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

def load_vars_for_plot(params_path, return_params_dict=False, var_suffixes=("data", "params", "res")):
    '''
    loads the three necessary (for plot generation) variables
    into R. we assume a naming convention in which params_path
    is the base, data is stored in *.data, params in *.params
    and result in *.res.
    '''
    for var in var_suffixes:
        cur_path = "%s.%s" % (params_path, var)
        if os.path.exists(cur_path):
            load_in_R(cur_path)
            print "loaded %s" % cur_path
        else:
            print "whoops -- couldn't load %s" % cur_path
            return False

    if return_params_dict:
        robj = exR.execute_in_R("params")
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
    data_type = str(exR.execute_in_R("class(%s)" % om_data_name))

    if "BinaryData" in data_type:
        r_str = "plot.data<-create.plot.data.binary(%s, %s, %s)" % \
                        (om_data_name, plot_params_name, res_name)
        exR.execute_in_R(r_str)

    elif "ContinuousData" in data_type:
        r_str = "plot.data<-create.plot.data.continuous(%s, %s, %s)" % \
                            (om_data_name, plot_params_name, res_name)
        exR.execute_in_R(r_str)
    elif "DiagnosticData" in data_type:
        r_str = "plot.data<-create.plot.data.diagnostic(%s, %s, %s)" % \
                            (om_data_name, plot_params_name, res_name)
        exR.execute_in_R(r_str)

    print("executed: %s" % r_str)

def update_plot_params(plot_params, plot_params_name="params", \
                        write_them_out=False, outpath=None):
    # first cast the params to an R data frame to make it
    # R-palatable
    params_df = ro.r['data.frame'](**plot_params)
    exR.execute_in_R("tmp.params <- %s" % params_df.r_repr())

    for param_name in plot_params:
        r_str = "%s$%s <- tmp.params$%s" % (plot_params_name, param_name, param_name)
        exR.execute_in_R(r_str)

    if write_them_out:
        exR.execute_in_R("save(tmp.params, file='%s')" % outpath)

def write_out_plot_data(params_out_path, plot_data_name="plot.data"):
    exR.execute_in_R("save.plot.data(%s, '%s')" % (plot_data_name, params_out_path))

    #save.plot.data.and.params

######### DEAL WITH COVARIATES #########

def list_of_cov_value_objects_str(studies, cov_list=[], cov_to_ref_var={}):
    ''' makes r_string of covariate objects with their values '''

    r_cov_str = []
    for cov in cov_list:
        ref_var = None
        if cov in cov_to_ref_var:
            ref_var = cov_to_ref_var[cov]
        ref_var_as_string = str(ref_var) if ref_var is not None else None
        r_cov_str.append(_gen_cov_vals_obj_str(cov, studies, ref_var_as_string))
    r_cov_str = "list(" + ",".join(r_cov_str) + ")"

    return r_cov_str


def _gen_cov_vals_obj_str(cov, studies, ref_var=None):
    ''' makes an R-evalable string to generate a covariate in R'''

    values_str, cov_vals = cov_to_str(cov, studies, named_list=False, return_cov_vals=True)
    if ref_var is None: # just take the first value if unspecified
        ref_var = cov_vals[0].replace("'", "") # arbitrary, get rid of single quotes
        ref_var = cov_vals[0].replace('"', '') # get rid if double quotes too

    ## setting the reference variable to the first entry
    # for now -- this only matters for factors, obviously

    r_str = "new('CovariateValues', cov.name='%s', cov.vals=%s, cov.type='%s', ref.var='%s')" % \
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
        if cov_type == CONTINUOUS or cov_type==COUNT:
            if value is None:
                return "NA"
            else:
                return "%s" % str(value)
        elif cov_type == CATEGORICAL:
            if value is None:
                return "NA"
            else:
                return '"%s"' % unicode(str(value).encode('latin1'), 'latin1')
        else:
            raise Exception("Unrecognized covariate type")


    cov_values = [study.get_var(cov) for study in studies]
    cov_values = [convert_cov_value(cov.get_type(), value) for value in cov_values]

    cov_str += joiner(cov_values) + ")"

    if return_cov_vals:
        return (cov_str, cov_values)
    return cov_str

##################### END OF COVARIATE STUFF #################################

def get_funnel_params(params_path):
    '''gets the values in the 'r_tmp/{params_path}.funnel.params' object stored
    for a plot where {params path} is the timestamp path.
    Will return the parameters in 'python' mode i.e. lists are list not strings
    that look like e.g. "c(1,2,3,4)" '''

    r_str = 'get.funnel.params("%s")' % params_path
    params = exR.execute_in_R(r_str)
    params_pyfmt = R_parse_tools.recursioner(params)
    print("The funnel parameters in python format are: %s" % params_pyfmt)
    return params_pyfmt

def get_exploratory_params(params_path, plot_type=None):
    ''' gets the stored params from r_tmp from R for histograms and scatterplots
    and puts them into 'python' mode '''

    r_str = 'get.exploratory.params("%s")' % params_path
    params = exR.execute_in_R(r_str)
    params_pyfmt = R_parse_tools.recursioner(params)
    print("The parameters in python format are: %s" % params_pyfmt)
    return params_pyfmt


def run_model_building(model_info,
                       data_name="tmp_obj",
                       fixed_effects = False,
                       random_effects_method="DL",
                       digits=4,
                       conf_level=DEFAULT_CONFIDENCE_LEVEL,
                       results_name="results_obj"):

    # Set fixed-effects vs. random effects
    method_str = "FE" if fixed_effects else random_effects_method

    full_model_info = model_info[0]
    reduced_model_info = model_info[1]

    # Mods is a Listvector (see description in _make_mods_listVector)
    mods_full = _make_mods_listVector(full_model_info['covariates'], full_model_info['interactions'])
    mods_reduced = _make_mods_listVector(reduced_model_info['covariates'], reduced_model_info['interactions'])

    r_str = "{results} <- model.building(data={data}, full.mods={full_mods}, reduced.mods={reduced_mods}, method=\"{method}\", level={level}, digits={digits})".format(
                results=results_name, data=data_name, full_mods=mods_full.r_repr(), reduced_mods=mods_reduced.r_repr(),
                method=random_effects_method, level=conf_level, digits=digits)

    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % results_name)

    parsed_results = parse_out_results(result)
    return parsed_results

def run_phylo_ma(tree, evo_model, random_effects_method, lambda_, alpha,
                 include_species, plot_params,
                 data_name="tmp_obj",
                 fixed_effects = False,
                 digits=4,
                 conf_level=DEFAULT_CONFIDENCE_LEVEL,
                 results_name="results_obj"):

    # Set fixed-effects vs. random effects
    method_str = "FE" if fixed_effects else random_effects_method

    plot_params_df = ro.r['data.frame'](**plot_params)


# phylo.meta.analysis <- function(tree, evo.model,
#                                 data, method, level, digits, plot.params, metric,
#                                 btt=NULL,
#                                 lambda=1.0, alpha=1.0, include.species=TRUE)


    r_str = "{results} <- phylo.meta.analysis(tree={tree}, evo.model=\"{evo_model}\", \
data={data}, method=\"{method}\", level={level}, digits={digits}, btt=NULL, \
lambda={lambda_}, alpha={alpha}, include.species={include_species}, plot.params={plot_params})".format(
        results=results_name,
        tree=tree.r_repr(), evo_model=evo_model, data=data_name,
        method=method_str, digits=digits, lambda_=lambda_,
        alpha=alpha, level=conf_level,
        include_species="TRUE" if include_species else "FALSE",
        plot_params=plot_params_df.r_repr())


    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % results_name)

    parsed_results = parse_out_results(result)
    return parsed_results




def covariates_to_dataframe(model, studies, covariates):
    # This is for imputation using mice. We create an R dataframe of the portion
    # of the dataset of interest suitable for sending on to mice.
    # Categorical variables in the dataframe are converted to factors. Missing
    # data will be left out of the factor levels
    #
    # Creates the dataframe with covariates in the same order that they were
    # provided

    # Gathers values of the variable from amongst the included studies
    #var_values = lambda x: [study.get_var(x) for study in studies]

    def var_values(cov, NA_type):
        values = [study.get_var(cov) for study in studies]
        values = [None_to_NA(x, NA_type) for x in values] # convert None to R NA of the appropriate variety
        return values


    # Covariates sorted into 'int', 'continuous', and 'factor' categories
    sorted_covariates = sort_covariates_by_type(covariates, sort_method=INT_CONTINUOUS_FACTOR)

    # Convert covariates to R representation
    cov_to_FloatVector = lambda cov: ro.FloatVector(var_values(cov, float))
    cov_to_FactorVector= lambda cov: ro.FactorVector(var_values(cov, str))
    cov_to_IntVector   = lambda cov: ro.IntVector(var_values(cov, int))

    int_covs  = dict([(cov,cov_to_IntVector(cov))    for cov in sorted_covariates['int']])
    cont_covs = dict([(cov,cov_to_FloatVector(cov))  for cov in sorted_covariates['continuous']])
    cat_covs  = dict([(cov,cov_to_FactorVector(cov)) for cov in sorted_covariates['factor']])

    # mapping covs --> R vectors
    covs_to_Rvectors = {}
    covs_to_Rvectors.update(int_covs)
    covs_to_Rvectors.update(cont_covs)
    covs_to_Rvectors.update(cat_covs)

    # maintain order of covariates
    ordered_init_dict = rlc.OrdDict([(cov.get_label(), covs_to_Rvectors[cov]) for cov in covariates])

    dataf = ro.DataFrame(ordered_init_dict)
    return dataf


def dataframe_to_ordered_dict(dataframe, covariates):
    # converts a dataframe with .names attribute corresponding to 'covariates'
    # to an Ordered dict mapping covariates --> values

    def vector_to_values(vector):
        # determine class of vector
        # convert it back to a suitable python representation
        # NAs converted to None

        if type(vector) in [ro.IntVector, ro.FloatVector, ro.StrVector]:
            values = list(vector)
            values = [NA_to_None(val) for val in values]
            return values
        elif isinstance(vector, ro.FactorVector):
            values = list(list(base.as_character(vector)))
            values = [NA_to_None(val) for val in values]
            return values
        else:
            raise Exception("This type is unrecognizes: %s" % str(type(vector)))

    print("Covariates: %s" % [cov.get_label() for cov in covariates])
    # pyish_df is an OrderedDict mapping the covariates to their imputed
    # values.
    pyish_df = OrderedDict()
    # Build up the choice
    print("Names in imputed df: %s" % list(dataframe.names))
    for i,cov in enumerate(covariates):
        pyish_df[cov] = vector_to_values(dataframe[i])
    return pyish_df

def imputation_dataframes_to_pylist_of_ordered_dicts(imputations_list, covariates):
    # 'imputations_list' is an R-list of imputations(data frames) with the order
    # of covariates given in by the order of 'covariates'
    # Converts the R list of dataframes to a python list of ordered dicts
    #   with the order given by the order of covs in 'covariates'

    imputation_choices = [dataframe_to_ordered_dict(df, covariates) for df in imputations_list]
    return imputation_choices

def impute(model, studies, covariates, m, maxit, defaultMethod_rstring, input_df_name="mice.source.df"):
    '''
    Here is a start at issue #86
    '''
    # @TODO
    # add pop-up, and possibly (probably?) a small wizard
    # that tells the user what we're doing here and assumptions
    # that are being made. the thinking is that we'll just use
    # mice 'out of the box'. it seems like it's relatively
    # straight forward to select different imputation methods
    # for each variable column, so we may want to allow the user
    # to do this eventually
    #
    # See MICE: Multivariate Imputation by Chained Equations in R
    # http://www.stefvanbuuren.nl/publications/MICE%20in%20R%20-%20Draft.pdf
    # Also: http://cran.r-project.org/web/packages/mice/index.html
    ####

    # convert to a data frame
    data_f = covariates_to_dataframe(model, studies, covariates)

    # Also store the df as a python ordered dictionary for the purposes of seeing
    # which values were None
    source_data = dataframe_to_ordered_dict(data_f, covariates)

    # put dataframe in to R workspace
    exR.execute_in_R("%s<-%s" % (input_df_name, data_f.r_repr()))

    mice_r_str = rstr_for_rfn("impute", data=input_df_name, m=m, maxit=maxit, defaultMethod=defaultMethod_rstring)
    mice_result = exR.execute_in_R(mice_r_str)

    # parse out result
    toReturn = dict(summary = mice_result.rx2('Summary')[0],
                    imputations = mice_result.rx2('imputations'),
                    source_data = source_data
                    )
    return toReturn

def rstr_for_rfn(fname, **kargs):
    # Takes an R function name and keyword arguments and builds the function
    # call string suitable for then calling with exR.execute_in_R()
    keyword_argument_substrs = ["{k}={v}".format(k=key,v=val) for key,val in kargs.iteritems()]
    r_str = fname + "(" + ", ".join(keyword_argument_substrs) + ")"
    return r_str


def make_imputed_datasets(original_dataset,
                          imputations,
                          imputed_datasets_name="imputed.datasets"):
    # Makes R list of datasets with imputated values and put it in the R
    # workspace as imputed_datasets_name
    # original dataset is a dataframe
    # imputations is a list of dataframes containing imputed values
    r_str = "combine.imputations.with.dataset(%s, %s)" % (original_dataset.r_repr(), imputations.r_repr())
    imputed_datasets = exR.execute_in_R(r_str)
    r_str = "%s <- %s" % (imputed_datasets_name, imputed_datasets.r_repr())
    exR.execute_in_R(r_str)
    return imputed_datasets


# Runs a meta analysis/regression depending on whether covariates are chosen
# or not
def run_multiple_imputation_meta_analysis(ma_params,
                                          covariates=[],
                                          interactions=[],
                                          imputed_datasets_name="tmp_obj",
                                          results_name="results_obj"):

    # build ma_params
    params = params_dict_to_Robject(ma_params, "list")

    # Mods is a Listvector (see description in _make_mods_listVector)
    mods = _make_mods_listVector(covariates, interactions)

    r_str = "{results} <- multiply.imputed.meta.analysis(imputed.datasets={data}, mods={mods}, rma.args={params})".format(
                results=results_name,
                data=imputed_datasets_name,
                mods=mods.r_repr(),
                params = params.r_repr())

    exR.execute_in_R(r_str)
    result = exR.execute_in_R("%s" % results_name)

    parsed_results = parse_out_results(result)
    return parsed_results

def params_dict_to_Robject(params, robject_type ="list"):
    # Builds an R object (either a "list" or "dataframe") corresponding to the
    # params dict.
    # each param should be a scalar value

    if robject_type == "list":
        robj = ro.ListVector(params)
    elif robject_type == "dataframe":
        robj = ro.DataFrame(params)
    else:
        raise Exception("robject type is incorrect ")

    return robj
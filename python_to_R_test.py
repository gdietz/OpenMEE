import python_to_R


import unittest
import ome_globals
import os.path


# RExecutor:
#     def __init__(self):
#     def set_R_log_dialog(self, dialog):
#     def unset_R_log_dialog(self):
#     def execute_in_R(self, r_str, show_output=False, reset_wd=True):

# RlibLoader:
#     def __init__(self):
#     def load_ape(self):
#     def load_grid(self):
#     def load_igraph(self):
#     def load_metafor(self):
#     def load_mice(self):
#     def load_openmeer(self):
#     def load_openmetar(self):
#     def load_rmeta(self):
#     def _load_r_lib(self, name):
#     def load_all_libraries(self):

# R parse tools:
#     def __init__(self):
#     def rlist_to_pydict(named_r_list):
#     def recursioner(data):
#     def R_iterable_to_pylist(r_iterable):
#         def filter_list_element(x):
#     def _singleton_list_to_scalar(singleton_list):
#     def _convert_NA_to_None(scalar):
#     def _isListable(element, exclude_strings=True):
#     def haskeys(r_object):


def SetupForAllTests():
    # setup r_tmp and working directory
    python_to_R.setup_directories()

    rloader = python_to_R.RlibLoader()
    rloader.load_metafor()
    rloader.load_openmetar()
    rloader.load_openmeer()
    rloader.load_igraph()
    rloader.load_grid()
    rloader.load_ape()
    rloader.load_mice()

SetupForAllTests()

class TestXMethods(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

class TestUtilityMthods(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_load_ape_file(self):
        '''
        TODO: need an ape file to test with
        '''
        pass

    def test_reset_Rs_working_dir(self):
        '''
        TODO: Implement later
        '''
        pass

class TestSetConfidenceLevelinR(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # rest conf level 
        r_str = "set.global.conf.level(%s)" % ome_globals.DEFAULT_CONFIDENCE_LEVEL
        python_to_R.exR.execute_in_R(r_str)

    def test_set_conf_level_in_R(self):
        new_conf_level = python_to_R.set_conf_level_in_R(80)
        self.assertEqual(new_conf_level, 80)

class TestBinaryMetaAnalysis(unittest.TestCase):
    def setUp(self):
        python_to_R.set_conf_level_in_R(95)

        r_str = '''
            tmp_obj <- new(
                'BinaryData',
                g1O1=c(32, 119, 46, 32, 22, 28, 52, 99),
                g1O2=c(24, 32, 109, 42, 51, 19, 117, 102),
                g2O1=c(54, 82, 111, 125, 109, 63, 6, 83),
                g2O2=c(125, 29, 9, 64, 49, 74, 120, 32),
                y=c(
                    1.12701176319,
                    0.273964173034,
                    -3.37501210972,
                    -0.941364369426,
                    -1.64031076348,
                    0.548695897821,
                    2.18480205734,
                    -0.982957668147
                ),
                SE=c(
                    0.315333450787,
                    0.29382178598,
                    0.388630367421,
                    0.280507618095,
                    0.307644053711,
                    0.343121544133,
                    0.450308536204,
                    0.251402315902
                ),
                study.names=c(
                    "Storm",
                    "Rogue",
                    "Wolverine",
                    "Gambit",
                    "Spiderman",
                    "Mr. Fantastic",
                    "The Flash",
                    "Thor"
                ),
                years=c(
                    as.integer(),
                    as.integer(),
                    as.integer(),
                    as.integer(),
                    as.integer(),
                    as.integer(),
                    as.integer(),
                    as.integer()
                ),
                covariates=list()
            )
        '''
        python_to_R.exR.execute_in_R(r_str)

    def test_run_binary_ma(self):
        # run_binary_ma() parameters:
        function_name = 'binary.random'
        params = {
            'conf.level': 95.0,
            'digits': 3,
            'fp_col2_str': u'[default]',
            'fp_show_col4': True,
            'to': 'only0',
            'fp_col4_str': u'Ev/Ctrl',
            'fp_xticks': '[default]',
            'fp_col3_str': u'Ev/Trt',
            'fp_show_col3': True,
            'fp_show_col2': True,
            'fp_show_col1': True,
            'fp_plot_lb': '[default]',
            'fp_outpath': u'./r_tmp/forest.png',
            'rm.method': 'DL',
            'adjust': 0.5,
            'fp_plot_ub': '[default]',
            'fp_col1_str': u'Studies',
            'measure': 'OR',
            'fp_xlabel': u'[default]',
            'fp_show_summary_line': True,
        }
        res_name = 'result'
        bin_data_name = 'tmp_obj'

        # expected result
        full_expected_result = {
            'image_order': None,
            'image_var_names': {
                'Forest Plot': 'r_tmp/1459137190.84989',
            },
            'save_plot_functions': {},
            'texts': {
                'References': '1. this is a placeholder for binary random reference\n2. metafor: Viechtbauer, Wolfgang. "Conducting meta-analyses in R with the metafor package." Journal of 36 (2010).\n3. OpenMetaAnalyst: Wallace, Byron C., Issa J. Dahabreh, Thomas A. Trikalinos, Joseph Lau, Paul Trow, and Christopher H. Schmid. "Closing the Gap between Methodologists and End-Users: R as a Computational Back-End." Journal of Statistical Software 49 (2012): 5."\n',
            'weights': 'study names    weights\nStorm        : 12.565%\nRogue        : 12.641%\nWolverine    : 12.277%\nGambit       : 12.685%\nSpiderman    : 12.593%\nMr. Fantastic: 12.462%\nThe Flash    : 12.000%\nThor         : 12.776%\n',
            'Summary': 'Binary Random-Effects Model\n\nMetric: Odds Ratio\n\n Model Results\n\n Estimate  Lower bound   Upper bound   p-Value  \n\n 0.698        0.249         1.955       0.494   \n\n\n Heterogeneity\n\n tau^2  Q(df=7)   Het. p-Value    I^2    \n\n 2.096  152.959     < 0.001      95.424  \n\n\n Results (log scale)\n\n Estimate  Lower bound   Upper bound   Std. error  \n\n -0.359      -1.388         0.670         0.525    \n\n'},
            'image_params_paths': {},
            'results_data': [
                ('b', {'type': 'vector', 'description': 'estimated coefficients of the model.', 'value': [-0.35910271701829777]}),
                ('se', {'type': 'vector', 'description': 'standard errors of the coefficients.', 'value': [0.5251713828737001]}),
                ('zval', {'type': 'vector', 'description': 'test statistics of the coefficients.', 'value': [-0.6837819590498505]}),
                ('pval', {'type': 'vector', 'description': 'p-values for the test statistics.', 'value': [0.49411286038331276]}),
                ('ci.lb', {'type': 'vector', 'description': 'lower bound of the confidence intervals for the coefficients.', 'value': [-1.3884197131618454]}),
                ('ci.ub', {'type': 'vector', 'description': 'upper bound of the confidence intervals for the coefficients.', 'value': [0.6702142791252498]}),
                ('vb', {'type': 'vector', 'description': 'variance-covariance matrix of the estimated coefficients.', 'value': [0.27580498138947457]}),
                ('tau2', {'type': 'vector', 'description': 'estimated amount of (residual) heterogeneity. Always 0 when method="FE".', 'value': [2.095509444028601]}),
                ('se.tau2', {'type': 'vector', 'description': 'estimated standard error of the estimated amount of (residual) heterogeneity.', 'value': [1.2212968160381423]}),
                ('k', {'type': 'vector', 'description': 'number of outcomes included in the model fitting.', 'value': [8]}),
                ('p', {'type': 'vector', 'description': 'number of coefficients in the model (including the intercept).', 'value': [1]}),
                ('m', {'type': 'vector', 'description': 'number of coefficients included in the omnibus test of coefficients.', 'value': [1]}),
                ('QE', {'type': 'vector', 'description': 'test statistic for the test of (residual) heterogeneity.', 'value': [152.9594285526956]}),
                ('QEp', {'type': 'vector', 'description': 'p-value for the test of (residual) heterogeneity.', 'value': [9.700902393814967e-30]}),
                ('QM', {'type': 'vector', 'description': 'test statistic for the omnibus test of coefficients.', 'value': [0.4675577675220514]}),
                ('QMp', {'type': 'vector', 'description': 'p-value for the omnibus test of coefficients.', 'value': [0.49411286038331265]}),
                ('I2', {'type': 'vector', 'description': 'value of I2. See print.rma.uni for more details.', 'value': [95.42362307035656]}),
                ('H2', {'type': 'vector', 'description': 'value of H2. See print.rma.uni for more details.', 'value': [21.851346936099375]}),
                ('R2', {'type': 'vector', 'description': 'value of R2. See print.rma.uni for more details.', 'value': 'NULL'}),
                ('int.only', {'type': 'vector', 'description': 'logical that indicates whether the model is an intercept-only model.', 'value': [True]}),
                ('yi', {'type': 'vector', 'description': 'the vector of outcomes', 'value': [1.12701176319, 0.273964173034, -3.37501210972, -0.941364369426, -1.64031076348, 0.548695897821, 2.18480205734, -0.982957668147]}),
                ('vi', {'type': 'vector', 'description': 'the corresponding sample variances', 'value': [0.09943518518523733, 0.08633124191647694, 0.15103356248178146, 0.07868452380933039, 0.09464486378373665, 0.11773239404821427, 0.2027777777781892, 0.063203124440889]}),
                ('X', {'type': 'matrix', 'description': 'the model matrix of the model', 'value': '     intrcpt\n[1,]       1\n[2,]       1\n[3,]       1\n[4,]       1\n[5,]       1\n[6,]       1\n[7,]       1\n[8,]       1\n'}),
                ('fit.stats', {'type': 'data.frame', 'description': 'a list with the log-likelihood, deviance, AIC, BIC, and AICc values under the unrestricted and restricted likelihood.', 'value': '            ML      REML\nll   -15.27398 -13.95936\ndev   33.88934  27.91871\nAIC   34.54797  31.91871\nBIC   34.70685  31.81053\nAICc  36.94797  34.91871\n'}),
                ('weights', {'type': 'vector', 'description': 'weights in % given to the observed effects', 'value': [12.56546419069621, 12.640931263503685, 12.27686185353247, 12.685389871803455, 12.592947465193252, 12.461583575933748, 12.00045750472613, 12.776364274611055]})
            ],
            'images': {'Forest Plot': './r_tmp/forest.png'},
        }

        # calculate result
        result = python_to_R.run_binary_ma(
            function_name,
            params,
            res_name=res_name,
            bin_data_name=bin_data_name,
        )
        b_row = result['results_data'][0]
        b_value = b_row[1]['value']

        expected_b_row = full_expected_result['results_data'][0]
        expected_b_value = expected_b_row[1]['value']

        self.assertEqual(b_value, expected_b_value)

# TODO: FUNCTIONS THAT WE STILL NEED TO WRITE UNIT TESTS FOR

# def run_bootstrap_meta_regression(
# def run_continuous_ma(
# def run_dynamic_data_exploration_analysis(
# def run_failsafe_analysis(
# def run_funnelplot_analysis(
# def run_gmeta_regression(
# def run_gmeta_regression_bootstrapped(
# def run_gmeta_regression_bootstrapped_cond_means(
# def run_gmeta_regression_cond_means(
# def run_histogram(
# def run_meta_method(
# def run_meta_regression(
# def run_model_building(
# def run_multiple_imputation_meta_analysis(
# def run_permutation_analysis(
# def run_phylo_ma(
# def run_scatterplot(

# def _gen_cov_vals_obj_str(cov, studies, ref_var=None):
# def _is_grouped_result(res_info):
# def _make_conditional_data_listVector(covs_to_values):
# def _make_mods_listVector(covariates, interactions):
# def _sanitize_for_R(a_str):
# def _to_strs(v):
# def bool_to_rstr(x):
# def calculate_bounds(yi, vi, conf_level):
# def col_data_to_R_fmt(col_data, data_type):
# def cols_to_data_frame(model):
# def cov_to_str(cov, studies, named_list=True, return_cov_vals=False):
# def covariates_to_dataframe(model, studies, covariates):
# def dataframe_to_ordered_dict(dataframe, covariates):
# def dataframe_to_pydict(dataframe):
# def dataset_to_dataframe(
# def dataset_to_simple_binary_robj(
# def dataset_to_simple_cont_robj(
# def dataset_to_simple_fsn_data_robj(
# def dynamic_save_plot(rfunction, plot_data_path, file_path, format):
# def effect_size(metric, data_type, data):
# def extract_additional_values(res, res_info, sublist_prefix="__"):
# def extract_values_for_results_data_single_result(res, res_info):
# def gather_data(model, data_location, vars_given_directly=False):
# def gather_data_for_single_study(data_location, study):
# def generate_forest_plot(
# def generate_reg_plot(file_path, params_name="plot.data"):
# def get_available_methods(
# def get_btt_indices(data, mods, choice, choice_type):
# def get_data_exploration_analyses():
# def get_exploratory_params(params_path, plot_type=None):
# def get_funnel_params(params_path):
# def get_method_description(method_name):
# def get_mult_from_r(confidence_level):
# def get_nested_rlist_as_pydict(rcommand):
# def get_params(method_name):
# def get_pretty_names_and_descriptions_for_params(method_name, param_list):
# def get_R_libpaths():
# def get_random_effects_methods_descriptions(method_name):
# def histogram_params_toR(params):
# def imputation_dataframes_to_pylist_of_ordered_dicts(
# def impute(
# def joiner(alist, sep=", ", line_length=80):
# def keys_in_dictionary(keys, dictionary):
# def list_of_cov_value_objects_str(studies, cov_list=[], cov_to_ref_var={}):
# def load_in_R(fpath):
# def load_vars_for_plot(
# def make_imputed_datasets(
# def make_weights_str(results):
# def NA_to_None(value):
# def None_to_NA(value, value_type):
# def params_dict_to_Robject(params, robject_type="list"):
# def parse_out_results(result, function_name=None, meta_function_name=None):
# def prepare_funnel_params_for_R(params):
# def regenerate_exploratory_plot(
# def regenerate_forest_plot_of_coefficients(
# def regenerate_funnel_plot(params_path, file_path, edited_funnel_params=None):
# def regenerate_phylo_forest_plot(
# def regenerate_plot_data(
# def rstr_for_rfn(fname, **kargs):
# def scatterplot_params_to_R(params):
# def sort_covariates_by_type(covs, sort_method=NUMERIC_AND_CATEGORICAL):
# def studies_have_point_estimates(studies, data_location, model):
# def studies_have_raw_data(
# def toRBool(value):
# def transform_effect_size(metric, source_data, direction, conf_level):
# def try_n_run(fn):
# def unpack_r_parameters(params_dict):
# def update_plot_params(
# def write_out_plot_data(params_out_path, plot_data_name="plot.data"):
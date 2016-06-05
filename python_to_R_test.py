import python_to_R


import unittest
import ome_globals
import os, os.path

base_dir = os.getcwd()

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

# This is awful but we need it for now to determine how to find some sample data
# This should def. be refactored way in the future.
# If you get a utest failing, make sure you set this string correctly according
# to your path
open_mee_base_dir = '/Users/george/git/OpenMEE'


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



class BaseTestCase(unittest.TestCase):
    def ObservedResultsDataMatchesExpected(
        self,
        expected_result, # expected output from analysis function
        observed_result, # actual output from analysis function
    ):
        for j in range(len(expected_result['results_data'])):
            print "checking %s" % expected_result['results_data'][j][0]

            observed_val = expected_result['results_data'][j][1]['value']
            expected_val = observed_result['results_data'][j][1]['value']

            if type(observed_val) == type([]):
                for idx in range(len(observed_val)):
                    self.assertAlmostEqual(observed_val[idx], expected_val[idx])
            elif type(observed_val) == str:
                # not checking equality of string values in results data
                continue
            else:
                self.assertAlmostEqual(observed_val, expected_val)

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

class TestBinaryMetaAnalysis(BaseTestCase):
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

        self.ObservedResultsDataMatchesExpected(
            expected_result=full_expected_result,
            observed_result=result,
        )


#class TestContinuousMetaAnalysis(unittest.TestCase):
class TestContinuousMetaAnalysis(BaseTestCase):
    def setUp(self):
        python_to_R.set_conf_level_in_R(95)

        r_str = '''tmp_obj <- new(
            'ContinuousData',
            N1=c(60, 65, 40, 200, 45, 85),
            mean1=c(92.0, 92.0, 88.0, 82.0, 88.0, 92.0),
            sd1=c(20.0, 22.0, 26.0, 17.0, 22.0, 22.0),
            N2=c(60, 65, 40, 200, 50, 85),
            mean2=c(94.0, 98.0, 98.0, 94.0, 98.0, 96.0),
            sd2=c(22.0, 21.0, 28.0, 19.0, 21.0, 21.0),
            y=c(-0.0945241585203, -0.277355866266, -0.366544429516, -0.664385099891, -0.461806281288, -0.185164437399),
            SE=c(0.182676111563, 0.176252946255, 0.225476645393, 0.102721757438, 0.208193827499, 0.153721347104),
            study.names=c("Carroll, 1997", "Grant, 1981", "Peck, 1987", "Donat, 2003", "Stewart, 1990", "Young, 1995"),
            years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer()),
            covariates=list())'''
    
        python_to_R.exR.execute_in_R(r_str)


    def test_run_cont_ma(self):

        # run_binary_ma() parameters:
        function_name = 'continuous.random'
        params = {
            'conf.level': 95.0,
            'digits': 3,
            'fp_col2_str': u'[default]',
            'fp_show_col4': True,
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
        cont_data_name = 'tmp_obj'

        # expected result
        full_expected_result = {
            'image_order': None,
            'image_var_names': {
                'Forest Plot': 'r_tmp/1459137190.84989',
            },
            'save_plot_functions': {},
            'texts': {
            'weights': 'study names    weights\nStorm        : 12.565%\nRogue        : 12.641%\nWolverine    : 12.277%\nGambit       : 12.685%\nSpiderman    : 12.593%\nMr. Fantastic: 12.462%\nThe Flash    : 12.000%\nThor         : 12.776%\n',
            'Summary': 'Binary Random-Effects Model\n\nMetric: Odds Ratio\n\n Model Results\n\n Estimate  Lower bound   Upper bound   p-Value  \n\n 0.698        0.249         1.955       0.494   \n\n\n Heterogeneity\n\n tau^2  Q(df=7)   Het. p-Value    I^2    \n\n 2.096  152.959     < 0.001      95.424  \n\n\n Results (log scale)\n\n Estimate  Lower bound   Upper bound   Std. error  \n\n -0.359      -1.388         0.670         0.525    \n\n'},
            'image_params_paths': {},
            'results_data': [
                ('b', {'type': 'vector', 'description': 'estimated coefficients of the model.', 'value': [-0.35849725582231884]}),
                ('se', {'type': 'vector', 'description': 'standard errors of the coefficients.', 'value': [0.10545381861892394]}),
                ('zval', {'type': 'vector', 'description': 'test statistics of the coefficients.', 'value': [-3.3995663743369238]}),
                ('pval', {'type': 'vector', 'description': 'p-values for the test statistics.', 'value': [0.0006749279631807598]}),
                ('ci.lb', {'type': 'vector', 'description': 'lower bound of the confidence intervals for the coefficients.', 'value': [-0.5651829423476291]}),
                ('ci.ub', {'type': 'vector', 'description': 'upper bound of the confidence intervals for the coefficients.', 'value': [-0.15181156929700854]}),
                ('vb', {'type': 'vector', 'description': 'variance-covariance matrix of the estimated coefficients.', 'value': [0.011120507861312912]}),
                ('tau2', {'type': 'vector', 'description': 'estimated amount of (residual) heterogeneity. Always 0 when method="FE".', 'value': [0.03723543730128847]}),
                ('se.tau2', {'type': 'vector', 'description': 'estimated standard error of the estimated amount of (residual) heterogeneity.', 'value': [0.04211456580908173]}),
                ('k', {'type': 'vector', 'description': 'number of outcomes included in the model fitting.', 'value': [6]}),
                ('p', {'type': 'vector', 'description': 'number of coefficients in the model (including the intercept).', 'value': [1]}),
                ('m', {'type': 'vector', 'description': 'number of coefficients included in the omnibus test of coefficients.', 'value': [1]}),
                ('QE', {'type': 'vector', 'description': 'test statistic for the test of (residual) heterogeneity.', 'value': [11.913847853272866]}),
                ('QEp', {'type': 'vector', 'description': 'p-value for the test of (residual) heterogeneity.', 'value': [0.0359875242819107]}),
                ('QM', {'type': 'vector', 'description': 'test statistic for the omnibus test of coefficients.', 'value': [11.557051533522298]}),
                ('QMp', {'type': 'vector', 'description': 'p-value for the omnibus test of coefficients.', 'value': [0.0006749279631807591]}),
                ('I2', {'type': 'vector', 'description': 'value of I2. See print.rma.uni for more details.', 'value': [58.03203077982531]}),
                ('H2', {'type': 'vector', 'description': 'value of H2. See print.rma.uni for more details.', 'value': [2.382769570654573]}),
                ('R2', {'type': 'vector', 'description': 'value of R2. See print.rma.uni for more details.', 'value': 'NULL'}),
                ('int.only', {'type': 'vector', 'description': 'logical that indicates whether the model is an intercept-only model.', 'value': [True]}),
                ('yi', {'type': 'vector', 'description': 'the vector of outcomes', 'value': [-0.0945241585203, -0.277355866266, -0.366544429516, -0.664385099891, -0.461806281288, -0.185164437399]}),
                ('vi', {'type': 'vector', 'description': 'the corresponding sample variances', 'value': [0.033370561735777626, 0.031065101063567913, 0.05083971761768067, 0.010551759451151306, 0.04334466980868337, 0.023630252555468453]}),
                ('X', {'type': 'matrix', 'description': 'the model matrix of the model', 'value': '     intrcpt\n[1,]       1\n[2,]       1\n[3,]       1\n[4,]       1\n[5,]       1\n[6,]       1\n'}),
                ('fit.stats', {'type': 'data.frame', 'description': 'a list with the log-likelihood, deviance, AIC, BIC, and AICc values under the unrestricted and restricted likelihood.', 'value': '            ML       REML\nll   0.7136296  0.2789657\ndev  8.8315690 -0.5579313\nAIC  2.5727409  3.4420687\nBIC  2.1562598  2.6609445\nAICc 6.5727409  9.4420687\n'}),
                ('weights', {'type': 'vector', 'description': 'weights in % given to the observed effects', 'value': [15.750089245922242, 16.28172797395532, 12.626157594095625, 23.270893915209935, 13.800562272939368, 18.270568997877515]})
            ],
            'images': {'Forest Plot': './r_tmp/forest.png'},
        }
        
        # calculate result
        result = python_to_R.run_continuous_ma(
            function_name,
            params,
            res_name=res_name,
            cont_data_name=cont_data_name,
        )

        self.ObservedResultsDataMatchesExpected(
            expected_result=full_expected_result,
            observed_result=result,
        )


class TestMetaRegression(unittest.TestCase):
    def setUp(self):
        python_to_R.set_conf_level_in_R(95)


        r_str = '''tmp_obj<-structure(list(
                    yi = c(-0.09452415852033, -0.277355866265512, -0.366544429515919, -0.664385099891136, -0.461806281287715, -0.185164437399104), 
                    vi = c(0.0333705617355999, 0.0310651010636611, 0.0508397176175572, 0.0105517594511967, 0.0433446698087316, 0.0236302525555215), 
                    STATE = structure(c(1L, 1L, 1L, 2L, 2L, 2L), .Label = c("MA", 
                    "RI"), class = "factor"), slab = structure(c("Carroll, 1997", 
                    "Grant, 1981", "Peck, 1987", "Donat, 2003", "Stewart, 1990", 
                    "Young, 1995"), class = "AsIs")), .Names = c("yi", "vi", 
                    "STATE", "slab"), row.names = c(NA, -6L), class = "data.frame")'''
        
        python_to_R.exR.execute_in_R(r_str)


    def test_run_meta_reg(self): 
        r_str = '''results_obj <- g.meta.regression(
                    data=tmp_obj,
                    mods=structure(list(interactions = list(), numeric = character(0), categorical = "STATE"), .Names = c("interactions", "numeric", "categorical")),
                    method="REML",
                    level=95.0,
                    digits=3,
                    measure="SMD",
                    btt=NULL,
                    make.coeff.forest.plot=FALSE,
                    exclude.intercept=FALSE)'''
        metric = 0
        

        expected_result = {'image_order': None, 'image_var_names': {}, 'save_plot_functions': {}, 'texts': {'Summary': u'\n\nModel Summary:\n---------------\n         SOURCE    Q DF     P\n          model 1.36  1 0.244\n residual error 3.27  4 0.514\n          total 4.62  5 0.463\n\nEffect Tests Summary:\n----------------------\n SOURCE    Q DF     P\n  STATE 1.36  1 0.244\n\n\nMixed-Effects Model (k = 6; tau^2 estimator: REML)\n\ntau^2 (estimated amount of residual heterogeneity):     0.026 (SE = 0.039)\ntau (square root of estimated tau^2 value):             0.161\nI^2 (residual heterogeneity / unaccounted variability): 48.01%\nH^2 (unaccounted variability / sampling variability):   1.92\nR^2 (amount of heterogeneity accounted for):            19.60%\n\nTest for Residual Heterogeneity: \nQE(df = 4) = 7.766, p-val = 0.101\n\nTest of Moderators (coefficient(s) 2): \nQM(df = 1) = 1.358, p-val = 0.244\n\nModel Results:\n\n         estimate     se    zval   pval   ci.lb  ci.ub   \nintrcpt    -0.237  0.145  -1.633  0.103  -0.521  0.047   \nSTATERI    -0.225  0.193  -1.165  0.244  -0.602  0.153   \n\n---\nSignif. codes:  0 \u2018***\u2019 0.001 \u2018**\u2019 0.01 \u2018*\u2019 0.05 \u2018.\u2019 0.1 \u2018 \u2019 1 \n\n\nRegression model formula: yi ~ STATE\nRegression model equation: -0.237 + -0.225*STATERI'}, 'image_params_paths': {}, 'results_data': [('b', {'type': 'vector', 'description': 'estimated coefficients of the model.', 'value': [-0.236836247249815, -0.2245733962144813]}), ('se', {'type': 'vector', 'description': 'standard errors of the coefficients.', 'value': [0.1450665837035122, 0.19268622774116997]}), ('zval', {'type': 'vector', 'description': 'test statistics of the coefficients.', 'value': [-1.6326037410094534, -1.1654875330070007]}), ('pval', {'type': 'vector', 'description': 'p-values for the test statistics.', 'value': [0.10255236393127247, 0.24382170374572817]}), ('ci.lb', {'type': 'vector', 'description': 'lower bound of the confidence intervals for the coefficients.', 'value': [-0.521161526668964, -0.602231462904057]}), ('ci.ub', {'type': 'vector', 'description': 'upper bound of the confidence intervals for the coefficients.', 'value': [0.04748903216933398, 0.15308467047509444]}), ('vb', {'type': 'vector', 'description': 'variance-covariance matrix of the estimated coefficients.', 'value': [0.021044313707408106, -0.021044313707408103, -0.021044313707408103, 0.037127982361122025]}), ('tau2', {'type': 'vector', 'description': 'estimated amount of (residual) heterogeneity. Always 0 when method="FE".', 'value': [0.025819695129668186]}), ('se.tau2', {'type': 'vector', 'description': 'estimated standard error of the estimated amount of (residual) heterogeneity.', 'value': [0.038789582156374396]}), ('k', {'type': 'vector', 'description': 'number of outcomes included in the model fitting.', 'value': [6]}), ('p', {'type': 'vector', 'description': 'number of coefficients in the model (including the intercept).', 'value': [2]}), ('m', {'type': 'vector', 'description': 'number of coefficients included in the omnibus test of coefficients.', 'value': [1]}), ('QE', {'type': 'vector', 'description': 'test statistic for the test of (residual) heterogeneity.', 'value': [7.766127079511218]}), ('QEp', {'type': 'vector', 'description': 'p-value for the test of (residual) heterogeneity.', 'value': [0.10053083905164525]}), ('QM', {'type': 'vector', 'description': 'test statistic for the omnibus test of coefficients.', 'value': [1.358361189594745]}), ('QMp', {'type': 'vector', 'description': 'p-value for the omnibus test of coefficients.', 'value': [0.2438217037457282]}), ('I2', {'type': 'vector', 'description': 'value of I2. See print.rma.uni for more details.', 'value': [48.00592969486093]}), ('H2', {'type': 'vector', 'description': 'value of H2. See print.rma.uni for more details.', 'value': [1.9232962415353745]}), ('R2', {'type': 'vector', 'description': 'value of R2. See print.rma.uni for more details.', 'value': [19.6]}), ('int.only', {'type': 'vector', 'description': 'logical that indicates whether the model is an intercept-only model.', 'value': [False]}), ('yi', {'type': 'vector', 'description': 'the vector of outcomes', 'value': [-0.09452415852033, -0.277355866265512, -0.366544429515919, -0.664385099891136, -0.461806281287715, -0.185164437399104]}), ('vi', {'type': 'vector', 'description': 'the corresponding sample variances', 'value': [0.0333705617355999, 0.0310651010636611, 0.0508397176175572, 0.0105517594511967, 0.0433446698087316, 0.0236302525555215]}), ('X', {'type': 'matrix', 'description': 'the model matrix of the model', 'value': '  intrcpt STATERI\n1       1       0\n2       1       0\n3       1       0\n4       1       1\n5       1       1\n6       1       1\n'}), ('fit.stats', {'type': 'data.frame', 'description': 'a list with the log-likelihood, deviance, AIC, BIC, and AICc values under the unrestricted and restricted likelihood.', 'value': '            ML       REML\nll    1.480225  0.4211768\ndev   7.298377 -0.8423536\nAIC   3.039549  5.1576464\nBIC   2.414828  3.3165295\nAICc 15.039549 29.1576464\n'}), ('weights', {'type': 'vector', 'description': 'weights in % given to the observed effects', 'value': 'NULL'}), ('residuals', {'type': 'blob', 'description': 'Standardized residuals for fitted models', 'value': '               resid    se      z\nCarroll, 1997  0.142 0.195  0.729\nGrant, 1981   -0.041 0.189 -0.214\nPeck, 1987    -0.130 0.236 -0.550\nDonat, 2003   -0.203 0.142 -1.425\nStewart, 1990 -0.000 0.230 -0.002\nYoung, 1995    0.276 0.183  1.512\n'})], 'images': {}}["results_data"]

        observed_result = python_to_R.run_gmeta_regression(metric, r_str=r_str)['results_data']

        print "checking coefficient estimates"
        observed_coefs = observed_result[0]
        expected_coefs = expected_result[0]

        # sanity check the formatting
        self.assertEqual(observed_coefs[0], "b")
        for j, observed_val in enumerate(observed_coefs[1]['value']):
            self.assertAlmostEqual(observed_val, expected_coefs[1]['value'][j])
        print "ok."


        print "checking standard errors"
        observed_SEs = observed_result[1]
        expected_SEs = expected_result[1]
        self.assertEqual(observed_SEs[0], "se")
        for j, observed_SE in enumerate(observed_SEs[1]['value']):
            self.assertAlmostEqual(observed_SE, expected_SEs[1]['value'][j])
        print "done."


    def test_run_meta_regression_cond_means(self):
        r_str = '''results_obj <- g.meta.regression.cond.means(
                    data=tmp_obj,
                    mods=structure(list(interactions = list(), numeric = character(0), 
                            categorical = "STATE"), .Names = c("interactions", "numeric", "categorical")),
                    method="REML",
                    level=95.0,
                    digits=4,
                    strat.cov="STATE",
                    cond.means.data=list(),
                    btt=NULL)'''

        metric = 0
        result_rows = python_to_R.run_gmeta_regression(metric, r_str=r_str)['texts']['Conditional Means Summary'].split("\n")

        def _extract_res(i):
            row = [s for s in result_rows[i].split(" ") if len(s.strip())>1]
            return [float(r_j) for r_j in row[1:]]

        def check_row(observed, expected, theta=.01):
            # note that we allow a fair amount of divergence (0.05)
            # here because the bootstrap method is stochastic.
            for j, expected_val in enumerate(expected):
                observed_val = observed[j]
                #self.assertAlmostEqual(observed_val, expected_val)
                diff = abs(observed_val-expected_val)
                print "difference: %s" % diff
                self.assertTrue(diff <= theta)

        metric = 0
        

        '''
            cond.mean     se    var   ci.lb   ci.ub
        MA   -0.2368 0.1451 0.0210 -0.5212  0.0475
        RI   -0.4614 0.1268 0.0161 -0.7100 -0.2128
        '''
        expected_MA = [-0.2368, 0.1451, 0.0210, -0.5212, 0.0475]
        observed_MA = _extract_res(4)
        check_row(observed_MA, expected_MA)

        expected_RI = [ -0.4614, 0.1268, 0.0161, -0.7100, -0.2128]
        observed_RI = _extract_res(5)
        check_row(observed_RI, expected_RI)



class TestBootstrapMetaRegression(unittest.TestCase):
    '''
    @TODO this test currently relies on passing along the assembled
    R string to run the bootstrap analysis directly, which is a 
    tad hacky. The reason we have done this for now is to avoid
    re-constructing the list of Covariate objects, which presently come
    from the UI. 
    '''
    def setUp(self):
        python_to_R.set_conf_level_in_R(95)


        r_str = '''tmp_obj<-structure(list(
                    yi = c(-0.09452415852033, -0.277355866265512, -0.366544429515919, -0.664385099891136, -0.461806281287715, -0.185164437399104), 
                    vi = c(0.0333705617355999, 0.0310651010636611, 0.0508397176175572, 0.0105517594511967, 0.0433446698087316, 0.0236302525555215), 
                    STATE = structure(c(1L, 1L, 1L, 2L, 2L, 2L), .Label = c("MA", 
                    "RI"), class = "factor"), slab = structure(c("Carroll, 1997", 
                    "Grant, 1981", "Peck, 1987", "Donat, 2003", "Stewart, 1990", 
                    "Young, 1995"), class = "AsIs")), .Names = c("yi", "vi", 
                    "STATE", "slab"), row.names = c(NA, -6L), class = "data.frame")'''
        
        python_to_R.exR.execute_in_R(r_str)


    def test_run_bootstrap_meta_reg(self):
        ''' Vanilla bootstrap meta-regression. '''
        r_str = '''results_obj <- g.bootstrap.meta.regression(
            data=tmp_obj,
            mods=structure(list(interactions = list(), numeric = character(0), 
                categorical = "STATE"), .Names = c("interactions", "numeric", "categorical")),
            method="REML",
            level=95.0,
            digits=4,
            n.replicates=1000,
            histogram.title="Bootstrap Histogram",
            bootstrap.plot.path="./r_tmp/bootstrap.png")'''

        result = python_to_R.run_gmeta_regression_bootstrapped(1000, r_str=r_str)
        '''
        The result will look as below. We extract the numbers from this
        and check against observed.

        # Bootstrap replicates: 1000
        # of failures: 0

                estimate Lower.Bound Upper.Bound
        intrcpt  -0.2368     -0.3818     -0.0889
        STATERI  -0.2246     -0.5474      0.0923
        '''

        result_rows = result['texts']['Bootstrapped Meta Regression Summary'].split("\n")

        def _extract_res(i):
            row = [s for s in result_rows[i].split(" ") if len(s.strip())>1]
            return [row[0]] + [float(r_j) for r_j in row[1:]]

        def check_row(observed, expected, theta=.05):
            # note that we allow a fair amount of divergence (0.05)
            # here because the bootstrap method is stochastic.
            for j, expected_val in enumerate(expected):
                observed_val = observed[j]
                #self.assertAlmostEqual(observed_val, expected_val)
                diff = abs(observed_val-expected_val)
                print "difference: %s" % diff
                self.assertTrue(diff <= theta)

        ''' check the intercept numbers '''
        intercept_row_expected = [-0.2368, -0.3838, -0.0802]
        intercept_row_observed = _extract_res(-2)[1:] # skip var name
        check_row(intercept_row_observed, intercept_row_expected)

        ''' and the coef estimate '''
        coef_row_expected = [-0.2246, -0.5449, 0.0898]
        coef_row_observed = _extract_res(-1)[1:]
        check_row(coef_row_observed, coef_row_expected)

    def test_run_cond_means_bootstrap_meta_reg(self):
        r_str = '''results_obj <- g.bootstrap.meta.regression.cond.means(
                    data=tmp_obj,
                    mods=structure(list(interactions = list(), numeric = character(0), 
                                    categorical = "STATE"), 
                                    .Names = c("interactions", "numeric", "categorical")),
                    method="REML",
                    level=95.0,
                    digits=4,
                    n.replicates=1000,
                    histogram.title="Bootstrap Histogram",
                    bootstrap.plot.path="./r_tmp/bootstrap.png",
                    strat.cov="STATE",
                    cond.means.data=list())'''
        def _extract_res(i):
            row = [s for s in result_rows[i].split(" ") if len(s.strip())>1]
            return [row[0]] + [float(r_j) for r_j in row[1:]]

        def check_row(observed, expected, theta=.05):
            # note that we allow a fair amount of divergence (0.05)
            # here because the bootstrap method is stochastic.
            for j, expected_val in enumerate(expected):
                observed_val = observed[j]
                #self.assertAlmostEqual(observed_val, expected_val)
                diff = abs(observed_val-expected_val)
                print "difference: %s" % diff
                self.assertTrue(diff <= theta)

        result = python_to_R.run_gmeta_regression_bootstrapped(1000, r_str=r_str)
        result_rows = result['texts']['Bootstrapped Conditional Means Meta Regression Summary'].split("\n")

        ''' check MA estimate '''
        MA_row_expected = [-0.2368, -0.3693, -0.1011]
        MA_row_observed = _extract_res(-2)[1:]
        check_row(MA_row_observed, MA_row_expected)

        ''' check RI estimate '''
        RI_row_expected = [-0.4614, -0.7474, -0.1839]
        RI_row_observed = _extract_res(-1)[1:]
        check_row(RI_row_observed, RI_row_expected)
        #import pdb; pdb.set_trace()


class TestFailSafeN(unittest.TestCase):
    def setUp(self):
        r_str = '''tmp_obj <- data.frame(yi=c(0.559615787935, 0.829598283288, 2.57694350425, -0.337229812415, 1.66579084899, 
                0.929187972983, -0.47692407209, -1.05693959227, 1.96711235671, -0.679541528504, 2.62051920862, 0.410284394544, 
                -0.0180185055027, -0.304489190768, 0.0, 1.67726050877, -1.75126810787, -0.0500104205747, 
                1.15125602215), vi=c(0.380952380952, 0.511591478697, 2.25382075334, 0.143645452199, 2.45638276752, 
                0.077038306378, 0.367816091954, 2.69445650601, 0.679370629371, 0.52721214365, 
                2.17608553609, 0.665273132664, 0.161038961039, 0.257574152542, 4.10256410256, 
                2.46787460454, 0.541125541126, 4.10006253909, 2.70177870178))'''
        python_to_R.exR.execute_in_R(r_str)


    def test_fail_safe_n_plot(self):
        r_str = '''result <- failsafe.wrapper(tmp_obj, digits=4, alpha=0.05, type="Rosenthal")'''
        result = python_to_R.exR.execute_in_R(r_str)
        
        to_dict = lambda rv : dict(zip(rv.names, list(rv)))
        result = to_dict(result)
        summary = to_dict(result["Summary"])
        expected_p_val = 0.028124971427696127
        self.assertAlmostEqual(summary['pval'][0],expected_p_val)


class TestFunnelPlot(unittest.TestCase):
    def setUp(self):
        r_str = '''tmp_obj <- new(
                    'BinaryData',
                    g1O1=c(9, 7, 5, 13, 2, 49, 6, 0, 11, 3, 6, 4, 16, 8, 0, 2, 3, 0, 1),
                    g1O2=c(18, 57, 25, 139, 34, 96, 29, 70, 20, 73, 87, 23, 56, 64, 19, 28, 22, 20, 55),
                    g2O1=c(6, 3, 0, 19, 0, 26, 8, 1, 2, 6, 0, 3, 16, 10, 0, 0, 11, 0, 0),
                    g2O2=c(21, 56, 30, 145, 36, 129, 24, 73, 26, 74, 92, 26, 55, 59, 19, 30, 14, 19, 58),
                    y=c(0.559615787935, 0.829598283288, 2.57694350425, -0.337229812415, 1.66579084899, 
                        0.929187972983, -0.47692407209, -1.05693959227, 1.96711235671, 
                        -0.679541528504, 2.62051920862, 0.410284394544, -0.0180185055027, 
                        -0.304489190768, 0.0, 1.67726050877, -1.75126810787, -0.0500104205747, 
                        1.15125602215),
                    SE=c(0.617213399848, 0.715256232896, 1.50127304423, 0.379005873568, 1.56728515833, 
                        0.27755775323, 0.606478434863, 1.64147997429, 0.824239424785, 0.726093756791, 
                        1.47515610567, 0.815642772704, 0.401296599835, 0.507517637666, 2.02547873417, 
                        1.57094704066, 0.735612357921, 2.024861116, 1.64370882512),
                    study.names=c("Gonzalez", "Prins", "Giamarellou", "Maller", "Sturm", "Marik", "Muijsken", 
                        "Vigano", "Hansen", "De Vries", "Mauracher", "Nordstrom", "Rozdzinski", 
                        "Ter Braak", "Tulkens", "Van der Auwera", "Klastersky", "Vanhaeverbeek", 
                        "Hollender"),
                    years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
                        as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
                        as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
                        as.integer(), as.integer(), as.integer(), as.integer()),
                    covariates=list())'''
        
        python_to_R.exR.execute_in_R(r_str)

    def test_generate_funnel_plot(self):
        r_str = '''result<-funnel.wrapper('binary.random', tmp_obj,
                    structure(list(conf.level = 95, digits = 3L, 
                    fp_col2_str = structure(1L, .Label = "[default]", class = "factor"), 
                    fp_show_col4 = TRUE, to = structure(1L, .Label = "only0", class = "factor"), 
                    fp_col4_str = structure(1L, .Label = "Ev/Ctrl", class = "factor"), 
                    fp_xticks = structure(1L, .Label = "[default]", class = "factor"), 
                    fp_col3_str = structure(1L, .Label = "Ev/Trt", class = "factor"), 
                    fp_show_col3 = TRUE, fp_show_col2 = TRUE, fp_show_col1 = TRUE, 
                    fp_plot_lb = structure(1L, .Label = "[default]", class = "factor"), 
                    fp_outpath = structure(1L, .Label = "./r_tmp/forest.png", class = "factor"), 
                    rm.method = structure(1L, .Label = "DL", class = "factor"), 
                    adjust = 0.5, fp_plot_ub = structure(1L, .Label = "[default]", class = "factor"), 
                    fp_col1_str = structure(1L, .Label = "Studies", class = "factor"), 
                    measure = structure(1L, .Label = "OR", class = "factor"), 
                    fp_xlabel = structure(1L, .Label = "[default]", class = "factor"), 
                    fp_show_summary_line = TRUE), .Names = c("conf.level", "digits", 
                "fp_col2_str", "fp_show_col4", "to", "fp_col4_str", "fp_xticks", 
                "fp_col3_str", "fp_show_col3", "fp_show_col2", "fp_show_col1", 
                "fp_plot_lb", "fp_outpath", "rm.method", "adjust", "fp_plot_ub", 
                "fp_col1_str", "measure", "fp_xlabel", "fp_show_summary_line"
                ), row.names = c(NA, -1L), class = "data.frame"), digits=5, steps=5, addtau2=FALSE)'''

        results = python_to_R.run_funnelplot_analysis(*[None]*8, r_str=r_str)
        
        # we are basically just asserting that the plot exists here!
        image_name, image_path = results['images'].items()[0]
        self.assertTrue(image_name == "Funnel Plot")
        self.assertTrue( os.path.isfile(image_path))

class TestScatterPlot(unittest.TestCase):
    def test_run_scatterplot(self):
        # Not actually testing run_scatterplot() since it's basically just a
        # passthrough to _run_scatterplot()
        pass

    def test__get_scatterplot_data_rstr(self):
        # TODO
        pass
    def test__get_scatterplot_params_rstr(self):
        # TODO
        pass

    def test__run_scatterplot(self):
        data_r_str = '''
            structure(
                list(
                    y = c(
                        10L, 20L, 40L, 100L, 38L, 588L, 2910L, 302L, 101L, 101L,
                        48L, 48L, 1670L, 1816L, 1601L, 1034L, 1404L, 1246L,
                        646L, 541L, 1046L, 1895L, 1162L, 14L, 906L, 1188L,
                        1990L, 2188L, 635L
                    ),
                    x = c(
                        40, 65, 2000, 47, 199, 348, 40, 18, 49, 44, 18, 584, 35,
                        107, 101, 50, 79, 48, 75, 41, 53, 24, 54, 33, 102, 87,
                        118, 60, 106
                    )
                ),
                .Names = c("y", "x"),
                row.names = c(NA, -29L),
                class = "data.frame"
            )
        '''
        params_r_str = '''structure(list(xlab = "Age", ylab = "sample size"), .Names = c("xlab", "ylab"))'''
        res_name = 'result'
        var_name = 'tmp_obj'

        results = python_to_R._run_scatterplot(
            data_rstr=data_r_str,
            params_rstr=params_r_str,
            res_name=res_name,
            var_name=var_name,
        )
        # we are basically just asserting that the plot exists here!
        image_name, image_path = results['images'].items()[0]
        self.assertTrue(image_name == "Scatterplot")
        self.assertTrue( os.path.isfile(image_path))

class TestHistogram(unittest.TestCase):
    def test_run_histogram(self):
        # Not actually testing run_histogram() since it's basically just a
        # passthrough to _run_histogram()
        pass

    def test__get_histogram_data_rstr(self):
        # TODO
        pass

    def test__run_histogram(self):
        data_r_str = '''
            c(
                "US", "US", "US", "US", "CANADA", "CANADA", "CANADA", "CANADA",
                "CANADA", "CANADA", "CHINA", "CHINA", "US", "US", "US", "US",
                "CANADA", "CANADA", "CANADA", "CANADA", "CANADA", "CANADA",
                "CHINA", "CHINA", "US", "US", "US", "US", "CANADA"
            )
        '''
        params_r_str = '''
            structure(
                list(
                    GRADIENT = FALSE,
                    xlab = "Country",
                    color = "#000000",
                    fill = "#FFFFFF"
                ),
                .Names = c("GRADIENT", "xlab", "color", "fill")
            )
        '''
        res_name = 'result'
        var_name = 'tmp_obj'

        results = python_to_R._run_histogram(
            data_rstr=data_r_str,
            params_rstr=params_r_str,
            res_name=res_name,
            var_name=var_name,
        )
        # we are basically just asserting that the plot exists here!
        image_name, image_path = results['images'].items()[0]
        self.assertTrue(image_name == "Histogram")
        self.assertTrue( os.path.isfile(image_path))

class TestDynamicDataExplorationAnalysis(unittest.TestCase):
    def test__run_dynamic_data_exploration_analysis(self):
        data_rstr = '''
        tmp_obj<-structure(
            list(
                yi = c(
                    0.251222927, 0.359662774, 0.365604284,
                    0.132471994, 0.413560041, 0.351011661, 0.29080727, 0.220697921,
                    0.314726091, 0.299664236, 0.309915434, 0.018196837, 0.220769991,
                    0.288105953, 0.082563839, 0.199795575, 0.280285088, 0.375566345,
                    0.138447493, 0.304502484, 0.268833813, 0.353074827, 0.420422366,
                    0.221994369, 0.357595146, 0.286467997, 0.395542146, 0.335632696,
                    0.120763021, 0.351163226, 0.38844754, 0.268362539, 0.351484633,
                    0.24250489, 0.255221155, 0.204200073, 0.433802537, 0.278007089,
                    0.377414447, 0.194480138, 0.344467919, 0.345545078, 0.367696705,
                    0.252591178, 0.319385547, 0.2557075, 0.266361608, 0.377689832,
                    0.377093453, 0.245424913, 0.152421443, 0.394352217, 0.215269482,
                    0.365345905, 0.301902019, 0.126634986, 0.439153487, 0.291032036,
                    0.274961532, 0.423477194, 0.235710702, 0.297293615, 0.296571162,
                    0.297957025, 0.293439342, 0.300234828, 0.320274922, 0.139814023,
                    0.272618472, 0.331860825, 0.029592308, 0.266549972, 0.275775005,
                    0.255888575, 0.338694662, 0.250091707, 0.223141687, 0.324536035,
                    0.244416143, 0.134387143, 0.146982837, 0.421676602, 0.236608408,
                    0.105958044, 0.453174952, 0.256437724, 0.363988393, 0.263553561,
                    0.451273894, 0.359168445, 0.394039486, 0.462775113, 0.297986878,
                    0.316844753, 0.177924634, 0.277252993, 0.282120994, 0.299782482,
                    0.373713129, 0.438260456
                ),
                vi = c(
                    0.009049045, 0.0069543, 0.012720911,
                    0.015320798, 0.005453874, 0.006199695, 0.006348592, 0.015338259,
                    0.006149291, 0.009633331, 0.008786344, 0.020819539, 0.00923364,
                    0.014752276, 0.006165081, 0.010718104, 0.011958481, 0.006707227,
                    0.014358686, 0.012663905, 0.006940967, 0.004328909, 0.004772763,
                    0.007469964, 0.003674412, 0.012211691, 0.012937646, 0.00729066,
                    0.009427624, 0.008445885, 0.006999857, 0.004160144, 0.006455291,
                    0.017035408, 0.009103826, 0.018741701, 0.003414737, 0.006978668,
                    0.005836558, 0.00477209, 0.018064267, 0.010339385, 0.009010573,
                    0.004951786, 0.021220821, 0.01247861, 0.007846697, 0.003223902,
                    0.003053202, 0.010640497, 0.011224413, 0.017828929, 0.015414671,
                    0.017461884, 0.007059981, 0.00405098, 0.011429505, 0.004296281,
                    0.021362706, 0.012026686, 0.009195544, 0.010012586, 0.010802949,
                    0.010125912, 0.015758511, 0.009739335, 0.007670188, 0.014564942,
                    0.011425092, 0.007133926, 0.009786758, 0.011063464, 0.004589678,
                    0.009492713, 0.008249802, 0.019104788, 0.005573425, 0.003510727,
                    0.014984581, 0.010043816, 0.020809974, 0.003595715, 0.016814473,
                    0.009052517, 0.014032017, 0.008081517, 0.005190192, 0.007871853,
                    0.00696897, 0.0090314, 0.013463654, 0.012602923, 0.009654563,
                    0.009991322, 0.004883791, 0.006086932, 0.021721806, 0.009979969,
                    0.005140155, 0.009460106
                ),
                slab = structure(c(
                    "study label 01",
                    "study label 02", "study label 03", "study label 04", "study label 05",
                    "study label 06", "study label 07", "study label 08", "study label 09",
                    "study label 10", "study label 11", "study label 12", "study label 13",
                    "study label 14", "study label 15", "study label 16", "study label 17",
                    "study label 18", "study label 19", "study label 20", "study label 21",
                    "study label 22", "study label 23", "study label 24", "study label 25",
                    "study label 26", "study label 27", "study label 28", "study label 29",
                    "study label 30", "study label 31", "study label 32", "study label 33",
                    "study label 34", "study label 35", "study label 36", "study label 37",
                    "study label 38", "study label 39", "study label 40", "study label 41",
                    "study label 42", "study label 43", "study label 44", "study label 45",
                    "study label 46", "study label 47", "study label 48", "study label 49",
                    "study label 50", "study label 51", "study label 52", "study label 53",
                    "study label 54", "study label 55", "study label 56", "study label 57",
                    "study label 58", "study label 59", "study label 60", "study label 61",
                    "study label 62", "study label 63", "study label 64", "study label 65",
                    "study label 66", "study label 67", "study label 68", "study label 69",
                    "study label 70", "study label 71", "study label 72", "study label 73",
                    "study label 74", "study label 75", "study label 76", "study label 77",
                    "study label 78", "study label 79", "study label 80", "study label 81",
                    "study label 82", "study label 83", "study label 84", "study label 85",
                    "study label 86", "study label 87", "study label 88", "study label 89",
                    "study label 90", "study label 91", "study label 92", "study label 93",
                    "study label 94", "study label 95", "study label 96", "study label 97",
                    "study label 98", "study label 99", "study label 100"), class = "AsIs")
            ),
            .Names = c("yi", "vi", "slab"),
            row.names = c(NA, -100L),
            class = "data.frame"
        )
        '''

        python_to_R.exR.execute_in_R(data_rstr)

        analysis_details = {
            'MAIN': 'weighted.histogram'
        }

        results = python_to_R._run_dynamic_data_exploration_analysis(
            analysis_details=analysis_details,
            res_name="result",
            var_name="tmp_obj",
        )

        # we are basically just asserting that the plot exists here!
        image_name, image_path = results['images'].items()[0]
        self.assertTrue(image_name == "Weighted Histogram of Correlations")
        self.assertTrue( os.path.isfile(image_path))

class TestPhyloMA(BaseTestCase):
    def test__run_phylo_ma(self):

        # Prepare data
        data_rstr = '''
            tmp_obj <- structure(
                list(
                    yi = c(0.5, 0.2, 0.2, 0.1, 0.8, 0.9, 1),
                    vi = c(0.2, 0.1, 0.4, 0.8, 0.9, 0.2, 0.1),
                    slab = structure(c("study 1", "study 2", "study 3", "study 4", "study 5", "study 6", "study 7"), class = "AsIs"),
                    species = structure(c(1L, 1L, 2L, 3L, 4L, 5L, 5L), .Label = c("A", "B", "C", "D", "E"), class = "factor")
                ),
                .Names = c("yi", "vi", "slab", "species"),
                row.names = c(NA, -7L),
                class = "data.frame"
            )
        '''
        python_to_R.exR.execute_in_R(data_rstr)

        tree_rstr = '''
            tree <- structure(
                list(
                    edge = structure(
                        c(6L, 7L, 7L, 6L, 8L, 8L, 9L, 9L, 7L, 1L, 2L, 8L, 3L, 9L, 4L, 5L),
                        .Dim = c(8L, 2L)
                    ),
                    Nnode = 4L,
                    tip.label = c("A", "B", "C", "D", "E"),
                    edge.length = c(1, 1, 1, 1, 1, 0.5, 0.5, 0.5)
                ),
                .Names = c("edge", "Nnode", "tip.label", "edge.length"),
                class = "phylo", order = "cladewise"
            )
        '''

        python_to_R.exR.execute_in_R(tree_rstr)

        # Parameters:
        params = {
            'tree_name': 'tree',
            'evo_model': 'BM',
            'random_effects_method': 'ML',
            'lambda_': 1.0,
            'alpha': 1.0,
            'include_species': True,
            'plot_params': {
                'digits': 4,
                'fp_show_summary_line': True,
                'fp_col2_str': u'[default]',
                'fp_show_col4': True,
                'fp_xlabel': u'[default]',
                'fp_col4_str': u'Ev/Ctrl',
                'fp_xticks': '[default]',
                'fp_col3_str': u'Ev/Trt',
                'fp_show_col3': True,
                'fp_show_col2': True,
                'fp_show_col1': True,
                'fp_plot_lb': '[default]',
                'fp_outpath': u'./r_tmp/forest.png',
                'fp_plot_ub': '[default]',
                'fp_col1_str': u'Studies',
                'measure': 'OR',
            },
            'data_name': 'tmp_obj',
            'fixed_effects': False,
            'digits': 4,
            'conf_level': 95.0,
            'results_name': 'results_obj',
        }

        full_expected_result = {
            'image_order': None,
            'image_var_names': {'Forest Plot__phylo': 'r_tmp/1461548676.0349'},
            'save_plot_functions': {},
            'texts': {'Summary': u'\nMultivariate Meta-Analysis Model (k = 7; method: ML)\n\nVariance Components: \n\n            estim    sqrt  nlvls  fixed                factor    R\nsigma^2.1  0.0000  0.0000      7     no  betweenStudyVariance   no\nsigma^2.2  0.0340  0.1845      5     no     phylogenyVariance  yes\n\nTest for Heterogeneity: \nQ(df = 6) = 4.4523, p-val = 0.6157\n\nModel Results:\n\nestimate       se     zval     pval    ci.lb    ci.ub          \n  0.5789   0.2091   2.7691   0.0056   0.1692   0.9887       ** \n\n---\nSignif. codes:  0 \u2018***\u2019 0.001 \u2018**\u2019 0.01 \u2018*\u2019 0.05 \u2018.\u2019 0.1 \u2018 \u2019 1 \n'},
            'image_params_paths': {},
            'results_data': [
                ('b', {'type': 'matrix', 'description': 'estimated coefficients of the model.', 'value': '             [,1]\nintrcpt 0.5789494\n'}),
                ('se', {'type': 'vector', 'description': 'standard errors of the coefficients.', 'value': [0.2090765126869899]}),
                ('zval', {'type': 'vector', 'description': 'test statistics of the coefficients.', 'value': [2.7690793177618054]}),
                ('pval', {'type': 'vector', 'description': 'p-values for the test statistics.', 'value': [0.005621494796307728]}),
                ('ci.lb', {'type': 'vector', 'description': 'lower bound of the confidence intervals for the coefficients.', 'value': [0.16916701223157565]}),
                ('ci.ub', {'type': 'vector', 'description': 'upper bound of the confidence intervals for the coefficients.', 'value': [0.9887318819910393]}),
                ('vb', {'type': 'matrix', 'description': 'variance-covariance matrix of the estimated coefficients.', 'value': '           intrcpt\nintrcpt 0.04371299\n'}),
                ('sigma2', {'type': 'vector', 'description': 'estimated sigma^2 value(s)', 'value': [8.690201786983326e-11, 0.03402342057707157]}),
                ('tau2', {'type': 'vector', 'description': 'estimated taU^2 values', 'value': [0.0]}),
                ('rho', {'type': 'vector', 'description': 'estimated \xcf\x81 value(s).', 'value': [0.0]}),
                ('k', {'type': 'vector', 'description': 'number of studies included in the model.', 'value': [7]}),
                ('p', {'type': 'vector', 'description': 'number of coefficients in the model (including the intercept).', 'value': [1]}),
                ('m', {'type': 'vector', 'description': 'number of coefficients included in the omnibus test of coefficients.', 'value': [1]}),
                ('QE', {'type': 'matrix', 'description': 'test statistic for the test of (residual) heterogeneity.', 'value': '[1] 4.452291\n'}),
                ('QEp', {'type': 'matrix', 'description': 'p-value for the test of (residual) heterogeneity.', 'value': '[1] 0.6157117\n'}),
                ('QM', {'type': 'vector', 'description': 'test statistic for the omnibus test of coefficients.', 'value': [7.667800268056186]}),
                ('QMp', {'type': 'vector', 'description': 'p-value for the omnibus test of coefficients.', 'value': [0.005621494796307731]}),
                ('int.only', {'type': 'vector', 'description': 'logical that indicates whether the model is an intercept-only model.', 'value': [True]}),
                ('yi', {'type': 'vector', 'description': 'the vector of outcomes', 'value': [0.5, 0.2, 0.2, 0.1, 0.8, 0.9, 1.0]}),
                ('V', {'type': 'matrix', 'description': 'the corresponding variance-covariance matrix of the sampling errors', 'value': '     [,1] [,2] [,3] [,4] [,5] [,6] [,7]\n[1,]  0.2  0.0  0.0  0.0  0.0  0.0  0.0\n[2,]  0.0  0.1  0.0  0.0  0.0  0.0  0.0\n[3,]  0.0  0.0  0.4  0.0  0.0  0.0  0.0\n[4,]  0.0  0.0  0.0  0.8  0.0  0.0  0.0\n[5,]  0.0  0.0  0.0  0.0  0.9  0.0  0.0\n[6,]  0.0  0.0  0.0  0.0  0.0  0.2  0.0\n[7,]  0.0  0.0  0.0  0.0  0.0  0.0  0.1\n'}), ('X', {'type': 'matrix', 'description': 'and the model matrix of the model.', 'value': '     intrcpt\n[1,]       1\n[2,]       1\n[3,]       1\n[4,]       1\n[5,]       1\n[6,]       1\n[7,]       1\n'}),
                ('fit.stats', {'type': 'data.frame', 'description': 'a list with the log-likelihood, deviance, AIC, BIC, and AICc values', 'value': '            ML     REML\nll   -3.996878 -3.67004\ndev   4.197458  7.34008\nAIC  13.993757 13.34008\nBIC  13.831487 12.71536\nAICc 21.993757 25.34008\n'})
            ],
            'images': {'Forest Plot__phylo': './r_tmp/forest.png'}
        }

        results = python_to_R._run_phylo_ma(**params)

        # we are basically just asserting that the plot exists here!
        image_name, image_path = results['images'].items()[0]
        self.assertTrue(image_name == "Forest Plot__phylo")
        self.assertTrue( os.path.isfile(image_path))

        self.ObservedResultsDataMatchesExpected(
            expected_result=full_expected_result,
            observed_result=results,
        )

class TestPermutationAnalysis(BaseTestCase):
    def test_run_permutation_analysis_ma_mode(self):
        # prepare data
        data_rstr = '''
        tmp_obj <- structure(
            list(
                yi = c(-0.09452415852033,
                -0.277355866265512,
                -0.366544429515919,
                -0.664385099891136,
                -0.461806281287715,
                -0.185164437399104
            ),
            vi = c(
                0.0333705617355999,
                0.0310651010636611,
                0.0508397176175572,
                0.0105517594511967,
                0.0433446698087316,
                0.0236302525555215
            ),
            slab = structure(c(
                "Carroll, 1997", "Grant, 1981", "Peck, 1987", "Donat, 2003",
                "Stewart, 1990", "Young, 1995"
            ), class = "AsIs")),
            .Names = c("yi", "vi", "slab"),
            row.names = c(NA, -6L), class = "data.frame")
        '''

        python_to_R.exR.execute_in_R(data_rstr)

        parameters = {
            'digits': 4,
            'weighted': True,
            'level': 95.0,
            'data_type_and_metric': (0, 0),
            'exact': False,
            'knha': False,
            'retpermdist': False,
            'iter': 100,
            'intercept': True,
            'make_histograms': False,
            #'studies': [<dataset.study.Study instance at 0x11993ed88>, <dataset.study.Study instance at 0x11e9be098>, <dataset.study.Study instance at 0x11e9be0e0>, <dataset.study.Study instance at 0x11e9be128>, <dataset.study.Study instance at 0x11e9be170>, <dataset.study.Study instance at 0x11e9be1b8>],
            'method': 'REML',
            'data_location': {
                'experimental_mean': 5,
                'effect_size': 8,
                'experimental_std_dev': 6,
                'experimental_sample_size': 4,
                'control_std_dev': 3,
                'control_sample_size': 1,
                'variance': 9,
                'control_mean': 2
            }
        }

        result = python_to_R.run_permutation_analysis(
            parameters=parameters,
            meta_reg_mode=False,
        )

        full_expected_result = {
            'image_order': None,
            'image_var_names': {},
            'save_plot_functions': {},
            'texts': {
                'Summary': u'\nModel Results:\n\n         estimate      se     zval   pval*    ci.lb    ci.ub   \nintrcpt   -0.3607  0.1011  -3.5664  0.0312  -0.5589  -0.1624  *\n\n---\nSignif. codes:  0 \u2018***\u2019 0.001 \u2018**\u2019 0.01 \u2018*\u2019 0.05 \u2018.\u2019 0.1 \u2018 \u2019 1 \n'
            },
            'image_params_paths': {},
            'results_data': [
                ('pval', {'type': 'vector', 'description': 'p-value(s) based on the permutation test.', 'value': [0.03125]}),
                ('QMp', {'type': 'vector', 'description': 'p-value for the omnibus test of coefficients based on the permutation test.', 'value': [0.03125]})
            ],
            'images': {}
        }

        self.ObservedResultsDataMatchesExpected(
            expected_result=full_expected_result,
            observed_result=result,
        )

    def test_run_permutation_analysis_meta_reg_mode(self):
        # not implmented yet
        pass

# tests run_meta_method for continuous data
#   cumulative
#   leave-one-out
#   subgroup
#   bootstrap
class TestMetaMethod(BaseTestCase):
    def setUp(self):
        python_to_R.set_conf_level_in_R(95)

    def _setup_cum_data(self):
        r_str = '''
        tmp_obj <- new(
            'ContinuousData',
            N1=c(60, 65, 40, 200, 45, 85),
            mean1=c(92.0, 92.0, 88.0, 82.0, 88.0, 92.0),
            sd1=c(20.0, 22.0, 26.0, 17.0, 22.0, 22.0),
            N2=c(60, 65, 40, 200, 50, 85),
            mean2=c(94.0, 98.0, 98.0, 94.0, 98.0, 96.0),
            sd2=c(22.0, 21.0, 28.0, 19.0, 21.0, 21.0),
            y=c(
                -0.0945241585203, -0.277355866266, -0.366544429516,
                -0.664385099891, -0.461806281288, -0.185164437399
            ),
            SE=c(
                0.182676111563, 0.176252946255, 0.225476645393, 0.102721757438,
                0.208193827499, 0.153721347104
            ),
            study.names=c(
                "Carroll, 1997",
                "Grant, 1981",
                "Peck, 1987",
                "Donat, 2003",
                "Stewart, 1990",
                "Young, 1995"
            ),
            years=c(
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

    def _setup_loo_data(self):
        r_str = '''
        tmp_obj <- new(
            'ContinuousData',
            N1=c(60, 65, 40, 200, 45, 85),
            mean1=c(92.0, 92.0, 88.0, 82.0, 88.0, 92.0),
            sd1=c(20.0, 22.0, 26.0, 17.0, 22.0, 22.0),
            N2=c(60, 65, 40, 200, 50, 85),
            mean2=c(94.0, 98.0, 98.0, 94.0, 98.0, 96.0),
            sd2=c(22.0, 21.0, 28.0, 19.0, 21.0, 21.0),
            y=c(
                -0.0945241585203, -0.277355866266, -0.366544429516,
                -0.664385099891, -0.461806281288, -0.185164437399
            ),
            SE=c(
                0.182676111563, 0.176252946255, 0.225476645393, 0.102721757438,
                0.208193827499, 0.153721347104
            ),
            study.names=c(
                "Carroll, 1997", "Grant, 1981", "Peck, 1987", "Donat, 2003",
                "Stewart, 1990", "Young, 1995"
            ),
            years=c(
                as.integer(), as.integer(), as.integer(), as.integer(),
                as.integer(), as.integer()
            ),
            covariates=list())
        '''

        python_to_R.exR.execute_in_R(r_str)

    def _setup_subgroup_data(self):
        r_str = '''
        tmp_obj <- new(
            'ContinuousData',
            N1=c(60, 65, 40, 200, 45, 85),
            mean1=c(92.0, 92.0, 88.0, 82.0, 88.0, 92.0),
            sd1=c(20.0, 22.0, 26.0, 17.0, 22.0, 22.0),
            N2=c(60, 65, 40, 200, 50, 85),
            mean2=c(94.0, 98.0, 98.0, 94.0, 98.0, 96.0),
            sd2=c(22.0, 21.0, 28.0, 19.0, 21.0, 21.0),
            y=c(
                -0.0945241585203, -0.277355866266, -0.366544429516,
                -0.664385099891, -0.461806281288, -0.185164437399
            ),
            SE=c(
                0.182676111563, 0.176252946255, 0.225476645393, 0.102721757438,
                0.208193827499, 0.153721347104
            ),
            study.names=c(
                "Carroll, 1997", "Grant, 1981", "Peck, 1987", "Donat, 2003",
                "Stewart, 1990", "Young, 1995"
            ),
            years=c(
                as.integer(), as.integer(), as.integer(), as.integer(),
                as.integer(), as.integer()
            ),
            covariates=list(
                new(
                    'CovariateValues',
                    cov.name='STATE',
                    cov.vals=c("MA", "MA", "MA", "RI", "RI", "RI"),
                    cov.type='factor',
                    ref.var='MA'
                )
            )
        )
        '''

        python_to_R.exR.execute_in_R(r_str)

    def _setup_bootstrap_data(self):
        r_str = '''
        tmp_obj <- new(
            'ContinuousData',
            N1=c(60, 65, 40, 200, 45, 85),
            mean1=c(92.0, 92.0, 88.0, 82.0, 88.0, 92.0),
            sd1=c(20.0, 22.0, 26.0, 17.0, 22.0, 22.0),
            N2=c(60, 65, 40, 200, 50, 85),
            mean2=c(94.0, 98.0, 98.0, 94.0, 98.0, 96.0),
            sd2=c(22.0, 21.0, 28.0, 19.0, 21.0, 21.0),
            y=c(
                -0.0945241585203, -0.277355866266, -0.366544429516,
                -0.664385099891, -0.461806281288, -0.185164437399
            ),
            SE=c(
                0.182676111563, 0.176252946255, 0.225476645393, 0.102721757438,
                0.208193827499, 0.153721347104
            ),
            study.names=c(
                "Carroll, 1997", "Grant, 1981", "Peck, 1987", "Donat, 2003",
                "Stewart, 1990", "Young, 1995"
            ),
            years=c(
                as.integer(), as.integer(), as.integer(), as.integer(),
                as.integer(), as.integer()
            ),
            covariates=list())
        '''

        python_to_R.exR.execute_in_R(r_str)

    def _cum_full_expected_results(self):
        results = {
            'image_order': None,
            'image_var_names': {'Cumulative Forest Plot': 'r_tmp/1462159028.22232'},
            'save_plot_functions': {},
            'texts': {'Cumulative Summary': 'Continuous Random-Effects Model\n\nMetric: Standardized Mean Difference\n\n Model Results\n\n Studies          Estimate   Lower bound   Upper bound   Std. error    p-Val   \n\n Carroll, 1997     -0.095      -0.453         0.264         0.183        NA    \n\n + Grant, 1981     -0.189      -0.438         0.059         0.127      0.136   \n\n + Peck, 1987      -0.232      -0.449        -0.015         0.111      0.036   \n\n + Donat, 2003     -0.376      -0.660        -0.091         0.145      0.010   \n\n + Stewart, 1990   -0.397      -0.626        -0.169         0.116     < 0.001  \n\n + Young, 1995     -0.358      -0.565        -0.152         0.105     < 0.001  \n\n\n'},
            'image_params_paths': {},
            'results_data': [
                ('summary.table', {
                    'type': 'data.frame',
                    'description': '',
                    'value': '     estimate        se      zval         pval      ci.lb       ci.ub         QE        QEp       tau2       I2       H2\n1 -0.09452416 0.1826761        NA           NA -0.4525628  0.26351444         NA         NA         NA       NA       NA\n2 -0.18921080 0.1268396 -1.491732 0.1357692977 -0.4378119  0.05939032  0.5187722 0.47136588 0.00000000  0.00000 1.000000\n3 -0.23183863 0.1105484 -2.097168 0.0359787158 -0.4485096 -0.01516768  0.9886385 0.60998601 0.00000000  0.00000 1.000000\n4 -0.37551497 0.1449767 -2.590174 0.0095927422 -0.6596641 -0.09136579  9.2044548 0.02669251 0.05510402 67.40709 3.068152\n5 -0.39732795 0.1164982 -3.410594 0.0006482153 -0.6256602 -0.16899574  9.2045498 0.05618519 0.03707059 56.54323 2.301137\n6 -0.35849726 0.1054538 -3.399566 0.0006749280 -0.5651829 -0.15181157 11.9138479 0.03598752 0.03723544 58.03203 2.382770\n'}
                )],
            'images': {'Cumulative Forest Plot': './r_tmp/forest.png'}
        }

        return results

    def _loo_full_expected_results(self):
        results = {
            'image_order': None,
            'image_var_names': {'Leave-one-out Forest Plot': 'r_tmp/1462159093.92416'},
            'save_plot_functions': {},
            'texts': {
                'Leave-one-out Summary': 'Continuous Random-Effects Model\n\nMetric: Standardized Mean Difference\n\n Model Results\n\n Studies          Estimate   Lower bound   Upper bound   Std. error    p-Val   \n\n Overall           -0.358      -0.565        -0.152         0.105     < 0.001  \n\n - Carroll, 1997   -0.411      -0.621        -0.202         0.107     < 0.001  \n\n - Grant, 1981     -0.370      -0.615        -0.126         0.125      0.003   \n\n - Peck, 1987      -0.353      -0.593        -0.113         0.122      0.004   \n\n - Donat, 2003     -0.254      -0.416        -0.093         0.082      0.002   \n\n - Stewart, 1990   -0.337      -0.580        -0.094         0.124      0.007   \n\n - Young, 1995     -0.397      -0.626        -0.169         0.116     < 0.001  \n\n\n',  
            },
            'image_params_paths': {},
            'results_data': [
                ('summary.table', {
                        'type': 'data.frame',
                        'description': '',
                        'value': '    estimate         se      zval         pval      ci.lb       ci.ub         Q         Qp       tau2       I2       H2\n1 -0.3584973 0.10545382 -3.399566 0.0006749280 -0.5651829 -0.15181157 11.913848 0.03598752 0.03723544 58.03203 2.382770\n2 -0.4114342 0.10699571 -3.845333 0.0001203888 -0.6211419 -0.20172642  8.401100 0.07794237 0.02895657 52.38719 2.100275\n3 -0.3704578 0.12473111 -2.970052 0.0029774957 -0.6149263 -0.12598937 11.210371 0.02429874 0.04813708 64.31876 2.802593\n4 -0.3534015 0.12249925 -2.884928 0.0039150302 -0.5934957 -0.11330741 11.863574 0.01839513 0.04831155 66.28335 2.965894\n5 -0.2544609 0.08241803 -3.087443 0.0020188677 -0.4159973 -0.09292457  2.225595 0.69434623 0.00000000  0.00000 1.000000\n6 -0.3370921 0.12416044 -2.714972 0.0066281404 -0.5804421 -0.09374211 11.857982 0.01843919 0.04938846 66.26745 2.964495\n7 -0.3973279 0.11649816 -3.410594 0.0006482153 -0.6256602 -0.16899574  9.204550 0.05618519 0.03707059 56.54323 2.301137\n'}
                )],
            'images': {'Leave-one-out Forest Plot': './r_tmp/forest.png'}
        }

        return results

    def _subgroup_full_expected_results(self):
        results = {
            'image_order': None,
            'image_var_names': {'Subgroups Forest Plot': 'r_tmp/1462159148.32582'},
            'save_plot_functions': {},
            'texts': {
                'Subgroup Summary': 'Continuous Random-Effects Model\n\nMetric: Standardized Mean Difference\n\n Model Results\n\n Studies      Estimate   Lower bound   Upper bound   Std. error    p-Val   \n\n Subgroup MA   -0.232      -0.449        -0.015         0.111      0.036   \n\n Subgroup RI   -0.451      -0.765        -0.137         0.160      0.005   \n\n Overall       -0.358      -0.565        -0.152         0.105     < 0.001  \n\n\n', 
            },
            'image_params_paths': {},
            'results_data': [
                ('__Subgroup MA', {'type': 'label', 'description': '', 'value': '######################################'}),
                ('b', {'type': 'vector', 'description': 'estimated coefficients of the model.', 'value': [-0.23183862796808252]}),
                ('se', {'type': 'vector', 'description': 'standard errors of the coefficients.', 'value': [0.11054843486383627]}),
                ('zval', {'type': 'vector', 'description': 'test statistics of the coefficients.', 'value': [-2.0971678907407485]}),
                ('pval', {'type': 'vector', 'description': 'p-values for the test statistics.', 'value': [0.035978715810442374]}),
                ('ci.lb', {'type': 'vector', 'description': 'lower bound of the confidence intervals for the coefficients.', 'value': [-0.44850957884847364]}),
                ('ci.ub', {'type': 'vector', 'description': 'upper bound of the confidence intervals for the coefficients.', 'value': [-0.0151676770876914]}),
                ('vb', {'type': 'vector', 'description': 'variance-covariance matrix of the estimated coefficients.', 'value': [0.01222095645084385]}),
                ('tau2', {'type': 'vector', 'description': 'estimated amount of (residual) heterogeneity. Always 0 when method="FE".', 'value': [0.0]}),
                ('se.tau2', {'type': 'vector', 'description': 'estimated standard error of the estimated amount of (residual) heterogeneity.', 'value': [0.03741085701470231]}),
                ('k', {'type': 'vector', 'description': 'number of outcomes included in the model fitting.', 'value': [3]}),
                ('p', {'type': 'vector', 'description': 'number of coefficients in the model (including the intercept).', 'value': [1]}),
                ('m', {'type': 'vector', 'description': 'number of coefficients included in the omnibus test of coefficients.', 'value': [1]}),
                ('QE', {'type': 'vector', 'description': 'test statistic for the test of (residual) heterogeneity.', 'value': [0.9886385060531218]}),
                ('QEp', {'type': 'vector', 'description': 'p-value for the test of (residual) heterogeneity.', 'value': [0.6099860121211939]}),
                ('QM', {'type': 'vector', 'description': 'test statistic for the omnibus test of coefficients.', 'value': [4.398113161954]}),
                ('QMp', {'type': 'vector', 'description': 'p-value for the omnibus test of coefficients.', 'value': [0.03597871581044249]}),
                ('I2', {'type': 'vector', 'description': 'value of I2. See print.rma.uni for more details.', 'value': [0.0]}),
                ('H2', {'type': 'vector', 'description': 'value of H2. See print.rma.uni for more details.', 'value': [1.0]}),
                ('R2', {'type': 'vector', 'description': 'value of R2. See print.rma.uni for more details.', 'value': 'NULL'}),
                ('int.only', {'type': 'vector', 'description': 'logical that indicates whether the model is an intercept-only model.', 'value': [True]}),
                ('yi', {'type': 'vector', 'description': 'the vector of outcomes', 'value': [-0.0945241585203, -0.277355866266, -0.366544429516]}),
                ('vi', {'type': 'vector', 'description': 'the corresponding sample variances', 'value': [0.033370561735777626, 0.031065101063567913, 0.05083971761768067]}),
                ('X', {'type': 'matrix', 'description': 'the model matrix of the model', 'value': '     intrcpt\n[1,]       1\n[2,]       1\n[3,]       1\n'}),
                ('fit.stats', {'type': 'data.frame', 'description': 'a list with the log-likelihood, deviance, AIC, BIC, and AICc values under the unrestricted and restricted likelihood.', 'value': '             ML       REML\nll    1.6742795  0.9402227\ndev   0.9886385 -1.8804454\nAIC   0.6514409  2.1195546\nBIC  -1.1513345 -0.4941510\nAICc 12.6514409 14.1195546\n'}),
                ('weights', {'type': 'vector', 'description': 'weights in % given to the observed effects', 'value': [36.62196803160608, 39.33982518143542, 24.038206786958504]}),
                ('__Subgroup RI', {'type': 'label', 'description': '', 'value': '######################################'}),
                ('b', {'type': 'vector', 'description': 'estimated coefficients of the model.', 'value': [-0.4509453099130886]}),
                ('se', {'type': 'vector', 'description': 'standard errors of the coefficients.', 'value': [0.1601494603147735]}),
                ('zval', {'type': 'vector', 'description': 'test statistics of the coefficients.', 'value': [-2.8157778928930286]}),
                ('pval', {'type': 'vector', 'description': 'p-values for the test statistics.', 'value': [0.004865929397759372]}),
                ('ci.lb', {'type': 'vector', 'description': 'lower bound of the confidence intervals for the coefficients.', 'value': [-0.7648324842735713]}),
                ('ci.ub', {'type': 'vector', 'description': 'upper bound of the confidence intervals for the coefficients.', 'value': [-0.13705813555260593]}),
                ('vb', {'type': 'vector', 'description': 'variance-covariance matrix of the estimated coefficients.', 'value': [0.025647849639113214]}),
                ('tau2', {'type': 'vector', 'description': 'estimated amount of (residual) heterogeneity. Always 0 when method="FE".', 'value': [0.05333381843718102]}),
                ('se.tau2', {'type': 'vector', 'description': 'estimated standard error of the estimated amount of (residual) heterogeneity.', 'value': [0.07817603127010604]}),
                ('k', {'type': 'vector', 'description': 'number of outcomes included in the model fitting.', 'value': [3]}),
                ('p', {'type': 'vector', 'description': 'number of coefficients in the model (including the intercept).', 'value': [1]}),
                ('m', {'type': 'vector', 'description': 'number of coefficients included in the omnibus test of coefficients.', 'value': [1]}),
                ('QE', {'type': 'vector', 'description': 'test statistic for the test of (residual) heterogeneity.', 'value': [6.777488573474647]}),
                ('QEp', {'type': 'vector', 'description': 'p-value for the test of (residual) heterogeneity.', 'value': [0.03375103191953712]}),
                ('QM', {'type': 'vector', 'description': 'test statistic for the omnibus test of coefficients.', 'value': [7.928605142105104]}),
                ('QMp', {'type': 'vector', 'description': 'p-value for the omnibus test of coefficients.', 'value': [0.00486592939775937]}),
                ('I2', {'type': 'vector', 'description': 'value of I2. See print.rma.uni for more details.', 'value': [70.49054412533447]}),
                ('H2', {'type': 'vector', 'description': 'value of H2. See print.rma.uni for more details.', 'value': [3.3887442867373236]}),
                ('R2', {'type': 'vector', 'description': 'value of R2. See print.rma.uni for more details.', 'value': 'NULL'}),
                ('int.only', {'type': 'vector', 'description': 'logical that indicates whether the model is an intercept-only model.', 'value': [True]}),
                ('yi', {'type': 'vector', 'description': 'the vector of outcomes', 'value': [-0.664385099891, -0.461806281288, -0.185164437399]}),
                ('vi', {'type': 'vector', 'description': 'the corresponding sample variances', 'value': [0.010551759451151306, 0.04334466980868337, 0.023630252555468453]}),
                ('X', {'type': 'matrix', 'description': 'the model matrix of the model', 'value': '     intrcpt\n[1,]       1\n[2,]       1\n[3,]       1\n'}),
                ('fit.stats', {'type': 'data.frame', 'description': 'a list with the log-likelihood, deviance, AIC, BIC, and AICc values under the unrestricted and restricted likelihood.', 'value': '             ML       REML\nll    0.2528357 -0.1105674\ndev   5.4159592  0.2211349\nAIC   3.4943287  4.2211349\nBIC   1.6915532  1.6074292\nAICc 15.4943287 16.2211349\n'}),
                ('weights', {'type': 'vector', 'description': 'weights in % given to the observed effects', 'value': [40.14654087334693, 26.529013955915225, 33.324445170737846]}),
                ('__Overall', {'type': 'label', 'description': '', 'value': '######################################'}),
                ('b', {'type': 'vector', 'description': 'estimated coefficients of the model.', 'value': [-0.35849725582231895]}),
                ('se', {'type': 'vector', 'description': 'standard errors of the coefficients.', 'value': [0.1054538186189239]}),
                ('zval', {'type': 'vector', 'description': 'test statistics of the coefficients.', 'value': [-3.399566374336926]}),
                ('pval', {'type': 'vector', 'description': 'p-values for the test statistics.', 'value': [0.0006749279631807544]}),
                ('ci.lb', {'type': 'vector', 'description': 'lower bound of the confidence intervals for the coefficients.', 'value': [-0.5651829423476291]}),
                ('ci.ub', {'type': 'vector', 'description': 'upper bound of the confidence intervals for the coefficients.', 'value': [-0.15181156929700873]}),
                ('vb', {'type': 'vector', 'description': 'variance-covariance matrix of the estimated coefficients.', 'value': [0.011120507861312903]}),
                ('tau2', {'type': 'vector', 'description': 'estimated amount of (residual) heterogeneity. Always 0 when method="FE".', 'value': [0.03723543730128842]}),
                ('se.tau2', {'type': 'vector', 'description': 'estimated standard error of the estimated amount of (residual) heterogeneity.', 'value': [0.042114565809081704]}),
                ('k', {'type': 'vector', 'description': 'number of outcomes included in the model fitting.', 'value': [6]}),
                ('p', {'type': 'vector', 'description': 'number of coefficients in the model (including the intercept).', 'value': [1]}),
                ('m', {'type': 'vector', 'description': 'number of coefficients included in the omnibus test of coefficients.', 'value': [1]}),
                ('QE', {'type': 'vector', 'description': 'test statistic for the test of (residual) heterogeneity.', 'value': [11.913847853272857]}),
                ('QEp', {'type': 'vector', 'description': 'p-value for the test of (residual) heterogeneity.', 'value': [0.03598752428191084]}),
                ('QM', {'type': 'vector', 'description': 'test statistic for the omnibus test of coefficients.', 'value': [11.557051533522314]}),
                ('QMp', {'type': 'vector', 'description': 'p-value for the omnibus test of coefficients.', 'value': [0.0006749279631807537]}),
                ('I2', {'type': 'vector', 'description': 'value of I2. See print.rma.uni for more details.', 'value': [58.03203077982528]}),
                ('H2', {'type': 'vector', 'description': 'value of H2. See print.rma.uni for more details.', 'value': [2.3827695706545713]}),
                ('R2', {'type': 'vector', 'description': 'value of R2. See print.rma.uni for more details.', 'value': 'NULL'}),
                ('int.only', {'type': 'vector', 'description': 'logical that indicates whether the model is an intercept-only model.', 'value': [True]}),
                ('yi', {'type': 'vector', 'description': 'the vector of outcomes', 'value': [-0.0945241585203, -0.277355866266, -0.366544429516, -0.664385099891, -0.461806281288, -0.185164437399]}),
                ('vi', {'type': 'vector', 'description': 'the corresponding sample variances', 'value': [0.033370561735777626, 0.031065101063567913, 0.05083971761768067, 0.010551759451151306, 0.04334466980868337, 0.023630252555468453]}),
                ('X', {'type': 'matrix', 'description': 'the model matrix of the model', 'value': '     intrcpt\n[1,]       1\n[2,]       1\n[3,]       1\n[4,]       1\n[5,]       1\n[6,]       1\n'}),
                ('fit.stats', {'type': 'data.frame', 'description': 'a list with the log-likelihood, deviance, AIC, BIC, and AICc values under the unrestricted and restricted likelihood.', 'value': '            ML       REML\nll   0.7136296  0.2789657\ndev  8.8315690 -0.5579313\nAIC  2.5727409  3.4420687\nBIC  2.1562598  2.6609445\nAICc 6.5727409  9.4420687\n'}),
                ('weights', {'type': 'vector', 'description': 'weights in % given to the observed effects', 'value': [15.750089245922238, 16.28172797395532, 12.626157594095625, 23.270893915209943, 13.800562272939368, 18.27056899787751]})
            ],
            'images': {'Subgroups Forest Plot': './r_tmp/forest.png'}
        }

        return results

    def _bootstrap_full_expected_results(self):
        results = {
            'image_order': None,
            'image_var_names': {},
            'save_plot_functions': {},
            'texts': {
                'Summary': 'The 95% Confidence Interval: [-0.554, -0.19]\nThe observed value of the effect size was -0.358, while the mean over the replicates was -0.345.'},
                'image_params_paths': {},
                'results_data': [
                    ('Summary', {'type': 'blob', 'description': '', 'value': '[1] "The 95% Confidence Interval: [-0.554, -0.19]\\nThe observed value of the effect size was -0.358, while the mean over the replicates was -0.345."\n'}),
                    ('t', {'type': 'matrix', 'description': 'A matrix with #replicates rows, each of which is a bootstrap replicate', 'value': '             [,1]\n  [1,] -0.2302012\n  [2,] -0.4184438\n  [3,] -0.4347124\n  [4,] -0.2585689\n  [5,] -0.3396847\n  [6,] -0.4347124\n  [7,] -0.2771395\n  [8,] -0.3594981\n  [9,] -0.3001969\n [10,] -0.3937101\n [11,] -0.3805454\n [12,] -0.4482880\n [13,] -0.3735779\n [14,] -0.4284900\n [15,] -0.3132265\n [16,] -0.2248503\n [17,] -0.2606362\n [18,] -0.2461854\n [19,] -0.3912389\n [20,] -0.2047695\n [21,] -0.5052002\n [22,] -0.2729712\n [23,] -0.4392815\n [24,] -0.3396847\n [25,] -0.2204164\n [26,] -0.2214600\n [27,] -0.3115000\n [28,] -0.2477373\n [29,] -0.1896892\n [30,] -0.3584973\n [31,] -0.3396847\n [32,] -0.1907797\n [33,] -0.4289649\n [34,] -0.2439954\n [35,] -0.3854014\n [36,] -0.3718429\n [37,] -0.3990686\n [38,] -0.4223145\n [39,] -0.2745522\n [40,] -0.3873510\n [41,] -0.2676714\n [42,] -0.3216578\n [43,] -0.2816691\n [44,] -0.2274112\n [45,] -0.3805454\n [46,] -0.4111363\n [47,] -0.3092504\n [48,] -0.2092832\n [49,] -0.3584973\n [50,] -0.3448428\n [51,] -0.3805454\n [52,] -0.3599910\n [53,] -0.2389887\n [54,] -0.2816752\n [55,] -0.3718429\n [56,] -0.6000563\n [57,] -0.3584973\n [58,] -0.3249589\n [59,] -0.3735779\n [60,] -0.3013142\n [61,] -0.3854014\n [62,] -0.4794101\n [63,] -0.3126637\n [64,] -0.2878125\n [65,] -0.4614713\n [66,] -0.2955435\n [67,] -0.4458280\n [68,] -0.3594981\n [69,] -0.3112254\n [70,] -0.3285209\n [71,] -0.5547973\n [72,] -0.1615770\n [73,] -0.2825526\n [74,] -0.1609691\n [75,] -0.4794101\n [76,] -0.4478744\n [77,] -0.3072409\n [78,] -0.5893392\n [79,] -0.3594534\n [80,] -0.3255938\n [81,] -0.1761371\n [82,] -0.3813762\n [83,] -0.4165194\n [84,] -0.5167383\n [85,] -0.3255938\n [86,] -0.3309089\n [87,] -0.3735779\n [88,] -0.3192089\n [89,] -0.2461854\n [90,] -0.3264070\n [91,] -0.4165194\n [92,] -0.5222913\n [93,] -0.3013142\n [94,] -0.3072409\n [95,] -0.4615603\n [96,] -0.1739143\n [97,] -0.3982769\n [98,] -0.3990686\n [99,] -0.4239174\n[100,] -0.3731900\n'})
                ],
            'images': {'Histogram': './r_tmp/bootstrap.png'}
        }

        return results

    def test_run_meta_method_cumulative(self):
        self._setup_cum_data()

        # prepare parameters
        meta_function_name = 'cum.ma.continuous'
        function_name = 'continuous.random'
        params = {
            'conf.level': 95.0,
            'digits': 3,
            'fp_col2_str': u'[default]',
            'fp_show_col4': False,
            'fp_xlabel': u'[default]',
            'fp_col4_str': u'Ev/Ctrl',
            'fp_xticks': '[default]',
            'fp_col3_str': u'Ev/Trt',
            'fp_show_col3': False,
            'fp_show_col2': True,
            'fp_show_col1': True,
            'fp_plot_lb': '[default]',
            'fp_outpath': u'./r_tmp/forest.png',
            'rm.method': 'DL',
            'fp_plot_ub': '[default]',
            'fp_col1_str': u'Studies',
            'measure': 'SMD',
            'fp_show_summary_line': True
        }
        res_name = 'result'
        data_name = 'tmp_obj'

        result = python_to_R.run_meta_method(
            meta_function_name=meta_function_name,
            function_name=function_name,
            params=params,
            res_name="result",
            data_name="tmp_obj",
        )

        expected_result = self._cum_full_expected_results()

        self.ObservedResultsDataMatchesExpected(
            expected_result=expected_result,
            observed_result=result,
        )

    def test_run_meta_method_loo(self):
        self._setup_loo_data()

        # prepare parameters
        meta_function_name = 'loo.ma.continuous'
        function_name = 'continuous.random'
        params = {
            'conf.level': 95.0,
            'digits': 3,
            'fp_col2_str': u'[default]',
            'fp_show_col4': False,
            'fp_xlabel': u'[default]',
            'fp_col4_str': u'Ev/Ctrl',
            'fp_xticks': '[default]',
            'fp_col3_str': u'Ev/Trt',
            'fp_show_col3': False,
            'fp_show_col2': True,
            'fp_show_col1': True,
            'fp_plot_lb': '[default]',
            'fp_outpath': u'./r_tmp/forest.png',
            'rm.method': 'DL',
            'fp_plot_ub': '[default]',
            'fp_col1_str': u'Studies',
            'measure': 'SMD',
            'fp_show_summary_line': True
        }
        res_name = 'result'
        data_name = 'tmp_obj'

        result = python_to_R.run_meta_method(
            meta_function_name=meta_function_name,
            function_name=function_name,
            params=params,
            res_name="result",
            data_name="tmp_obj",
        )

        expected_result = self._loo_full_expected_results()

        self.ObservedResultsDataMatchesExpected(
            expected_result=expected_result,
            observed_result=result,
        )

    def test_run_meta_method_subgroup(self):
        self._setup_subgroup_data()

        # prepare parameters
        meta_function_name = 'subgroup.ma.continuous'
        function_name = 'continuous.random'
        params = {
            'conf.level': 95.0,
            'digits': 3,
            'fp_col2_str': u'[default]',
            'fp_show_col4': False,
            'fp_xlabel': u'[default]',
            'fp_col4_str': u'Ev/Ctrl',
            'fp_xticks': '[default]',
            'fp_col3_str': u'Ev/Trt',
            'fp_show_col3': False,
            'fp_show_col2': True,
            'fp_show_col1': True,
            'fp_plot_lb': '[default]',
            'fp_outpath': u'./r_tmp/forest.png',
            'rm.method': 'DL',
            'fp_plot_ub': '[default]',
            'fp_col1_str': u'Studies',
            'cov_name': 'STATE',
            'measure': 'SMD',
            'fp_show_summary_line': True
        }
        res_name = 'result'
        data_name = 'tmp_obj'

        result = python_to_R.run_meta_method(
            meta_function_name=meta_function_name,
            function_name=function_name,
            params=params,
            res_name="result",
            data_name="tmp_obj",
        )

        expected_result = self._subgroup_full_expected_results()

        self.ObservedResultsDataMatchesExpected(
            expected_result=expected_result,
            observed_result=result,
        )

    def test_run_meta_method_bootstrap(self):
        self._setup_bootstrap_data()

        # prepare parameters
        meta_function_name = 'bootstrap.continuous'
        function_name = 'continuous.random'
        params = {
            'conf.level': 95.0,
            'histogram.xlab': 'Effect Size',
            'fp_xticks': '[default]',
            'fp_show_col4': False,
            'fp_show_col3': False,
            'fp_xlabel': u'[default]',
            'fp_show_col1': True,
            'fp_show_col2': True,
            'fp_outpath': u'./r_tmp/forest.png',
            'rm.method': 'DL',
            'fp_plot_ub': '[default]',
            'fp_col1_str': u'Studies',
            'measure': 'SMD',
            'fp_plot_lb': '[default]',
            'bootstrap.plot.path': './r_tmp/bootstrap.png',
            'digits': 3,
            'fp_col2_str': u'[default]',
            'num.bootstrap.replicates': 100,
            'fp_col4_str': u'Ev/Ctrl',
            'histogram.title': 'Bootstrap Histogram',
            'fp_col3_str': u'Ev/Trt',
            'fp_show_summary_line': True,
            'bootstrap.type': 'boot.ma'
        }
        res_name = 'result'
        data_name = 'tmp_obj'

        result = python_to_R.run_meta_method(
            meta_function_name=meta_function_name,
            function_name=function_name,
            params=params,
            res_name="result",
            data_name="tmp_obj",
        )

        expected_result = self._bootstrap_full_expected_results()

        self.ObservedResultsDataMatchesExpected(
            expected_result=expected_result,
            observed_result=result,
        )

        # we are basically just asserting that the plot exists here!
        image_name, image_path = result['images'].items()[0]
        self.assertTrue(image_name == "Histogram")
        self.assertTrue( os.path.isfile(image_path))


# TODO: FUNCTIONS THAT WE STILL NEED TO WRITE UNIT TESTS FOR

# def run_failsafe_analysis(

# def run_model_building(
# def run_multiple_imputation_meta_analysis(

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
import python_to_R


import unittest
import ome_globals
import os, os.path


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
        

        for j in range(len(result['results_data'])):
            print "checking %s" % result['results_data'][j][0]

            observed_val = result['results_data'][j][1]['value']
            expected_val = full_expected_result['results_data'][j][1]['value']

            if type(observed_val) == type([]):
                for idx in range(len(observed_val)):
                    self.assertAlmostEqual(observed_val[idx], expected_val[idx])
            else:
                self.assertAlmostEqual(observed_val, expected_val)
            print "ok!"


class TestContinuousMetaAnalysis(unittest.TestCase):
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
                'References': '1. this is a placeholder for binary random reference\n2. metafor: Viechtbauer, Wolfgang. "Conducting meta-analyses in R with the metafor package." Journal of 36 (2010).\n3. OpenMetaAnalyst: Wallace, Byron C., Issa J. Dahabreh, Thomas A. Trikalinos, Joseph Lau, Paul Trow, and Christopher H. Schmid. "Closing the Gap between Methodologists and End-Users: R as a Computational Back-End." Journal of Statistical Software 49 (2012): 5."\n',
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


        for j in range(len(result['results_data'])):
            print "checking %s" % result['results_data'][j][0]

            observed_val = result['results_data'][j][1]['value']
            expected_val = full_expected_result['results_data'][j][1]['value']
            
            if type(observed_val) == type([]):
                for idx in range(len(observed_val)):
                    self.assertAlmostEqual(observed_val[idx], expected_val[idx])
            else:
                self.assertAlmostEqual(observed_val, expected_val)


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


class TestHistogram(unittest.TestCase):
    pass 

    
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
        image_name, image_path =  results['images'].items()[0]
        self.assertTrue(image_name == "Funnel Plot")
        self.assertTrue( os.path.isfile(image_path))



# TODO: FUNCTIONS THAT WE STILL NEED TO WRITE UNIT TESTS FOR



# def run_dynamic_data_exploration_analysis(
# def run_failsafe_analysis(
# def run_funnelplot_analysis(
# def run_gmeta_regression(

# def run_gmeta_regression_bootstrapped_cond_means(
# def run_gmeta_regression_cond_means(
# def run_histogram(
# def run_meta_method(

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
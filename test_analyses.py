import nose
from nose import with_setup, tools
import os, sys, time

from PyQt4 import QtCore, QtGui, Qt
from PyQt4.Qt import *


#import meta_py_r # this needs to come first or else weird stuff happens w/ nose
#import meta_globals

print("Importing meta_globals")
import globals
#print("Importing meta_form")
import launch
import main_form
print("Importing meta_py_r")
import python_to_R

app,form = None, None
bar = None


def setup_module(module):
    print("Launching Nose Test setup module for test_analyses")
    
    SPLASH_DISPLAY_TIME = 0
    
    global app, form, bar
    
    app = QtGui.QApplication(sys.argv)
    
    splash_pixmap = QPixmap(":/splash/nose_splash.png")
    splash = QSplashScreen(splash_pixmap)
    splash.show()
    splash.raise_()
    splash_starttime = time.time()
    globals.moment.play()
    
    launch.load_R_libraries(app, splash)
    
    
    # Show splash screen for at least SPLASH_DISPLAY_TIME seconds
    time_elapsed  = time.time() - splash_starttime
    print("It took %s seconds to load the R libraries" % str(time_elapsed))
    if time_elapsed < SPLASH_DISPLAY_TIME: # seconds
        print("Going to sleep for %f seconds" % float(SPLASH_DISPLAY_TIME-time_elapsed))
        QThread.sleep(int(SPLASH_DISPLAY_TIME-time_elapsed))
        print("woke up")

    form = main_form.MainForm()
    splash.finish(form)
    form.show()
    
    
    fullpath = os.path.join(os.getcwd(),"sample_data", "test_dataset.ome")
    form.open(fullpath)
    app.processEvents() #show the data
    
    bar = main_form.MetaProgress("Running self-tests")
    bar.show()

def teardown_module():
    bar.hide()
    QApplication.quit()
    
def test_dummy():
    print("Running test dummy")
    assert True
    
def test_generator():
    regular_test_data = [ # can test the actual numerical results
        {
         'test_name'          : "Binary Meta Analysis"
        ,'fnc_to_evaluate'    : 'python_to_R.run_binary_ma'
        ,'make_dataset_r_str' : "tmp_obj <- new('BinaryData', g1O1=c(30, 56, 5, 63, 5, 52, 56, 6, 43, 5, 55, 33, 8, 5, 56, 111, 23, 76, 89, 10, 123, 32, 119, 46, 32, 22, 28, 52, 99), g1O2=c(40, 654, 2, 25, 6, 45, 5, 56, 13, 52, 2, 93, 2, 10, 15, 21, 12, 115, 83, 46, 23, 24, 32, 109, 42, 51, 19, 117, 102), g2O1=c(10, 13, 104, 51, 13, 11, 31, 32, 52, 111, 51, 10, 68, 72, 129, 15, 2, 46, 2, 83, 56, 54, 82, 111, 125, 109, 63, 6, 83), g2O2=c(20, 4, 7, 54, 8, 34, 32, 23, 3, 33, 3, 50, 72, 84, 41, 22, 78, 55, 82, 66, 77, 125, 29, 9, 64, 49, 74, 120, 32),                             y=c(0.4055, -3.6364, -1.7822, 0.9814, -0.6678, 1.273, 2.4477, -2.5638, -1.6564, -3.5548, 0.481, 0.5733, 1.4435, -0.539, 0.1711, 2.048, 4.3141, -0.2355, 3.7834, -1.7552, 1.9951, 1.127, 0.274, -3.375, -0.9414, -1.6403, 0.5487, 2.1848, -0.983), SE=c(0.45639894829, 0.588472599192, 0.923309265631, 0.306594194335, 0.75405570086, 0.402243707222, 0.530471488395, 0.509215082259, 0.67282984476, 0.508428952755, 0.933327380933, 0.401372644808, 0.808455317256, 0.570788927713, 0.341613817051, 0.410731055558, 0.799749960925, 0.248596057893, 0.731778655059, 0.385875627631, 0.287228132327, 0.315277655409, 0.293768616431, 0.388587184555, 0.280535202782, 0.307571129985, 0.343074335968, 0.450333209968, 0.2513961018), study.names=c('George', 'Byron', 'Issa', 'Tom', 'Big Chris', 'Little Chris', 'Jens', 'Anja', 'Hailee', 'Joseph', 'Meghan', 'Medium Chris', 'Superman', 'Batman', 'Leonardo', 'Michaelangelo', 'Donatello', 'Raphael', 'The Hulk', 'Professor X', 'Cyclops', 'Storm', 'Rogue', 'Wolverine', 'Gambit', 'Spiderman', 'Mr. Fantastic', 'The Flash', 'Thor'), years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer()), covariates=list())"
        ,'results'            : {'images': {'Forest Plot': './r_tmp/forest.png'}, 'texts': {'References': '1. this is a placeholder for binary random reference\n2. metafor: Viechtbauer, Wolfgang. "Conducting meta-analyses in R with the metafor package." Journal of 36 (2010).\n3. OpenMetaAnalyst: Wallace, Byron C., Issa J. Dahabreh, Thomas A. Trikalinos, Joseph Lau, Paul Trow, and Christopher H. Schmid. "Closing the Gap between Methodologists and End-Users: R as a Computational Back-End." Journal of Statistical Software 49 (2012): 5."\n', 'Weights': u'studies       weights\nGeorge         3.5%\nByron          3.4%\nIssa           2.9%\nTom            3.7%\nBig Chris      3.1%\nLittle Chris   3.6%\nJens           3.4%\nAnja           3.5%\nHailee         3.2%\nJoseph         3.5%\nMeghan         2.8%\nMedium Chris   3.6%\nSuperman       3.0%\nBatman         3.4%\nLeonardo       3.6%\nMichaelangelo  3.6%\nDonatello      3.1%\nRaphael        3.7%\nThe Hulk       3.2%\nProfessor X    3.6%\nCyclops        3.7%\nStorm          3.7%\nRogue          3.7%\nWolverine      3.6%\nGambit         3.7%\nSpiderman      3.7%\nMr. Fantastic  3.6%\nThe Flash      3.5%\nThor           3.7%\n', 'Summary': 'Binary Random-Effects Model\n\nMetric: Odds Ratio\n\n Model Results\n\n Estimate  Lower bound   Upper bound   p-Value  \n\n 1.0084       0.5435        1.8707      0.9789  \n\n\n Heterogeneity\n\n tau^2   Q(df=28)   Het. p-Value   I^2  \n\n 2.6196  492.2579     < 1e-04      94%  \n\n\n Results (log scale)\n\n Estimate  Lower bound   Upper bound   Std. error  \n\n 0.0083      -0.6097        0.6263       0.3153    \n\n\n'}, 'image_var_names': {'forest plot': 'forest_plot'}, 'image_params_paths': {'Forest Plot': 'r_tmp/1382043049.54824'}, 'image_order': None}
        ,'params'             : {'conf.level': 95.0, 'digits': 4, 'fp_col2_str': u'[default]', 'fp_show_col4': True, 'to': 'only0', 'fp_col4_str': u'Ev/Ctrl', 'fp_xticks': '[default]', 'fp_col3_str': u'Ev/Trt', 'fp_show_col3': True, 'fp_show_col2': True, 'fp_show_col1': True, 'fp_plot_lb': '[default]', 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'adjust': 0.5, 'fp_plot_ub': '[default]', 'fp_col1_str': u'Studies', 'measure': 'OR', 'fp_xlabel': u'[default]', 'fp_show_summary_line': True}
        ,'function_name'      : 'binary.random'
        },
        
        {
         'test_name'          : "Binary Cumulative Meta Analysis"
        ,'fnc_to_evaluate'    : 'python_to_R.run_meta_method'
        ,'make_dataset_r_str' : "tmp_obj <- new('BinaryData', g1O1=c(30, 56, 5, 63, 5, 52, 56, 6, 43, 5, 55, 33, 8, 5, 56, 111, 23, 76, 89, 10, 123, 32, 119, 46, 32, 22, 28, 52, 99), g1O2=c(40, 654, 2, 25, 6, 45, 5, 56, 13, 52, 2, 93, 2, 10, 15, 21, 12, 115, 83, 46, 23, 24, 32, 109, 42, 51, 19, 117, 102), g2O1=c(10, 13, 104, 51, 13, 11, 31, 32, 52, 111, 51, 10, 68, 72, 129, 15, 2, 46, 2, 83, 56, 54, 82, 111, 125, 109, 63, 6, 83), g2O2=c(20, 4, 7, 54, 8, 34, 32, 23, 3, 33, 3, 50, 72, 84, 41, 22, 78, 55, 82, 66, 77, 125, 29, 9, 64, 49, 74, 120, 32),                             y=c(0.4055, -3.6364, -1.7822, 0.9814, -0.6678, 1.273, 2.4477, -2.5638, -1.6564, -3.5548, 0.481, 0.5733, 1.4435, -0.539, 0.1711, 2.048, 4.3141, -0.2355, 3.7834, -1.7552, 1.9951, 1.127, 0.274, -3.375, -0.9414, -1.6403, 0.5487, 2.1848, -0.983), SE=c(0.45639894829, 0.588472599192, 0.923309265631, 0.306594194335, 0.75405570086, 0.402243707222, 0.530471488395, 0.509215082259, 0.67282984476, 0.508428952755, 0.933327380933, 0.401372644808, 0.808455317256, 0.570788927713, 0.341613817051, 0.410731055558, 0.799749960925, 0.248596057893, 0.731778655059, 0.385875627631, 0.287228132327, 0.315277655409, 0.293768616431, 0.388587184555, 0.280535202782, 0.307571129985, 0.343074335968, 0.450333209968, 0.2513961018), study.names=c('George', 'Byron', 'Issa', 'Tom', 'Big Chris', 'Little Chris', 'Jens', 'Anja', 'Hailee', 'Joseph', 'Meghan', 'Medium Chris', 'Superman', 'Batman', 'Leonardo', 'Michaelangelo', 'Donatello', 'Raphael', 'The Hulk', 'Professor X', 'Cyclops', 'Storm', 'Rogue', 'Wolverine', 'Gambit', 'Spiderman', 'Mr. Fantastic', 'The Flash', 'Thor'), years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer()), covariates=list())"
        ,'results'            : {'images': {'Cumulative Forest Plot': './r_tmp/forest.png'}, 'texts': {'References': '1. this is a placeholder for binary random reference\n2. Cumulative Meta-Analysis: Lau, Joseph, et al. "Cumulative meta-analysis of therapeutic trials for myocardial infarction." New England Journal of Medicine 327.4 (1992): 248-254.)\n3. OpenMetaAnalyst: Wallace, Byron C., Issa J. Dahabreh, Thomas A. Trikalinos, Joseph Lau, Paul Trow, and Christopher H. Schmid. "Closing the Gap between Methodologists and End-Users: R as a Computational Back-End." Journal of Statistical Software 49 (2012): 5."\n4. metafor: Viechtbauer, Wolfgang. "Conducting meta-analyses in R with the metafor package." Journal of 36 (2010).\n', 'Cumulative Summary': 'Binary Random-Effects Model\n\nMetric: Odds Ratio\n\n Model Results\n\n Studies          Estimate   Lower bound   Upper bound   Std. error   p-Val   \n\n George            1.5001       0.6132        3.6694       0.4564       NA    \n\n + Byron           0.2022       0.0039       10.6171       2.0209     0.4290  \n\n + Issa            0.1919       0.0124        2.9712       1.3978     0.2376  \n\n + Tom             0.3877       0.0483        3.1100       1.0623     0.3724  \n\n + Big Chris       0.4126       0.0734        2.3190       0.8809     0.3148  \n\n + Little Chris    0.6113       0.1485        2.5158       0.7218     0.4954  \n\n + Jens            0.9350       0.2455        3.5612       0.6823     0.9216  \n\n + Anja            0.6733       0.1711        2.6499       0.6990     0.5715  \n\n + Hailee          0.5881       0.1638        2.1112       0.6521     0.4156  \n\n + Joseph          0.4291       0.1123        1.6397       0.6840     0.2161  \n\n + Meghan          0.4789       0.1355        1.6921       0.6440     0.2529  \n\n + Medium Chris    0.5383       0.1734        1.6709       0.5779     0.2839  \n\n + Superman        0.6248       0.2119        1.8419       0.5516     0.3938  \n\n + Batman          0.6222       0.2272        1.7038       0.5140     0.3559  \n\n + Leonardo        0.6530       0.2646        1.6117       0.4610     0.3552  \n\n + Michaelangelo   0.7684       0.3159        1.8692       0.4535     0.5614  \n\n + Donatello       0.9849       0.3973        2.4412       0.4632     0.9737  \n\n + Raphael         0.9720       0.4344        2.1752       0.4110     0.9450  \n\n + The Hulk        1.1753       0.5205        2.6542       0.4156     0.6975  \n\n + Professor X     1.0617       0.4788        2.3542       0.4063     0.8829  \n\n + Cyclops         1.1730       0.5366        2.5643       0.3990     0.6892  \n\n + Storm           1.2292       0.5884        2.5679       0.3759     0.5830  \n\n + Rogue           1.2328       0.6204        2.4496       0.3503     0.5503  \n\n + Wolverine       1.0550       0.5063        2.1983       0.3746     0.8864  \n\n + Gambit          1.0104       0.5025        2.0320       0.3564     0.9767  \n\n + Spiderman       0.9444       0.4774        1.8684       0.3481     0.8695  \n\n + Mr. Fantastic   0.9664       0.5028        1.8572       0.3333     0.9183  \n\n + The Flash       1.0483       0.5489        2.0018       0.3301     0.8865  \n\n + Thor            1.0084       0.5435        1.8707       0.3153     0.9789  \n\n\n'}, 'image_var_names': {'cumulative forest plot': 'cumulative_forest_plot'}, 'image_params_paths': {'Forest Plot': 'r_tmp/1382043081.69052'}, 'image_order': None}
        ,'params'             : {'conf.level': 95.0, 'digits': 4, 'fp_col2_str': u'[default]', 'fp_show_col4': True, 'to': 'only0', 'fp_col4_str': u'Ev/Ctrl', 'fp_xticks': '[default]', 'fp_col3_str': u'Ev/Trt', 'fp_show_col3': True, 'fp_show_col2': True, 'fp_show_col1': True, 'fp_plot_lb': '[default]', 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'adjust': 0.5, 'fp_plot_ub': '[default]', 'fp_col1_str': u'Studies', 'measure': 'OR', 'fp_xlabel': u'[default]', 'fp_show_summary_line': True}
        ,'meta_function_name' : 'cum.ma.binary'
        ,'function_name'      : 'binary.random'
        },
        
        {
         'test_name'          : "Binary Leave-one-out Meta Analysis"
        ,'fnc_to_evaluate'    : 'python_to_R.run_meta_method'
        ,'make_dataset_r_str' : "tmp_obj <- new('BinaryData', g1O1=c(30, 56, 5, 63, 5, 52, 56, 6, 43, 5, 55, 33, 8, 5, 56, 111, 23, 76, 89, 10, 123, 32, 119, 46, 32, 22, 28, 52, 99), g1O2=c(40, 654, 2, 25, 6, 45, 5, 56, 13, 52, 2, 93, 2, 10, 15, 21, 12, 115, 83, 46, 23, 24, 32, 109, 42, 51, 19, 117, 102), g2O1=c(10, 13, 104, 51, 13, 11, 31, 32, 52, 111, 51, 10, 68, 72, 129, 15, 2, 46, 2, 83, 56, 54, 82, 111, 125, 109, 63, 6, 83), g2O2=c(20, 4, 7, 54, 8, 34, 32, 23, 3, 33, 3, 50, 72, 84, 41, 22, 78, 55, 82, 66, 77, 125, 29, 9, 64, 49, 74, 120, 32),                             y=c(0.4055, -3.6364, -1.7822, 0.9814, -0.6678, 1.273, 2.4477, -2.5638, -1.6564, -3.5548, 0.481, 0.5733, 1.4435, -0.539, 0.1711, 2.048, 4.3141, -0.2355, 3.7834, -1.7552, 1.9951, 1.127, 0.274, -3.375, -0.9414, -1.6403, 0.5487, 2.1848, -0.983), SE=c(0.45639894829, 0.588472599192, 0.923309265631, 0.306594194335, 0.75405570086, 0.402243707222, 0.530471488395, 0.509215082259, 0.67282984476, 0.508428952755, 0.933327380933, 0.401372644808, 0.808455317256, 0.570788927713, 0.341613817051, 0.410731055558, 0.799749960925, 0.248596057893, 0.731778655059, 0.385875627631, 0.287228132327, 0.315277655409, 0.293768616431, 0.388587184555, 0.280535202782, 0.307571129985, 0.343074335968, 0.450333209968, 0.2513961018), study.names=c('George', 'Byron', 'Issa', 'Tom', 'Big Chris', 'Little Chris', 'Jens', 'Anja', 'Hailee', 'Joseph', 'Meghan', 'Medium Chris', 'Superman', 'Batman', 'Leonardo', 'Michaelangelo', 'Donatello', 'Raphael', 'The Hulk', 'Professor X', 'Cyclops', 'Storm', 'Rogue', 'Wolverine', 'Gambit', 'Spiderman', 'Mr. Fantastic', 'The Flash', 'Thor'), years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer()), covariates=list())"
        ,'results'            : {'images': {'Leave-one-out Forest plot': './r_tmp/forest.png'}, 'texts': {'Leave-one-out Summary': 'Binary Random-Effects Model\n\nMetric: Odds Ratio\n\n Model Results\n\n Studies          Estimate   Lower bound   Upper bound   Std. error   p-Val   \n\n Overall           1.0084       0.5435        1.8707       0.3153     0.9789  \n\n - George          0.9943       0.5257        1.8805       0.3252     0.9859  \n\n - Byron           1.1429       0.6209        2.1036       0.3113     0.6679  \n\n - Issa            1.0630       0.5676        1.9909       0.3201     0.8486  \n\n - Tom             0.9723       0.5124        1.8449       0.3268     0.9315  \n\n - Big Chris       1.0307       0.5484        1.9373       0.3220     0.9251  \n\n - Little Chris    0.9624       0.5108        1.8131       0.3232     0.9055  \n\n - Jens            0.9244       0.4967        1.7206       0.3170     0.8042  \n\n - Anja            1.1050       0.5943        2.0548       0.3165     0.7523  \n\n - Hailee          1.0661       0.5684        1.9998       0.3209     0.8418  \n\n - Joseph          1.1440       0.6248        2.0949       0.3086     0.6629  \n\n - Meghan          0.9946       0.5300        1.8662       0.3211     0.9865  \n\n - Medium Chris    0.9879       0.5215        1.8716       0.3260     0.9703  \n\n - Superman        0.9641       0.5141        1.8078       0.3208     0.9092  \n\n - Batman          1.0281       0.5453        1.9382       0.3235     0.9317  \n\n - Leonardo        1.0029       0.5265        1.9103       0.3288     0.9930  \n\n - Michaelangelo   0.9348       0.5014        1.7426       0.3178     0.8319  \n\n - Donatello       0.8807       0.4776        1.6240       0.3122     0.6840  \n\n - Raphael         1.0191       0.5283        1.9658       0.3352     0.9550  \n\n - The Hulk        0.8917       0.4824        1.6481       0.3134     0.7145  \n\n - Professor X     1.0768       0.5744        2.0186       0.3206     0.8175  \n\n - Cyclops         0.9338       0.5048        1.7273       0.3138     0.8271  \n\n - Storm           0.9669       0.5109        1.8297       0.3254     0.9176  \n\n - Rogue           0.9991       0.5221        1.9119       0.3311     0.9979  \n\n - Wolverine       1.1421       0.6323        2.0629       0.3017     0.6597  \n\n - Gambit          1.0463       0.5491        1.9935       0.3289     0.8906  \n\n - Spiderman       1.0736       0.5720        2.0151       0.3213     0.8251  \n\n - Mr. Fantastic   0.9887       0.5200        1.8797       0.3278     0.9723  \n\n - The Flash       0.9310       0.4997        1.7343       0.3174     0.8217  \n\n - Thor            1.0483       0.5489        2.0018       0.3301     0.8865  \n\n\n', 'References': '1. this is a placeholder for binary random reference\n2. metafor: Viechtbauer, Wolfgang. "Conducting meta-analyses in R with the metafor package." Journal of 36 (2010).\n3. Leave-one-out Meta-Analysis: LOO ma reference placeholder\n4. OpenMetaAnalyst: Wallace, Byron C., Issa J. Dahabreh, Thomas A. Trikalinos, Joseph Lau, Paul Trow, and Christopher H. Schmid. "Closing the Gap between Methodologists and End-Users: R as a Computational Back-End." Journal of Statistical Software 49 (2012): 5."\n'}, 'image_var_names': {'loo forest plot': 'loo_forest_plot'}, 'image_params_paths': {'Forest Plot': 'r_tmp/1382043090.98619'}, 'image_order': None}
        ,'params'             : {'conf.level': 95.0, 'digits': 4, 'fp_col2_str': u'[default]', 'fp_show_col4': True, 'to': 'only0', 'fp_col4_str': u'Ev/Ctrl', 'fp_xticks': '[default]', 'fp_col3_str': u'Ev/Trt', 'fp_show_col3': True, 'fp_show_col2': True, 'fp_show_col1': True, 'fp_plot_lb': '[default]', 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'adjust': 0.5, 'fp_plot_ub': '[default]', 'fp_col1_str': u'Studies', 'measure': 'OR', 'fp_xlabel': u'[default]', 'fp_show_summary_line': True}
        ,'meta_function_name' : 'loo.ma.binary'
        ,'function_name'      : 'binary.random'
        },
        
        {
         'test_name'          : "Binary Subgroup Meta Analysis"
        ,'fnc_to_evaluate'    : 'python_to_R.run_meta_method'
        ,'make_dataset_r_str' : "tmp_obj <- new('BinaryData', g1O1=c(30, 56, 5, 63, 5, 52, 56, 6, 43, 5, 55, 33, 8, 5, 56, 111, 23, 76, 89, 10, 123, 32, 119, 46, 32, 22, 28, 52, 99), g1O2=c(40, 654, 2, 25, 6, 45, 5, 56, 13, 52, 2, 93, 2, 10, 15, 21, 12, 115, 83, 46, 23, 24, 32, 109, 42, 51, 19, 117, 102), g2O1=c(10, 13, 104, 51, 13, 11, 31, 32, 52, 111, 51, 10, 68, 72, 129, 15, 2, 46, 2, 83, 56, 54, 82, 111, 125, 109, 63, 6, 83), g2O2=c(20, 4, 7, 54, 8, 34, 32, 23, 3, 33, 3, 50, 72, 84, 41, 22, 78, 55, 82, 66, 77, 125, 29, 9, 64, 49, 74, 120, 32),                             y=c(0.4055, -3.6364, -1.7822, 0.9814, -0.6678, 1.273, 2.4477, -2.5638, -1.6564, -3.5548, 0.481, 0.5733, 1.4435, -0.539, 0.1711, 2.048, 4.3141, -0.2355, 3.7834, -1.7552, 1.9951, 1.127, 0.274, -3.375, -0.9414, -1.6403, 0.5487, 2.1848, -0.983), SE=c(0.45639894829, 0.588472599192, 0.923309265631, 0.306594194335, 0.75405570086, 0.402243707222, 0.530471488395, 0.509215082259, 0.67282984476, 0.508428952755, 0.933327380933, 0.401372644808, 0.808455317256, 0.570788927713, 0.341613817051, 0.410731055558, 0.799749960925, 0.248596057893, 0.731778655059, 0.385875627631, 0.287228132327, 0.315277655409, 0.293768616431, 0.388587184555, 0.280535202782, 0.307571129985, 0.343074335968, 0.450333209968, 0.2513961018), study.names=c('George', 'Byron', 'Issa', 'Tom', 'Big Chris', 'Little Chris', 'Jens', 'Anja', 'Hailee', 'Joseph', 'Meghan', 'Medium Chris', 'Superman', 'Batman', 'Leonardo', 'Michaelangelo', 'Donatello', 'Raphael', 'The Hulk', 'Professor X', 'Cyclops', 'Storm', 'Rogue', 'Wolverine', 'Gambit', 'Spiderman', 'Mr. Fantastic', 'The Flash', 'Thor'), years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer()), covariates=list(new('CovariateValues', cov.name='Country', cov.vals=c('US','US','US','US','CANADA','CANADA','CANADA','CANADA','CANADA','CANADA','CHINA','CHINA','US','US','US','US','CANADA','CANADA','CANADA','CANADA','CANADA','CANADA','CHINA','CHINA','US','US','US','US','CANADA'),                     cov.type='factor', ref.var='US')))"
        ,'results'            : {'images': {'Subgroup Forest Plot': './r_tmp/forest.png'}, 'texts': {'Subgroup Summary': 'Binary Random-Effects Model\n\nMetric: Odds Ratio\n\n Model Results\n\n Subgroups        Studies   Estimate   Lower bound   Upper bound   Std. error   p-Val   \n\n Subgroup US         12      0.9681       0.4105        2.2829       0.4377     0.9409  \n\n Subgroup CANADA     13      1.2634       0.4480        3.5629       0.5290     0.6585  \n\n Subgroup CHINA      4       0.5783       0.0774        4.3204       1.0261     0.5935  \n\n Overall             29      1.0084       0.5435        1.8707       0.3153     0.9789  \n\n\n  Heterogeneity\n\n Studies             Q (df)       Het. p-Val   I^2   \n\n Subgroup US      147.9370 (11)    < 1e-04     93 %  \n\n Subgroup CANADA  265.6574 (12)    < 1e-04     95 %  \n\n Subgroup CHINA    69.7327 (3)     < 1e-04     96 %  \n\n Overall          492.2579 (28)    < 1e-04     94 %  \n\n\n', 'References': '1. this is a placeholder for binary random reference\n2. Subgroup Meta-Analysis: subgroup ma reference placeholder\n3. OpenMetaAnalyst: Wallace, Byron C., Issa J. Dahabreh, Thomas A. Trikalinos, Joseph Lau, Paul Trow, and Christopher H. Schmid. "Closing the Gap between Methodologists and End-Users: R as a Computational Back-End." Journal of Statistical Software 49 (2012): 5."\n4. metafor: Viechtbauer, Wolfgang. "Conducting meta-analyses in R with the metafor package." Journal of 36 (2010).\n'}, 'image_var_names': {'subgroups forest plot': 'subgroups_forest_plot'}, 'image_params_paths': {'Forest Plot': 'r_tmp/1382043149.43952'}, 'image_order': None}
        ,'params'             : {'conf.level': 95.0, 'digits': 4, 'fp_col2_str': u'[default]', 'fp_show_col4': True, 'to': 'only0', 'fp_col4_str': u'Ev/Ctrl', 'fp_xticks': '[default]', 'fp_col3_str': u'Ev/Trt', 'fp_show_col3': True, 'fp_show_col2': True, 'cov_name': 'Country', 'fp_plot_lb': '[default]', 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'fp_show_summary_line': True, 'adjust': 0.5, 'fp_plot_ub': '[default]', 'fp_show_col1': True, 'measure': 'OR', 'fp_xlabel': u'[default]', 'fp_col1_str': u'Studies'}
        ,'meta_function_name' : 'subgroup.ma.binary'
        ,'function_name'      : 'binary.random'
        },
        
        {
        # Remember to convert selected_cov, covs_to_values back to variables (not just column ids)
         'test_name'          : "Meta Regression"
        ,'fnc_to_evaluate'    : 'python_to_R.run_meta_regression'
        ,'make_dataset_r_str' : "tmp_obj <- new('BinaryData', y=c(0.4055, -3.6364, -1.7822, 0.9814, -0.6678, 1.273, 2.4477, -2.5638, -1.6564, -3.5548, 0.481, 0.5733), SE=c(0.45639894829, 0.588472599192, 0.923309265631, 0.306594194335, 0.75405570086, 0.402243707222, 0.530471488395, 0.509215082259, 0.67282984476, 0.508428952755, 0.933327380933, 0.401372644808), study.names=c('George', 'Byron', 'Issa', 'Tom', 'Big Chris', 'Little Chris', 'Jens', 'Anja', 'Hailee', 'Joseph', 'Meghan', 'Medium Chris'), years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer()), covariates=list(new('CovariateValues', cov.name='Age', cov.vals=c(40.0,65.0,2000.0,47.0,199.0,348.0,40.0,18.0,49.0,44.0,18.0,584.0),                     cov.type='continuous', ref.var='40.0'),new('CovariateValues', cov.name='Gender', cov.vals=c('M','M','M','M','M','M','M','F','F','M','F','M'),                     cov.type='factor', ref.var='M'),new('CovariateValues', cov.name='Country', cov.vals=c('US','US','US','US','CANADA','CANADA','CANADA','CANADA','CANADA','CANADA','CHINA','CHINA'),                     cov.type='factor', ref.var='US')))"
        ,'results'            : {'images': {}, 'texts': {'References': '1. metafor: Viechtbauer, Wolfgang. "Conducting meta-analyses in R with the metafor package." Journal of 36 (2010).\n2. OpenMetaAnalyst: Wallace, Byron C., Issa J. Dahabreh, Thomas A. Trikalinos, Joseph Lau, Paul Trow, and Christopher H. Schmid. "Closing the Gap between Methodologists and End-Users: R as a Computational Back-End." Journal of Statistical Software 49 (2012): 5."\n3. Meta Regression: meta regression citation placeholder\n', 'Summary': 'Meta-Regression\n\nMetric: Odds Ratio\n\nModel Results\n\n Covariate  Level    Studies   Coefficients   Lower bound   Upper bound   Std. error   p-Value  \n\n Intercept                        -0.697        -3.327         1.933         1.342      0.603   \n\n Age                              -0.001        -0.003         0.002         0.001      0.704   \n\n Gender        M        9                                                                       \n\n               F        3         -1.622        -5.037         1.793         1.742      0.352   \n\n Country      US        4                                                                       \n\n            CANADA      6          0.517        -2.708         3.743         1.646      0.753   \n\n             CHINA      2          2.153        -2.103         6.408         2.171      0.321   \n\n\nOmnibus p-Value\n\n 0.825 \n\n\n'}, 'image_var_names': {}, 'image_params_paths': {}, 'image_order': None}
        ,'covs_to_values'     : None
        ,'metric'             : 2
        ,'conf_level'         : 95
        ,'fixed_effects'      : False
        ,'selected_cov'       : None
        },
    
        {
         'test_name'          : "Meta regression conditional means"
        ,'fnc_to_evaluate'    : 'python_to_R.run_meta_regression'
        ,'make_dataset_r_str' : '''tmp_obj <- new('BinaryData', y=c(0.405465108108, -3.63641065706, -1.78219001821, 0.981417315363, 
-0.667829372576, 1.27304648063, 2.44766247662, -2.56383390838, -1.65638067168, 
-3.55482844599, 0.480972660616, 0.573345980747, 1.44345277496, 
-0.538996500733, 0.171061151976, 2.04800001585, 4.31414921227, 
-0.235506999334, 3.78336782864, -1.75524216927, 1.99514387056, 1.12701176319, 
0.273964173034, -3.37501210972, -0.941364369426, -1.64031076348, 
0.548695897821, 2.18480205734, -0.982957668147), SE=c(0.456435464588, 0.588480476964, 0.923294388303, 0.306593179195, 
0.754048899999, 0.402211197094, 0.530438693322, 0.509168017842, 
0.672861793714, 0.508471049857, 0.933339699494, 0.401317478407, 
0.808452083454, 0.570783365905, 0.341564037057, 0.410791028078, 
0.799770033837, 0.248544755582, 0.731764490652, 0.385925949318, 
0.287145430078, 0.315333450787, 0.29382178598, 0.388630367421, 0.280507618095, 
0.307644053711, 0.343121544133, 0.450308536204, 0.251402315902), study.names=c('George', 'Byron', 'Issa', 'Tom', 'Big Chris', 'Little Chris', 'Jens', 'Anja', 
'Hailee', 'Joseph', 'Meghan', 'Medium Chris', 'Superman', 'Batman', 
'Leonardo', 'Michaelangelo', 'Donatello', 'Raphael', 'The Hulk', 
'Professor X', 'Cyclops', 'Storm', 'Rogue', 'Wolverine', 'Gambit', 
'Spiderman', 'Mr. Fantastic', 'The Flash', 'Thor'), years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
as.integer(), as.integer(), as.integer(), as.integer()), covariates=list(new('CovariateValues', cov.name='Age', cov.vals=c(40.0, 65.0, 2000.0, 47.0, 199.0, 348.0, 40.0, 18.0, 49.0, 44.0, 18.0, 584.0, 
35.0, 107.0, 101.0, 50.0, 79.0, 48.0, 75.0, 41.0, 53.0, 24.0, 54.0, 33.0, 
102.0, 87.0, 118.0, 60.0, 106.0), cov.type='continuous', ref.var='40.0'),new('CovariateValues', cov.name='Gender', cov.vals=c("M", "M", "M", "M", "M", "M", "M", "F", "F", "M", "F", "M", "M", "M", "M", 
"M", "M", "M", "M", "F", "F", "M", "F", "M", "M", "M", "M", "M", "M"), cov.type='factor', ref.var='M'),new('CovariateValues', cov.name='Country', cov.vals=c("US", "US", "US", "US", "CANADA", "CANADA", "CANADA", "CANADA", "CANADA", 
"CANADA", "CHINA", "CHINA", "US", "US", "US", "US", "CANADA", "CANADA", 
"CANADA", "CANADA", "CANADA", "CANADA", "CHINA", "CHINA", "US", "US", "US", 
"US", "CANADA"), cov.type='factor', ref.var='US')))'''
        ,'results'            : {'images': {}, 'texts': {'Conditional Means': "Meta-Regression-Based Conditional Means\n\nMetric: Odds Ratio\n\nThese are the conditional means for 'Gender',\nstratified over its levels given the following values for the other covariates:\nCountry = CANADA\nAge = 65\n\n\nModel Results\n\n Level  Studies   Conditional Means   Lower bound   Upper bound   Std. error  \n\n M         23           0.523           -0.635         1.680         0.591    \n\n F         6           -0.366           -1.989         1.257         0.828    \n\n\n", 'References': '1. metafor: Viechtbauer, Wolfgang. "Conducting meta-analyses in R with the metafor package." Journal of 36 (2010).\n2. OpenMetaAnalyst: Wallace, Byron C., Issa J. Dahabreh, Thomas A. Trikalinos, Joseph Lau, Paul Trow, and Christopher H. Schmid. "Closing the Gap between Methodologists and End-Users: R as a Computational Back-End." Journal of Statistical Software 49 (2012): 5."\n3. Meta Regression: meta regression citation placeholder\n', 'Summary': 'Meta-Regression\n\nMetric: Odds Ratio\n\nModel Results\n\n Covariate  Level    Studies   Coefficients   Lower bound   Upper bound   Std. error   p-Value  \n\n Intercept                         0.112        -1.007         1.232         0.571      0.844   \n\n Age                              -0.001        -0.003         0.001         0.001      0.476   \n\n Gender        M        23                                                                      \n\n               F        6         -0.889        -2.754         0.977         0.952      0.351   \n\n Country      US        12                                                                      \n\n            CANADA      13         0.458        -1.101         2.017         0.796      0.565   \n\n             CHINA      4         -0.112        -2.374         2.151         1.154      0.923   \n\n\nOmnibus p-Value\n\n 0.772 \n\n\n'}, 'image_var_names': {}, 'image_params_paths': {}, 'image_order': None}
        ,'covs_to_values'     : {14: 'CANADA', 15: 65.0}
        ,'metric'             : 2
        ,'conf_level'         : 95
        ,'fixed_effects'      : False
        ,'selected_cov'       : 13
        },
    ]
    
    non_deterministic_test_data = [
        {
         'test_name'          : "Bootstrap Meta Analysis"
        ,'fnc_to_evaluate'    : 'python_to_R.run_meta_method'
        ,'make_dataset_r_str' : "tmp_obj <- new('BinaryData', g1O1=c(30, 56, 5, 63, 5, 52, 56, 6, 43, 5, 55, 33, 8, 5, 56, 111, 23, 76, 89, 10, 123, 32, 119, 46, 32, 22, 28, 52, 99), g1O2=c(40, 654, 2, 25, 6, 45, 5, 56, 13, 52, 2, 93, 2, 10, 15, 21, 12, 115, 83, 46, 23, 24, 32, 109, 42, 51, 19, 117, 102), g2O1=c(10, 13, 104, 51, 13, 11, 31, 32, 52, 111, 51, 10, 68, 72, 129, 15, 2, 46, 2, 83, 56, 54, 82, 111, 125, 109, 63, 6, 83), g2O2=c(20, 4, 7, 54, 8, 34, 32, 23, 3, 33, 3, 50, 72, 84, 41, 22, 78, 55, 82, 66, 77, 125, 29, 9, 64, 49, 74, 120, 32),                             y=c(0.4055, -3.6364, -1.7822, 0.9814, -0.6678, 1.273, 2.4477, -2.5638, -1.6564, -3.5548, 0.481, 0.5733, 1.4435, -0.539, 0.1711, 2.048, 4.3141, -0.2355, 3.7834, -1.7552, 1.9951, 1.127, 0.274, -3.375, -0.9414, -1.6403, 0.5487, 2.1848, -0.983), SE=c(0.45639894829, 0.588472599192, 0.923309265631, 0.306594194335, 0.75405570086, 0.402243707222, 0.530471488395, 0.509215082259, 0.67282984476, 0.508428952755, 0.933327380933, 0.401372644808, 0.808455317256, 0.570788927713, 0.341613817051, 0.410731055558, 0.799749960925, 0.248596057893, 0.731778655059, 0.385875627631, 0.287228132327, 0.315277655409, 0.293768616431, 0.388587184555, 0.280535202782, 0.307571129985, 0.343074335968, 0.450333209968, 0.2513961018), study.names=c('George', 'Byron', 'Issa', 'Tom', 'Big Chris', 'Little Chris', 'Jens', 'Anja', 'Hailee', 'Joseph', 'Meghan', 'Medium Chris', 'Superman', 'Batman', 'Leonardo', 'Michaelangelo', 'Donatello', 'Raphael', 'The Hulk', 'Professor X', 'Cyclops', 'Storm', 'Rogue', 'Wolverine', 'Gambit', 'Spiderman', 'Mr. Fantastic', 'The Flash', 'Thor'), years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer()), covariates=list())"
        ,'results'            : {'images': {'Histogram': './r_tmp/bootstrap.png'}, 'texts': {'Summary': 'The 95% Confidence Interval: [-0.7022, 0.6946]\nThe observed value of the effect size was 0.0083, while the mean over the replicates was 0.0204.'}, 'image_var_names': {}, 'image_params_paths': {}, 'image_order': None}
        ,'params'             : {'conf.level': 95.0, 'fp_xlabel': u'[default]', 'histogram.xlab': 'Effect Size', 'fp_xticks': '[default]', 'fp_show_col4': True, 'fp_show_col3': True, 'fp_show_col2': True, 'fp_show_col1': True, 'fp_plot_lb': '[default]', 'fp_outpath': u'./r_tmp/forest.png', 'rm.method': 'DL', 'fp_plot_ub': '[default]', 'fp_col1_str': u'Studies', 'measure': 'OR', 'bootstrap.plot.path': './r_tmp/bootstrap.png', 'digits': 4, 'fp_col2_str': u'[default]', 'num.bootstrap.replicates': 1000, 'fp_col4_str': u'Ev/Ctrl', 'histogram.title': 'Bootstrap Histogram', 'fp_col3_str': u'Ev/Trt', 'fp_show_summary_line': True, 'to': 'only0', 'adjust': 0.5, 'bootstrap.type': 'boot.ma'}
        ,'meta_function_name' : 'bootstrap'
        ,'function_name'      : 'binary.random'
        },
                                   
        {
         'test_name'          : "Bootstrapped meta regression"
        ,'fnc_to_evaluate'    : 'python_to_R.run_bootstrap_meta_regression'
        ,'make_dataset_r_str' : "tmp_obj <- new('BinaryData', y=c(0.4055, -3.6364, -1.7822, 0.9814, -0.6678, 1.273, 2.4477, -2.5638, -1.6564, -3.5548, 0.481, 0.5733, 1.4435, -0.539, 0.1711, 2.048, 4.3141, -0.2355, 3.7834, -1.7552, 1.9951, 1.127, 0.274, -3.375, -0.9414, -1.6403, 0.5487, 2.1848, -0.983), SE=c(0.45639894829, 0.588472599192, 0.923309265631, 0.306594194335, 0.75405570086, 0.402243707222, 0.530471488395, 0.509215082259, 0.67282984476, 0.508428952755, 0.933327380933, 0.401372644808, 0.808455317256, 0.570788927713, 0.341613817051, 0.410731055558, 0.799749960925, 0.248596057893, 0.731778655059, 0.385875627631, 0.287228132327, 0.315277655409, 0.293768616431, 0.388587184555, 0.280535202782, 0.307571129985, 0.343074335968, 0.450333209968, 0.2513961018), study.names=c('George', 'Byron', 'Issa', 'Tom', 'Big Chris', 'Little Chris', 'Jens', 'Anja', 'Hailee', 'Joseph', 'Meghan', 'Medium Chris', 'Superman', 'Batman', 'Leonardo', 'Michaelangelo', 'Donatello', 'Raphael', 'The Hulk', 'Professor X', 'Cyclops', 'Storm', 'Rogue', 'Wolverine', 'Gambit', 'Spiderman', 'Mr. Fantastic', 'The Flash', 'Thor'), years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), as.integer()), covariates=list(new('CovariateValues', cov.name='Gender', cov.vals=c('M','M','M','M','M','M','M','F','F','M','F','M','M','M','M','M','M','M','M','F','F','M','F','M','M','M','M','M','M'),                     cov.type='factor', ref.var='M'),new('CovariateValues', cov.name='Age', cov.vals=c(40.0,65.0,2000.0,47.0,199.0,348.0,40.0,18.0,49.0,44.0,18.0,584.0,35.0,107.0,101.0,50.0,79.0,48.0,75.0,41.0,53.0,24.0,54.0,33.0,102.0,87.0,118.0,60.0,106.0),                     cov.type='continuous', ref.var='40.0')))"
        ,'results'            : {'images': {'Histograms': './r_tmp/bootstrap.png'}, 'texts': {'Summary': 'Bootstrapped Meta-Regression based on 1000 replicates.\n\n0 resampling attempts failed.\n\nMetric: Odds Ratio\n\nModel Results\n\n Covariate  Level   Studies   Coefficients   Lower bound   Upper bound  \n\n Intercept                        0.218        -0.739         1.480     \n\n Age                             -0.000        -0.007         0.004     \n\n Gender       M        23                                               \n\n              F        6         -0.719        -2.563         0.840     \n\n\n'}, 'image_var_names': {}, 'image_params_paths': {}, 'image_order': None}
        ,'fixed_effects'      : False
        ,'data_type'          : 'binary'
        ,'metric'             : 2
        ,'bootstrap_params'   : {'histogram.title': 'Bootstrap Histogram', 'histogram.xlab': 'Effect Size', 'bootstrap.type': 'boot.meta.reg', 'num.bootstrap.replicates': 1000, 'bootstrap.plot.path': './r_tmp/bootstrap.png'}
        ,'conf_level'         : 95
        ,'covs_to_values'     : None
        ,'selected_cov'       : None
        },
        
        {                
         'test_name'          : "Bootstrapped meta regression conditional means"
        ,'fnc_to_evaluate'    : 'python_to_R.run_bootstrap_meta_regression'
        ,'make_dataset_r_str' : '''tmp_obj <- new('BinaryData', y=c(0.405465108108, -3.63641065706, -1.78219001821, 0.981417315363, 
-0.667829372576, 1.27304648063, 2.44766247662, -2.56383390838, -1.65638067168, 
-3.55482844599, 0.480972660616, 0.573345980747, 1.44345277496, 
-0.538996500733, 0.171061151976, 2.04800001585, 4.31414921227, 
-0.235506999334, 3.78336782864, -1.75524216927, 1.99514387056, 1.12701176319, 
0.273964173034, -3.37501210972, -0.941364369426, -1.64031076348, 
0.548695897821, 2.18480205734, -0.982957668147), SE=c(0.456435464588, 0.588480476964, 0.923294388303, 0.306593179195, 
0.754048899999, 0.402211197094, 0.530438693322, 0.509168017842, 
0.672861793714, 0.508471049857, 0.933339699494, 0.401317478407, 
0.808452083454, 0.570783365905, 0.341564037057, 0.410791028078, 
0.799770033837, 0.248544755582, 0.731764490652, 0.385925949318, 
0.287145430078, 0.315333450787, 0.29382178598, 0.388630367421, 0.280507618095, 
0.307644053711, 0.343121544133, 0.450308536204, 0.251402315902), study.names=c('George', 'Byron', 'Issa', 'Tom', 'Big Chris', 'Little Chris', 'Jens', 'Anja', 
'Hailee', 'Joseph', 'Meghan', 'Medium Chris', 'Superman', 'Batman', 
'Leonardo', 'Michaelangelo', 'Donatello', 'Raphael', 'The Hulk', 
'Professor X', 'Cyclops', 'Storm', 'Rogue', 'Wolverine', 'Gambit', 
'Spiderman', 'Mr. Fantastic', 'The Flash', 'Thor'), years=c(as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
as.integer(), as.integer(), as.integer(), as.integer(), as.integer(), 
as.integer(), as.integer(), as.integer(), as.integer()), covariates=list(new('CovariateValues', cov.name='Country', cov.vals=c("US", "US", "US", "US", "CANADA", "CANADA", "CANADA", "CANADA", "CANADA", 
"CANADA", "CHINA", "CHINA", "US", "US", "US", "US", "CANADA", "CANADA", 
"CANADA", "CANADA", "CANADA", "CANADA", "CHINA", "CHINA", "US", "US", "US", 
"US", "CANADA"), cov.type='factor', ref.var='US'),new('CovariateValues', cov.name='Age', cov.vals=c(40.0, 65.0, 2000.0, 47.0, 199.0, 348.0, 40.0, 18.0, 49.0, 44.0, 18.0, 584.0, 
35.0, 107.0, 101.0, 50.0, 79.0, 48.0, 75.0, 41.0, 53.0, 24.0, 54.0, 33.0, 
102.0, 87.0, 118.0, 60.0, 106.0), cov.type='continuous', ref.var='40.0')))'''
        ,'results'            : {'images': {'Histograms': './r_tmp/bootstrap.png'}, 'texts': {'Bootstrapped Meta-Regression Based Conditional Means': "Bootstrapped Meta-Regression-Based Conditional Means\n\nMetric: Odds Ratio\n\nThese are the conditional means for 'Country',\nstratified over its levels given the following values for the other covariates:\nAge = 65\n\n\nModel Results\n\n Level   Studies   Conditional Means   Lower bound   Upper bound  \n\n US         12           0.057           -0.931         1.004     \n\n CANADA     13           0.228           -0.985         1.495     \n\n CHINA      4           -0.615           -2.482         1.758     \n\n\n"}, 'image_var_names': {}, 'image_params_paths': {}, 'image_order': None}
        ,'fixed_effects'      : False
        ,'data_type'          : 'binary'
        ,'metric'             : 2
        ,'bootstrap_params'   : {'histogram.title': 'Bootstrap Histogram', 'histogram.xlab': 'Effect Size', 'bootstrap.type': 'boot.meta.reg.cond.means', 'num.bootstrap.replicates': 1000, 'bootstrap.plot.path': './r_tmp/bootstrap.png'}
        ,'conf_level'         : 95
        ,'covs_to_values'     : {15: 65.0}
        ,'selected_cov'       : 14
        },
    ]
    
    for datum in regular_test_data:     
        check_analysis.description = datum['test_name']
        yield check_analysis, datum
    for datum in non_deterministic_test_data:
        check_analysis.description = datum['test_name']
        yield check_analysis, datum, True
         
    


def check_analysis(test_data, check_images=False):
    test_name = test_data['test_name']
    fnc_to_evaluate = test_data['fnc_to_evaluate']
    make_dataset_r_str = test_data['make_dataset_r_str']
    results = test_data['results']
    
    bar.setText("Running test: %s" % test_name)
    QApplication.processEvents()
    
    # make function parameters dict
    function_params_dict = {}
    for key,value in test_data.items():
        if key not in ['test_name','fnc_to_evaluate','make_dataset_r_str','results']:
            if key == 'selected_cov':
                value = form._selected_cov_to_select_col(value, reverse=True)
            if key == 'covs_to_values':
                value = form._covs_to_values_to_cols_to_values(value, reverse=True) 
            function_params_dict[key] = value
    
    analysis_function = eval(fnc_to_evaluate)
    python_to_R.execute_in_R(make_dataset_r_str)
    test_results = analysis_function(**function_params_dict)
    
    if not check_images:
        assert 'texts' in results
    else:
        assert 'images' in results
        
    results_summary, test_results_summary = None, None
    results_summary_key, test_results_summary_key = None, None
    
    for key in results['texts'].keys():
        if key.lower().find("summary") != -1:
            results_summary_key = key
            results_summary = results['texts'][key]
            break
        
    test_results_summary = None
    for key in test_results['texts'].keys():
        if key.lower().find("summary") != -1:
            test_results_summary_key = key
            test_results_summary = test_results['texts'][key]
            break
    
    #if "Conditional Means" in results['texts']:
    #    print("Check analysis")
        #pyqtRemoveInputHook()
        #import pdb; pdb.set_trace()
        
    #if results_summary!=test_results_summary:
    #    print("Check analysis")
    #    pyqtRemoveInputHook()
    #    import pdb; pdb.set_trace()
    

        
    #assert True
    if check_images:
        results_histo_key = get_key_close_enough('histogram',results['images'])
        test_result_histo_key = get_key_close_enough('histogram',test_results['images'])
        assert results['images'][results_histo_key]==test_results['images'][test_result_histo_key]
    else:
        assert results_summary==test_results_summary 
    
def get_key_close_enough(key, adict):
    for akey in adict.keys():
        if akey.lower().find(key.lower()) != -1:
            return akey


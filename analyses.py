##############################################################################
# 
# Author: George Dietz
#
# Description: All the functions related to performing analysis should live
#              here
#
##############################################################################

from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import results_window
import ma_wizard
import data_exploration_wizards
import python_to_R
from phylo.phylowizard import PhyloWizard
from ome_globals import *
from meta_progress import MetaProgress


class Analyzer:
    def __init__(self, main_form):
        self.main_form = main_form
    
    def _get_model(self):
        return self.main_form.model
    
    def _show_additional_values(self):
        return self.main_form.user_prefs['show_additional_values']
    def _show_analysis_selections(self):
        return self.main_form.user_prefs['show_analysis_selections']
    
    #### META ANALYSIS & META-REGRESSION ####
    def cum_ma(self):
        self.meta_analysis(meta_f_str="cum.ma", mode=CUM_MODE)
        
    def loo_ma(self):
        self.meta_analysis(meta_f_str="loo.ma", mode=LOO_MODE)
        
    def bootstrap_ma(self):
        self.meta_analysis(meta_f_str="bootstrap", mode=BOOTSTRAP_MA)
        
    def subgroup_ma(self):
        self.meta_analysis(meta_f_str="subgroup.ma", mode=SUBGROUP_MODE)
        
    def meta_analysis(self, meta_f_str=None, mode = MA_MODE):
        model = self._get_model()
        
        if mode == BOOTSTRAP_MA:
            wizard = ma_wizard.MetaAnalysisWizard(model=model,
                                      meta_f_str=meta_f_str,
                                      mode=BOOTSTRAP_MA,
                                      parent=self.main_form)
        elif mode == SUBGROUP_MODE:
            wizard = ma_wizard.MetaAnalysisWizard(model=model,
                                                  meta_f_str=meta_f_str,
                                                  mode=SUBGROUP_MODE,
                                                  parent=self.main_form)
        else:
            wizard = ma_wizard.MetaAnalysisWizard(model=model,
                                      meta_f_str=meta_f_str,
                                      mode=mode,
                                      parent=self.main_form)
            
        unmodified_meta_f_str = meta_f_str    
        if wizard.exec_():
            meta_f_str = wizard.get_modified_meta_f_str()
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            current_param_vals = wizard.get_plot_params()
            chosen_method = wizard.get_current_method()
            if mode == SUBGROUP_MODE:
                subgroup_variable = wizard.get_subgroup_variable()
            summary = wizard.get_summary()
            if mode == BOOTSTRAP_MA:
                current_param_vals.update(wizard.get_bootstrap_params())
                meta_f_str = unmodified_meta_f_str

            # Save selections made for next analysis
            model.update_data_type_selection(data_type)    # int
            model.update_metric_selection(metric)          # int
            model.update_method_selection(chosen_method)   #int??? str??
            model.update_ma_param_vals(current_param_vals)
            model.update_data_location_choices(data_type, data_location)     # save data locations choices for this data type in the model
            model.update_previously_included_studies(set(included_studies))  # save which studies were included on last meta-regression
            if mode == SUBGROUP_MODE: model.update_subgroup_var_selection(subgroup_variable)
            if mode == BOOTSTRAP_MA: model.update_bootstrap_params_selection(wizard.get_bootstrap_params())



            if mode == SUBGROUP_MODE:
                covs_to_include = [subgroup_variable,]
            else:
                covs_to_include = []
                
            try:
                self.run_ma(included_studies,
                            data_type, metric,
                            data_location,
                            current_param_vals,
                            chosen_method,
                            meta_f_str,
                            covs_to_include=covs_to_include,
                            summary=summary)
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
                

    def run_ma(self, included_studies, data_type, metric, data_location,
               current_param_vals, chosen_method, meta_f_str,
               covs_to_include=[], summary=""):
        
        model = self._get_model()
        
        # First, let's fire up a progress bar
        bar = MetaProgress()
        bar.show()
        result = None
        

        # also add the metric to the parameters
        # -- this is for scaling
        current_param_vals["measure"] = METRIC_TO_ESCALC_MEASURE[metric]
    
        try:
            # dispatch on type; build an R object, then run the analysis
            if OMA_CONVENTION[data_type] == "binary":
                # note that this call creates a tmp object in R called
                # tmp_obj (though you can pass in whatever var name
                # you'd like)
                make_dataset_r_str = python_to_R.dataset_to_simple_binary_robj(model=model,
                                                          included_studies=included_studies,
                                                          data_location=data_location,
                                                          covs_to_include=covs_to_include)
                if meta_f_str is None:
                    result = python_to_R.run_binary_ma(function_name=chosen_method,
                                                       params=current_param_vals)
                    # for making tests
                    if MAKE_TESTS:
                        self._writeout_test_parameters("python_to_R.run_binary_ma", make_dataset_r_str, result,
                                                        function_name=chosen_method,
                                                        params=current_param_vals)
                else:
                    result = python_to_R.run_meta_method(meta_function_name = meta_f_str,
                                                         function_name = chosen_method,
                                                         params = current_param_vals)
                    if MAKE_TESTS:
                        self._writeout_test_parameters("python_to_R.run_meta_method", make_dataset_r_str, result,
                                                    meta_function_name = meta_f_str,
                                                    function_name = chosen_method,
                                                    params = current_param_vals)
                    
            elif OMA_CONVENTION[data_type] == "continuous":
                make_dataset_r_str = python_to_R.dataset_to_simple_continuous_robj(model=model,
                                                              included_studies=included_studies,
                                                              data_location=data_location,
                                                              data_type=data_type, 
                                                              covs_to_include=covs_to_include)
                if meta_f_str is None:
                    # run standard meta-analysis
                    result = python_to_R.run_continuous_ma(function_name = chosen_method,
                                                           params = current_param_vals)
                    if MAKE_TESTS:
                        self._writeout_test_parameters("python_to_R.run_continuous_ma", make_dataset_r_str, result,
                                                    function_name = chosen_method,
                                                    params = current_param_vals)
                else:
                    # get meta!
                    result = python_to_R.run_meta_method(meta_function_name = meta_f_str,
                                                         function_name = chosen_method,
                                                         params = current_param_vals)
                    if MAKE_TESTS:
                        self._writeout_test_parameters("python_to_R.run_meta_method", make_dataset_r_str, result,
                                                    meta_function_name = meta_f_str,
                                                         function_name = chosen_method,
                                                         params = current_param_vals)
                
                #_writeout_test_data(meta_f_str, self.current_method, current_param_vals, result) # FOR MAKING TESTS
        finally:
            bar.hide()

        # update the user_preferences object for the selected method
        # with the values selected for this run
        # TODO: refactor this so that all preferences just get stored/loaded
        # in the model
        current_dict = self.main_form.get_user_method_params_d()
        current_dict[chosen_method] = current_param_vals
        self.main_form.update_user_prefs("method_params", current_dict)
        
        self._display_results(result, summary)
        
    def meta_regression(self, mode = META_REG_MODE):
        model = self._get_model()
        
        wizard = ma_wizard.MetaAnalysisWizard(model=model,
                                              mode=mode,
                                              parent=self.main_form)
        
        if wizard.exec_():
            data_type, metric = wizard.get_data_type_and_metric()
            data_location     = wizard.get_data_location()
            included_studies  = wizard.get_included_studies_in_proper_order()
            covariates        = wizard.get_included_covariates()
            interactions      = wizard.get_included_interactions()
            fixed_effects     = wizard.using_fixed_effects()
            conf_level        = wizard.get_covpage_conf_level()
            random_effects_method = wizard.get_random_effects_method()
            cov_2_ref_values  = wizard.get_covariate_reference_levels()
            summary           = wizard.get_summary()
            if mode in [META_REG_COND_MEANS, BOOTSTRAP_META_REG_COND_MEANS]:
                selected_cov, covs_to_values = wizard.get_meta_reg_cond_means_info()
            else:
                selected_cov, covs_to_values = None, None
            bootstrap_params = wizard.get_bootstrap_params() if mode in [BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS] else {}
            
            print("Covariates to reference values: %s" % str(cov_2_ref_values))
            
            # Save analysis analysis info that we just gathered
            model.update_data_type_selection(data_type) # int
            model.update_metric_selection(metric) # int
            model.update_fixed_vs_random_effects_selection(fixed_effects) #bool
            model.update_conf_level_selection(conf_level) #double
            model.update_cov_2_ref_values_selection(cov_2_ref_values) # dict
            model.update_bootstrap_params_selection(bootstrap_params)
            model.update_data_location_choices(data_type, data_location)  # save data locations choices for this data type in the model
            model.update_previously_included_studies(set(included_studies)) # save which studies were included on last meta-regression
            model.update_previously_included_covariates(set(covariates)) # save which covariates were included on last meta-regression
            model.update_selected_cov_and_covs_to_values(selected_cov, covs_to_values)
            model.update_random_effects_method(random_effects_method)    
                
            try:
                if mode == META_REG_MODE:
                    self.grun_meta_regression(metric,
                                             data_type,
                                             included_studies,
                                             data_location,
                                             covariates=covariates,
                                             interactions = interactions,
                                             #covariate_reference_values = cov_2_ref_values,
                                             fixed_effects=fixed_effects,
                                             conf_level=conf_level,
                                             random_effects_method = random_effects_method,
                                             summary=summary)
                else:
                    self.run_meta_regression(metric,
                                             data_type,
                                             included_studies,
                                             data_location,
                                             covs_to_include=covariates,
                                             covariate_reference_values = cov_2_ref_values,
                                             fixed_effects=fixed_effects,
                                             conf_level=conf_level,
                                             random_effects_method = random_effects_method,
                                             selected_cov=selected_cov, covs_to_values=covs_to_values,
                                             mode=mode,
                                             bootstrap_params=bootstrap_params, # for bootstrapping
                                             summary=summary)
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
                
  
    def run_meta_regression(self, metric, data_type, included_studies,
                            data_location, covs_to_include,
                            fixed_effects, conf_level,
                            random_effects_method,
                            covariate_reference_values={},
                            selected_cov = None, covs_to_values = None,
                            mode=META_REG_MODE,
                            bootstrap_params={}, summary=""):
        model = self._get_model()
        
        if mode in [BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS]:
            bar = MetaProgress("Running Bootstrapped Meta regression. It can take some time. Patience...")
        else:
            bar = MetaProgress()
        bar.show()
        
        if OMA_CONVENTION[data_type] == "binary":
            make_dataset_r_str = python_to_R.dataset_to_simple_binary_robj(model=model,
                                                      included_studies=included_studies,
                                                      data_location=data_location,
                                                      covs_to_include=covs_to_include,
                                                      covariate_reference_values=covariate_reference_values,
                                                      include_raw_data=False)
        elif OMA_CONVENTION[data_type] == "continuous":
            make_r_object = partial(python_to_R.dataset_to_simple_continuous_robj, model=model,
                                              included_studies=included_studies,
                                              data_location=data_location,
                                              data_type=data_type, 
                                              covs_to_include=covs_to_include,
                                              covariate_reference_values=covariate_reference_values)
            if metric != GENERIC_EFFECT:
                make_dataset_r_str = make_r_object()
            else:
                make_dataset_r_str = make_r_object(generic_effect=True)
                
        try:
            if mode in [BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS]:
                result = python_to_R.run_bootstrap_meta_regression(metric=metric,
                                                                   fixed_effects=fixed_effects,
                                                                   conf_level=conf_level,
                                                                   selected_cov=selected_cov, covs_to_values = covs_to_values,
                                                                   data_type=OMA_CONVENTION[data_type],
                                                                   bootstrap_params = bootstrap_params)
                if MAKE_TESTS:
                    self._writeout_test_parameters("python_to_R.run_bootstrap_meta_regression", make_dataset_r_str, result,
                                                    metric=metric,
                                                    fixed_effects=fixed_effects,
                                                    conf_level=conf_level,
                                                    selected_cov=self._selected_cov_to_select_col(selected_cov), covs_to_values = self._covs_to_values_to_cols_to_values(covs_to_values),
                                                    data_type=OMA_CONVENTION[data_type],
                                                    bootstrap_params = bootstrap_params)

            else:
                result = python_to_R.run_meta_regression(metric=metric,
                                                         fixed_effects=fixed_effects,
                                                         conf_level=conf_level,
                                                         random_effects_method = random_effects_method,
                                                         selected_cov=selected_cov, covs_to_values = covs_to_values)
                if MAKE_TESTS:
                    self._writeout_test_parameters("python_to_R.run_meta_regression", make_dataset_r_str, result,
                                                    metric=metric,
                                                    fixed_effects=fixed_effects,
                                                    conf_level=conf_level,
                                                    selected_cov=self._selected_cov_to_select_col(selected_cov), covs_to_values = self._covs_to_values_to_cols_to_values(covs_to_values),)
            
        finally:
            bar.hide()
        self._display_results(result, summary)
        
    def run_gmeta_regression(self,
                             metric, data_type, included_studies,
                             data_location, covariates, interactions,
                             fixed_effects, conf_level, random_effects_method,
                             summary=""):
        
        model = self._get_model()
        
        
        bar = MetaProgress()
        
        # Make dataframe of data with associates covariates
        
        
        # Call python_to_R gmeta regression routine
        result = python_to_R.run_gmeta_regression(metric, fixed_effects, data_name, results_name, conf_level, random_effects_method, selected_cov, covs_to_values)
        
        self._display_results(result, summary)
        bar.show()
        bar.deleteLater()
        
    def phylo_analysis(self):
        wizard = PhyloWizard()
        if wizard.exec_():
            # get selections
            phylo_object = wizard.get_phylo_object()
            # run analysis and display results window
            print("Here is the phylo object: %s" % phylo_object)
            
#             try:
#                 result = python_to_R.run_histogram(model=self.model,
#                                                    var=var,
#                                                    params=params,
#                                                    res_name = "result", var_name = "tmp_obj", summary="")
#             except CrazyRError as e:
#                 if SOUND_EFFECTS:
#                     silly.play()
#                 QMessageBox.critical(self, "Oops", str(e))
#  
#             self.analysis(result, summary="")
    
    #### PUBLICATION BIAS ####
    
    def failsafe_analysis(self):
        model = self._get_model()
        
        wizard = ma_wizard.MetaAnalysisWizard(model=model,
                                              mode=FAILSAFE_MODE,
                                              parent=self.main_form)
        if wizard.exec_():
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            failsafe_parameters = wizard.get_failsafe_parameters()
            summary = wizard.get_summary()
            
            # figure out the data type
            var = model.get_variable_assigned_to_column(data_location['effect_size'])
            var_grp = model.get_variable_group_of_var(var)
            metric = var_grp.get_metric()
            data_type = get_data_type_for_metric(metric)
            
            # Save selections made for next analysis
            model.update_data_location_choices(data_type, data_location)     # save data locations choices for this data type in the model
            model.update_previously_included_studies(set(included_studies))  # save which studies were included on last meta-regression
            model.update_last_failsafe_parameters(failsafe_parameters)
            
            result = python_to_R.run_failsafe_analysis(model, included_studies, data_location, failsafe_parameters)
            self._display_results(result, summary)
    
        
    def funnel_plot_analysis(self):
        model = self._get_model()
        
        wizard = ma_wizard.MetaAnalysisWizard(model=model,
                                  mode=FUNNEL_MODE,
                                  parent=self.main_form)
        if wizard.exec_():
            meta_f_str = wizard.get_modified_meta_f_str()
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            current_param_vals = wizard.get_plot_params()
            chosen_method = wizard.get_current_method()
            funnel_params = wizard.get_funnel_parameters() # funnel params in R-ish format
            summary = wizard.get_summary()

            # Save selections made for next analysis
            model.update_data_type_selection(data_type)    # int
            model.update_metric_selection(metric)          # int
            model.update_method_selection(chosen_method)   #int??? str??
            model.update_ma_param_vals(current_param_vals)
            model.update_data_location_choices(data_type, data_location)     # save data locations choices for this data type in the model
            model.update_previously_included_studies(set(included_studies))  # save which studies were included on last meta-regression
            model.update_funnel_params(funnel_params)

            try:
                result = python_to_R.run_funnelplot_analysis(
                                                 model=model,
                                                 included_studies=included_studies,
                                                 data_type=data_type,
                                                 metric=metric,
                                                 data_location=data_location, 
                                                 ma_params=current_param_vals,
                                                 funnel_params=funnel_params,
                                                 fname=chosen_method,
                                                 res_name = "result",
                                                 var_name = "tmp_obj",
                                                 summary="")
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))

            self._display_results(result, summary)
    
    ### DATA EXPLORATION ####
    def histogram(self):
        model = self._get_model()
        
        prev_hist_var = None      # TODO: get from model
        old_histogram_params = {} # TODO: get from model
        wizard = data_exploration_wizards.HistogramWizard(model=model,
                                                          old_histogram_params=old_histogram_params,
                                                          prev_hist_var=prev_hist_var)
        if wizard.exec_():
            # get selections
            var = wizard.get_selected_var()
            params = wizard.get_histogram_params()
            
            # store selections for next analysis
            
            # run analysis and display results window
            print("selected var is: %s" % var.get_label())
            print("params are: %s" % params)
            
            try:
                result = python_to_R.run_histogram(model=model,
                                                   var=var,
                                                   params=params,
                                                   res_name="result", var_name="tmp_obj", 
                                                   summary="")
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
 
            self._display_results(result, summary="")
            
    def scatterplot(self):
        model=self._get_model()
        
        prev_scatterplot_data = None # TODO: get from model
        old_scatterplot_params = {}  # TODO: get from model
        wizard = data_exploration_wizards.ScatterPlotWizard(model=model,
                                old_scatterplot_params=old_scatterplot_params,
                                prev_scatterplot_data=prev_scatterplot_data)
        
        if wizard.exec_():
            # get selections
            xvar = wizard.get_selected_vars()['x']
            yvar = wizard.get_selected_vars()['y']
            params = wizard.get_scatterplot_params()

            # store selections for next analysis
            
            # run analysis and display results window
            print("xvar is: %s, yvar is: %s" % (xvar.get_label(), yvar.get_label()))
            print("params are: %s" % params)
            try:
                result = python_to_R.run_scatterplot(model=model,
                                                     xvar=xvar,
                                                     yvar=yvar,
                                                     params=params)
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
 
            self._display_results(result, summary="")
    
            
    #### RESULTS OUTPUT ####

    def _display_results(self, results, summary=""):
        if results is None:
            return # analysis failed
        else: # analysis succeeded
            form = results_window.ResultsWindow(
                    results=results,
                    show_additional_values=self._show_additional_values(),
                    show_analysis_selections=self._show_analysis_selections(),
                    summary=summary,
                    parent=self.main_form)
            form.show()





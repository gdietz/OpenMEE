##############################################################################
#
# Author: George Dietz
#
# Description: All the functions related to performing analysis should live
#              here
#
##############################################################################

# from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

import results_window
from ma_wizards import (
    RegularMetaAnalysisWizard,
    CumulativeMetaAnalysisWizard,
    LeaveOneOutMetaAnalysisWizard,
    SubgroupMetaAnalysisWizard,
    BootstrapMetaAnalysisWizard,
)
import meta_regression_wizard
import data_exploration_wizards
import python_to_R
from phylo.phylowizard import PhyloMAWizard
from ome_globals import *
from meta_progress import MetaProgress
from publication_bias_wizards import FunnelWizard, FailsafeWizard
from model_building.model_building_wizard import ModelBuildingWizard
from multiple_imputation_meta_analysis_wizard import MiMaWizard
from permutation_wizard import PermutationWizard
from dynamic_wizard import DynamicWizard

# catches an r exception, displays a message, returns None if there is an
# exception
# def CatchRError(function):
#     def _CatchRError(*args, **kw):
#         # stuff before
#         try:
#             res = function(*args, **kw)
#         except CrazyRError as e:
#             if SOUND_EFFECTS:
#                 silly.play()
#             QMessageBox.critical(self.main_form, "Oops", str(e))
#             res = None
#
#
#         # stuff after
#         return res
#     return _CatchRError


class Analyzer:
    def __init__(self, main_form):
        self.main_form = main_form

    def _get_model(self):
        return self.main_form.model

    # #### META ANALYSIS & META-REGRESSION ####
    def cum_ma(self):
        '''
        Cumulative Meta Analysis

        uses run_ma
        '''

        model = self._get_model()
        wizard = CumulativeMetaAnalysisWizard(
            model=model,
            parent=self.main_form,
        )

        if wizard.exec_():
            meta_f_str = wizard.get_modified_meta_f_str()
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            current_param_vals = wizard.get_plot_params()
            chosen_method = wizard.get_current_method()
            save_selections = wizard.save_selections()  # a bool
            summary = wizard.get_summary()

            if save_selections:
                # Save selections made for next analysis
                model.update_data_type_selection(data_type)    # int
                model.update_metric_selection(metric)          # int
                model.update_method_selection(chosen_method)   # int??? str??
                model.update_ma_param_vals(current_param_vals)
                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))

            try:
                result = self.run_ma(
                    included_studies,
                    data_type, metric,
                    data_location,
                    current_param_vals,
                    chosen_method,
                    meta_f_str,
                    covs_to_include=[],
                )
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
            self._display_results(result, summary)

    def loo_ma(self):
        model = self._get_model()
        wizard = LeaveOneOutMetaAnalysisWizard(
            model=model,
            parent=self.main_form,
        )

        if wizard.exec_():
            meta_f_str = wizard.get_modified_meta_f_str()
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            current_param_vals = wizard.get_plot_params()
            chosen_method = wizard.get_current_method()
            save_selections = wizard.save_selections()  # a bool
            summary = wizard.get_summary()

            if save_selections:
                # Save selections made for next analysis
                model.update_data_type_selection(data_type)    # int
                model.update_metric_selection(metric)          # int
                model.update_method_selection(chosen_method)   # int??? str??
                model.update_ma_param_vals(current_param_vals)
                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))

            try:
                result = self.run_ma(
                    included_studies,
                    data_type, metric,
                    data_location,
                    current_param_vals,
                    chosen_method,
                    meta_f_str,
                    covs_to_include=[],
                )
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
            self._display_results(result, summary)

    def bootstrap_ma(self):
        model = self._get_model()
        wizard = BootstrapMetaAnalysisWizard(model=model)

        if wizard.exec_():
            meta_f_str = wizard.get_modified_meta_f_str()
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            current_param_vals = wizard.get_plot_params()
            chosen_method = wizard.get_current_method()
            save_selections = wizard.save_selections()  # a bool
            summary = wizard.get_summary()
            # bootstrap specific
            bootstrap_params = wizard.get_bootstrap_params()
            bootstrap_params.update({
                'bootstrap.type': BOOTSTRAP_MODES_TO_STRING[BOOTSTRAP_MA]
            })
            current_param_vals.update(bootstrap_params)

            if save_selections:
                # Save selections made for next analysis
                model.update_data_type_selection(data_type)    # int
                model.update_metric_selection(metric)          # int
                model.update_method_selection(chosen_method)   # int??? str??
                model.update_ma_param_vals(current_param_vals)
                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))
                # bootstrap specific
                model.update_bootstrap_params_selection(
                    wizard.get_bootstrap_params(),
                )

            try:
                result = self.run_ma(
                    included_studies,
                    data_type,
                    metric,
                    data_location,
                    current_param_vals,
                    chosen_method,
                    meta_f_str,
                    covs_to_include=[],
                )
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
            self._display_results(result, summary)

    def subgroup_ma(self):
        model = self._get_model()

        wizard = SubgroupMetaAnalysisWizard(model=model, parent=self.main_form)

        if wizard.exec_():
            meta_f_str = wizard.get_modified_meta_f_str()
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            current_param_vals = wizard.get_plot_params()
            chosen_method = wizard.get_current_method()
            save_selections = wizard.save_selections()  # a bool
            summary = wizard.get_summary()
            # subgroup specific
            subgroup_variable = wizard.get_subgroup_variable()
            current_param_vals.update({
                "cov_name": subgroup_variable.get_label()
            })

            if save_selections:
                # Save selections made for next analysis
                model.update_data_type_selection(data_type)    # int
                model.update_metric_selection(metric)          # int
                model.update_method_selection(chosen_method)   # int??? str??
                model.update_ma_param_vals(current_param_vals)
                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))
                model.update_subgroup_var_selection(subgroup_variable)

            covs_to_include = [subgroup_variable, ]

            try:
                result = self.run_ma(
                    included_studies,
                    data_type,
                    metric,
                    data_location,
                    current_param_vals,
                    chosen_method,
                    meta_f_str,
                    covs_to_include=covs_to_include,
                )
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
            self._display_results(result, summary)

    def meta_analysis(self, meta_f_str=None, mode=MA_MODE):
        '''
        Spawns a wizard to get information in order to run a standard
        meta-analysis
        '''

        model = self._get_model()

        wizard = RegularMetaAnalysisWizard(model=model, parent=self.main_form)

        unmodified_meta_f_str = meta_f_str
        if wizard.exec_():
            meta_f_str = wizard.get_modified_meta_f_str()
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            current_param_vals = wizard.get_plot_params()
            chosen_method = wizard.get_current_method()
            save_selections = wizard.save_selections()  # a bool
            summary = wizard.get_summary()

            if save_selections:
                # Save selections made for next analysis
                model.update_data_type_selection(data_type)    # int
                model.update_metric_selection(metric)          # int
                model.update_method_selection(chosen_method)   # int??? str??
                model.update_ma_param_vals(current_param_vals)
                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))

            try:
                covs_to_include = []

                result = self.run_ma(
                    included_studies,
                    data_type,
                    metric,
                    data_location,
                    current_param_vals,
                    chosen_method,
                    meta_f_str,
                    covs_to_include=covs_to_include,
                )
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
            self._display_results(result, summary)

    def run_ma(
        self,
        included_studies,
        data_type,
        metric,
        data_location,
        current_param_vals,
        chosen_method,
        meta_f_str,
        covs_to_include=[],
    ):

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
                make_dataset_r_str = python_to_R.dataset_to_simple_binary_robj(
                    model=model,
                    included_studies=included_studies,
                    data_location=data_location,
                    covs_to_include=covs_to_include,
                )

                if meta_f_str is None:
                    result = python_to_R.run_binary_ma(
                        function_name=chosen_method,
                        params=current_param_vals,
                    )
                    # for making tests
                    if MAKE_TESTS:
                        self._writeout_test_parameters(
                            "python_to_R.run_binary_ma",
                            make_dataset_r_str,
                            result,
                            function_name=chosen_method,
                            params=current_param_vals,
                        )
                else:
                    result = python_to_R.run_meta_method(
                        meta_function_name=meta_f_str,
                        function_name=chosen_method,
                        params=current_param_vals,
                    )
                    if MAKE_TESTS:
                        self._writeout_test_parameters(
                            "python_to_R.run_meta_method",
                            make_dataset_r_str,
                            result,
                            meta_function_name=meta_f_str,
                            function_name=chosen_method,
                            params=current_param_vals,
                        )

            elif OMA_CONVENTION[data_type] == "continuous":
                make_dataset_r_str = python_to_R.dataset_to_simple_cont_robj(
                    model=model,
                    included_studies=included_studies,
                    data_location=data_location,
                    data_type=data_type,
                    covs_to_include=covs_to_include,
                )

                if meta_f_str is None:
                    # run standard meta-analysis
                    result = python_to_R.run_continuous_ma(
                        function_name=chosen_method,
                        params=current_param_vals,
                    )
                    if MAKE_TESTS:
                        self._writeout_test_parameters(
                            "python_to_R.run_continuous_ma",
                            make_dataset_r_str,
                            result,
                            function_name=chosen_method,
                            params=current_param_vals,
                        )
                else:
                    # get meta!
                    result = python_to_R.run_meta_method(
                        meta_function_name=meta_f_str,
                        function_name=chosen_method,
                        params=current_param_vals,
                    )
                    if MAKE_TESTS:
                        self._writeout_test_parameters(
                            "python_to_R.run_meta_method",
                            make_dataset_r_str,
                            result,
                            meta_function_name=meta_f_str,
                            function_name=chosen_method,
                            params=current_param_vals,
                        )

                # FOR MAKING TESTS
                # _writeout_test_data(
                #     meta_f_str,
                #     self.current_method,
                #     current_param_vals, result,
                # )
        finally:
            bar.hide()

        return result

    def gmeta_regression(self):
        model = self._get_model()

        wizard = meta_regression_wizard.MetaRegressionWizard(
            model=model,
            parent=self.main_form,
        )

        if wizard.exec_():
            # Selections to store
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            covariates = wizard.get_included_covariates()
            interactions = wizard.get_included_interactions()
            fixed_effects = wizard.using_fixed_effects()
            conf_level = wizard.get_conf_level()
            random_effects_method = wizard.get_random_effects_method()
            cov_2_ref_values = wizard.get_covariate_reference_levels()

            # Unstored selections
            phylogen = wizard.get_phylogen()
            analysis_type = wizard.get_analysis_type()
            output_type = wizard.get_output_type()
            summary = wizard.get_summary()
            save_selections = wizard.save_selections()  # a bool
            btt = wizard.get_btt()

            if analysis_type == PARAMETRIC:
                if output_type == NORMAL:
                    mode = META_REG_MODE
                elif output_type == CONDITIONAL_MEANS:
                    mode = META_REG_COND_MEANS
            elif analysis_type == BOOTSTRAP:
                if output_type == NORMAL:
                    mode = BOOTSTRAP_META_REG
                elif output_type == CONDITIONAL_MEANS:
                    mode = BOOTSTRAP_META_REG_COND_MEANS

            if mode in [META_REG_COND_MEANS, BOOTSTRAP_META_REG_COND_MEANS]:
                (
                    selected_cov,
                    covs_to_values,
                ) = wizard.get_meta_reg_cond_means_info()
            else:
                (selected_cov, covs_to_values) = (None, None)

            if mode in [BOOTSTRAP_META_REG, BOOTSTRAP_META_REG_COND_MEANS]:
                bootstrap_params = wizard.get_bootstrap_params()
                bootstrap_params.update({
                    'bootstrap.type': BOOTSTRAP_MODES_TO_STRING[mode],
                })

                num_replicates = bootstrap_params['num.bootstrap.replicates']
                histogram_title = bootstrap_params['histogram.title']
            else:
                bootstrap_params = {}

            print("Covariates to reference values: %s" % str(cov_2_ref_values))

            if save_selections:
                # Save analysis analysis info that we just gathered
                model.update_data_type_selection(data_type)  # int
                model.update_metric_selection(metric)  # int
                # fixed effects: bool
                model.update_fixed_vs_random_effects_selection(fixed_effects)
                model.update_conf_level_selection(conf_level)  # double
                # cov_2_ref_values: dict
                model.update_cov_2_ref_values_selection(cov_2_ref_values)
                model.update_bootstrap_params_selection(bootstrap_params)
                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))
                # save which covariates were included on last meta-regression
                model.update_previously_included_covariates(set(covariates))
                model.update_selected_cov_and_covs_to_values(
                    selected_cov,
                    covs_to_values,
                )
                model.update_random_effects_method(random_effects_method)

            try:
                if mode == META_REG_MODE:
                    result = self.run_gmeta_regression(
                        included_studies=included_studies,
                        data_location=data_location,
                        covariates=covariates,
                        cov_ref_values=cov_2_ref_values,
                        interactions=interactions,
                        fixed_effects=fixed_effects,
                        conf_level=conf_level,
                        random_effects_method=random_effects_method,
                        metric=metric,
                        btt=btt,
                    )
                elif mode == META_REG_COND_MEANS:
                    result = self.run_gmeta_regression_cond_means(
                        selected_cov=selected_cov,
                        covs_to_values=covs_to_values,
                        included_studies=included_studies,
                        data_location=data_location,
                        covariates=covariates,
                        cov_ref_values=cov_2_ref_values,
                        interactions=interactions,
                        fixed_effects=fixed_effects,
                        conf_level=conf_level,
                        random_effects_method=random_effects_method,
                        btt=btt,
                    )
                elif mode == BOOTSTRAP_META_REG:
                    result = self.run_gmeta_regression_bootstrapped(
                        num_replicates=num_replicates,
                        histogram_title=histogram_title,
                        included_studies=included_studies,
                        data_location=data_location,
                        covariates=covariates,
                        cov_ref_values=cov_2_ref_values,
                        interactions=interactions,
                        fixed_effects=fixed_effects,
                        conf_level=conf_level,
                        random_effects_method=random_effects_method,
                        btt=btt,
                    )
                elif mode == BOOTSTRAP_META_REG_COND_MEANS:
                    result = self.run_gmeta_regression_bootstrapped_cond_means(
                        num_replicates=num_replicates,    # bootstrap
                        histogram_title=histogram_title,  # bootstrap
                        selected_cov=selected_cov,        # cond means
                        covs_to_values=covs_to_values,    # cond means
                        included_studies=included_studies,
                        data_location=data_location,
                        covariates=covariates,
                        cov_ref_values=cov_2_ref_values,
                        interactions=interactions,
                        fixed_effects=fixed_effects,
                        conf_level=conf_level,
                        random_effects_method=random_effects_method,
                        btt=btt,
                    )

            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
            self._display_results(result, summary)

    def run_gmeta_regression(
        self,
        included_studies,
        data_location,
        covariates,
        cov_ref_values,
        interactions,
        fixed_effects,
        conf_level,
        random_effects_method,
        metric,
        digits=3,
        btt=None,
    ):

        model = self._get_model()

        bar = MetaProgress()
        bar.show()

        # Make dataframe of data with associated covariates
        python_to_R.dataset_to_dataframe(
            model=model,
            included_studies=included_studies,
            data_location=data_location,
            covariates=covariates,
            cov_ref_values=cov_ref_values,
            var_name="tmp_obj",
        )

        result = python_to_R.run_gmeta_regression(
            covariates=covariates,
            interactions=interactions,
            fixed_effects=fixed_effects,
            random_effects_method=random_effects_method,
            digits=digits,
            conf_level=conf_level,
            metric=metric,
            btt=btt,
            data_name="tmp_obj",
        )

        bar.hide()
        bar.deleteLater()
        return result

    def run_gmeta_regression_cond_means(
        self,
        included_studies,
        data_location,
        covariates,
        cov_ref_values,
        interactions,
        fixed_effects,
        conf_level,
        random_effects_method,
        selected_cov,
        covs_to_values,
        digits=4,
        btt=None,
    ):

        model = self._get_model()

        bar = MetaProgress()
        bar.show()

        # Make dataframe of data with associated covariates + interactions
        python_to_R.dataset_to_dataframe(
            model=model,
            included_studies=included_studies,
            data_location=data_location,
            covariates=covariates,
            cov_ref_values=cov_ref_values,
            var_name="tmp_obj",
        )

        result = python_to_R.run_gmeta_regression_cond_means(
            selected_cov=selected_cov,
            covs_to_values=covs_to_values,
            covariates=covariates,
            interactions=interactions,
            fixed_effects=fixed_effects,
            random_effects_method=random_effects_method,
            digits=digits,
            conf_level=conf_level,
            btt=btt,
            data_name="tmp_obj",
        )

        bar.hide()
        bar.deleteLater()
        return result

    def run_gmeta_regression_bootstrapped(
        self,
        num_replicates,
        histogram_title,  # for bootstrap
        included_studies,
        data_location,
        covariates,
        cov_ref_values,
        interactions,
        fixed_effects,
        conf_level,
        random_effects_method,
        digits=4,
        btt=None,
    ):

        model = self._get_model()

        bar = MetaProgress()
        bar.show()

        # Make dataframe of data with associated covariates + interactions
        python_to_R.dataset_to_dataframe(
            model=model,
            included_studies=included_studies,
            data_location=data_location,
            covariates=covariates,
            cov_ref_values=cov_ref_values,
            var_name="tmp_obj",
        )

        result = python_to_R.run_gmeta_regression_bootstrapped(
            num_replicates=num_replicates,
            histogram_title=histogram_title,
            covariates=covariates,
            interactions=interactions,
            fixed_effects=fixed_effects,
            random_effects_method=random_effects_method,
            digits=digits,
            conf_level=conf_level,
            btt=btt,
            data_name="tmp_obj",
        )

        bar.hide()
        bar.deleteLater()
        return result

    def run_gmeta_regression_bootstrapped_cond_means(
        self,
        num_replicates,
        histogram_title,  # for bootstrap
        included_studies,
        data_location,
        covariates,
        cov_ref_values,
        interactions,
        fixed_effects,
        conf_level,
        random_effects_method,
        selected_cov,
        covs_to_values,
        digits=4,
        btt=None
    ):

        model = self._get_model()

        bar = MetaProgress()
        bar.show()

        # Make dataframe of data with associated covariates + interactions
        python_to_R.dataset_to_dataframe(
            model=model,
            included_studies=included_studies,
            data_location=data_location,
            covariates=covariates,
            cov_ref_values=cov_ref_values,
            var_name="tmp_obj",
        )

        result = python_to_R.run_gmeta_regression_bootstrapped_cond_means(
            num_replicates=num_replicates,
            histogram_title=histogram_title,  # for bootstrap
            selected_cov=selected_cov,
            covs_to_values=covs_to_values,
            covariates=covariates,
            interactions=interactions,
            fixed_effects=fixed_effects,
            random_effects_method=random_effects_method,
            digits=digits,
            conf_level=conf_level,
            btt=btt,
            data_name="tmp_obj",
        )

        bar.hide()
        bar.deleteLater()
        return result

    # #### PUBLICATION BIAS ####

    def failsafe_analysis(self):
        model = self._get_model()

        wizard = FailsafeWizard(model=model, parent=self.main_form)

        if wizard.exec_():
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            failsafe_parameters = wizard.get_failsafe_parameters()
            summary = wizard.get_summary()
            save_selections = wizard.save_selections()  # a bool

            # figure out the data type
            var = model.get_variable_assigned_to_column(
                data_location['effect_size'],
            )
            var_grp = model.get_variable_group_of_var(var)
            metric = var_grp.get_metric()
            data_type = get_data_type_for_metric(metric)

            if save_selections:
                # Save selections made for next analysis
                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))
                model.update_last_failsafe_parameters(failsafe_parameters)

            result = python_to_R.run_failsafe_analysis(
                model,
                included_studies,
                data_location,
                failsafe_parameters,
            )
            self._display_results(result, summary)

    def funnel_plot_analysis(self):
        model = self._get_model()
        wizard = FunnelWizard(model=model, parent=self.main_form)

        if wizard.exec_():
            meta_f_str = wizard.get_modified_meta_f_str()
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            current_param_vals = wizard.get_plot_params()
            chosen_method = wizard.get_current_method()
            # funnel params in R-ish format
            funnel_params = wizard.get_funnel_parameters()
            summary = wizard.get_summary()
            save_selections = wizard.save_selections()  # a bool

            if save_selections:
                # Save selections made for next analysis
                model.update_data_type_selection(data_type)    # int
                model.update_metric_selection(metric)          # int
                model.update_method_selection(chosen_method)   # int??? str??
                model.update_ma_param_vals(current_param_vals)
                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))
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
                    res_name="result",
                    var_name="tmp_obj",
                    summary="",
                )
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))

            self._display_results(result, summary)

    # ### DATA EXPLORATION ####
    def histogram(self):
        model = self._get_model()

        prev_hist_var = None       # TODO: get from model
        old_histogram_params = {}  # TODO: get from model
        wizard = data_exploration_wizards.HistogramWizard(
            model=model,
            old_histogram_params=old_histogram_params,
            prev_hist_var=prev_hist_var,
        )
        if wizard.exec_():
            # get selections
            var = wizard.get_selected_var()
            params = wizard.get_histogram_params()

            # TODO: store selections for next analysis

            # run analysis and display results window
            print("selected var is: %s" % var.get_label())
            print("params are: %s" % params)

            try:
                result = python_to_R.run_histogram(
                    model=model,
                    var=var,
                    params=params,
                    res_name="result",
                    var_name="tmp_obj",
                )
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))

            self._display_results(result, summary="")

    def scatterplot(self):
        model = self._get_model()

        prev_scatterplot_data = None  # TODO: get from model
        old_scatterplot_params = {}   # TODO: get from model
        wizard = data_exploration_wizards.ScatterPlotWizard(
            model=model,
            old_scatterplot_params=old_scatterplot_params,
            prev_scatterplot_data=prev_scatterplot_data,
        )

        if not wizard.exec_():
            return

        # get selections
        xvar = wizard.get_selected_vars()['x']
        yvar = wizard.get_selected_vars()['y']
        params = wizard.get_scatterplot_params()
        label_points_with_study_names = wizard.get_annotate_plot_with_study_labels()

        # TODO: store selections for next analysis

        # run analysis and display results window
        print("xvar is: %s, yvar is: %s" % (
            xvar.get_label(),
            yvar.get_label(),
        ))
        print("params are: %s" % params)
        try:
            result = python_to_R.run_scatterplot(
                model=model,
                xvar=xvar,
                yvar=yvar,
                params=params,
                label_points_with_study_names=label_points_with_study_names,
            )
        except CrazyRError as e:
            if SOUND_EFFECTS:
                silly.play()
            QMessageBox.critical(self.main_form, "Oops", str(e))

        self._display_results(result, summary="")

    def dynamic_data_exploration_analysis(self, analysis_details):
        '''
        Creates a custom data exploration analysis

        analysis_details:
            a dictionary expected to be of the following
            structure:

            {
                'MAIN': string,                 # R analysis function
                'WIZARD.WINDOW.TITLE': string,  # Title of wizard window
                'WIZARD.PAGES': {
                    'NAME OF WIZARD PAGE1': {
                        wizard page parameters
                    },
                    'NAME OF WIZARD PAGE2': {
                        wizard page parameters
                    },
                    ......,
                }
            }
        '''
        model = self._get_model()

        wizard = DynamicWizard(
            model=model,
            parent=self.main_form,
            wizard_parameters=analysis_details,
        )

        if wizard.exec_():
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            summary = wizard.get_summary()
            save_selections = wizard.save_selections()  # a bool

            result = python_to_R.run_dynamic_data_exploration_analysis(
                model,
                included_studies,
                data_location,
                analysis_details)
            self._display_results(result, summary)

    # #### RESULTS OUTPUT ####

    def _display_results(self, results, summary=""):
        if results is None:
            return  # analysis failed
        else:  # analysis succeeded
            show_additional_values = get_setting("show_additional_values")
            show_analysis_selections = get_setting("show_analysis_selections")

            form = results_window.ResultsWindow(
                results=results,
                show_additional_values=show_additional_values,
                show_analysis_selections=show_analysis_selections,
                summary=summary,
                parent=self.main_form,
            )
            form.show()

    def model_building(self):
        model = self._get_model()

        wizard = ModelBuildingWizard(
            model=model,
            parent=self.main_form,
        )

        if wizard.exec_():
            # Selections to store
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            fixed_effects = wizard.using_fixed_effects()
            conf_level = wizard.get_conf_level()
            random_effects_method = wizard.get_random_effects_method()
            cov_2_ref_values = wizard.get_covariate_reference_levels()
            # consists of a list of dictionaries
            models = wizard.get_models_info()

            # Unstored selections
            phylogen = wizard.get_phylogen()
            summary = wizard.get_summary()
            save_selections = wizard.save_selections()  # a bool

            if save_selections:
                # Save analysis analysis info that we just gathered
                model.update_data_type_selection(data_type)  # int
                model.update_metric_selection(metric)  # int
                # fixed effects:
                model.update_fixed_vs_random_effects_selection(fixed_effects)
                model.update_conf_level_selection(conf_level)  # double
                # cov_2_ref_values: dict
                model.update_cov_2_ref_values_selection(cov_2_ref_values)
                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))
                model.update_random_effects_method(random_effects_method)

            try:
                result = self.run_model_building(
                    included_studies=included_studies,
                    data_location=data_location,
                    cov_ref_values=cov_2_ref_values,
                    fixed_effects=fixed_effects,
                    conf_level=conf_level,
                    model_info=models,  # regression model info
                    random_effects_method=random_effects_method,
                )

            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
            self._display_results(result, summary)

    def run_model_building(
        self,
        included_studies,
        data_location,
        cov_ref_values,
        fixed_effects,
        conf_level,
        random_effects_method,
        model_info,
        digits=4,
    ):

        model = self._get_model()

        bar = MetaProgress()
        bar.show()

        # Combine all the covariates together (sort of unnecessary using a loop
        # since the first info object will have all the necessary covariates
        # but whatever, this is fast anyway.)
        covariates = set()
        for info in model_info:
            model_covs = info['covariates']
            covariates.update(set(model_covs))
        covariates = list(covariates)

        # Make dataframe of data with associated covariates + interactions
        python_to_R.dataset_to_dataframe(
            model=model,
            included_studies=included_studies,
            data_location=data_location,
            covariates=covariates,
            cov_ref_values=cov_ref_values,
            var_name="tmp_obj",
        )

        result = python_to_R.run_model_building(
            model_info=model_info,
            fixed_effects=fixed_effects,
            random_effects_method=random_effects_method,
            digits=digits,
            conf_level=conf_level,
            data_name="tmp_obj",
        )

        bar.hide()
        bar.deleteLater()
        return result

# ################## phylogenetic analysis issue #15 #########################
    def phylo_ma(self, digits=4):
        model = self._get_model()

        wizard = PhyloMAWizard(
            model=model,
            parent=self.main_form,
        )

        if wizard.exec_():
            # Selections to store
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            # fixed_effects = wizard.using_fixed_effects()
            fixed_effects = False
            conf_level = wizard.get_conf_level()
            random_effects_method = wizard.get_random_effects_method()
            # cov_2_ref_values = wizard.get_covariate_reference_levels()

            # Unstored selections
            summary = wizard.get_summary()
            save_selections = wizard.save_selections()  # a bool
            tree_filepath = wizard.get_tree_filepath_and_format()['filepath']
            tree_format = wizard.get_tree_filepath_and_format()['format']
            evo_model = wizard.get_phylo_model_type()
            lambda_, alpha = wizard.get_lambda(), wizard.get_alpha()
            include_species = wizard.get_include_species_as_random_factor()
            current_param_vals = wizard.get_plot_params()

            if save_selections:
                # Save analysis analysis info that we just gathered
                model.update_data_type_selection(data_type)  # int
                model.update_metric_selection(metric)  # int
                # fixed_effects: bool
                model.update_fixed_vs_random_effects_selection(fixed_effects)
                model.update_conf_level_selection(conf_level)  # double
                # cov_2_ref_values: dict
                # model.update_cov_2_ref_values_selection(cov_2_ref_values)
                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))
                model.update_random_effects_method(random_effects_method)

            try:
                result = self.run_phylo_ma(
                    tree_path=tree_filepath,
                    tree_format=tree_format,
                    evo_model=evo_model,
                    lambda_=lambda_,
                    alpha=alpha,
                    include_species=include_species,
                    included_studies=included_studies,
                    data_location=data_location,
                    conf_level=conf_level,
                    random_effects_method=random_effects_method,
                    digits=digits,
                    plot_params=current_param_vals,
                    metric=metric,
                )
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
            self._display_results(result, summary)

    def run_phylo_ma(
        self,
        tree_path,
        tree_format,
        evo_model,
        lambda_,
        alpha,
        include_species,
        included_studies,
        data_location,
        conf_level,
        random_effects_method,
        plot_params,
        metric,
        digits=4,
    ):

        model = self._get_model()

        bar = MetaProgress()
        bar.show()

        plot_params["measure"] = METRIC_TO_ESCALC_MEASURE[metric]
        plot_params["digits"] = digits

        # Make dataframe of data with associated covariates + interactions
        python_to_R.dataset_to_dataframe(
            model=model,
            included_studies=included_studies,
            data_location=data_location,
            var_name="tmp_obj",
        )

        result = python_to_R.run_phylo_ma(
            tree_path,
            tree_format,
            evo_model,
            random_effects_method,
            lambda_, alpha,
            include_species,
            fixed_effects=False,
            digits=digits,
            conf_level=conf_level,
            plot_params=plot_params,
        )

        bar.hide()
        bar.deleteLater()
        return result

    # #################### Multiply imputed meta analysis ####################

    def mi_meta_analysis(self):
        model = self._get_model()

        wizard = MiMaWizard(model=model, parent=self.main_form)
        if wizard.exec_():
            data_type, metric = wizard.get_data_type_and_metric()
            data_location = wizard.get_data_location()
            included_studies = wizard.get_included_studies_in_proper_order()
            # R list of imputation results
            imputations = wizard.get_imputations()
            # get parameters like method, digits, etc
            ma_details = wizard.get_analysis_parameters()
            covariates_for_regression = wizard.get_included_covariates()
            covariates_for_imputation = wizard.get_covariates_for_imputation()
            cov_ref_values = wizard.get_covariate_reference_levels()
            interactions = wizard.get_included_interactions()

            save_selections = wizard.save_selections()  # a bool
            summary = wizard.get_summary()

            if save_selections:
                # Save selections made for next analysis
                model.update_data_type_selection(data_type)    # int
                model.update_metric_selection(metric)          # int
                # model.update_method_selection(chosen_method)   #int??? str??

                # save data locations choices for this data type in the model
                model.update_data_location_choices(data_type, data_location)
                # save which studies were included on last meta-regression
                model.update_previously_included_studies(set(included_studies))

            try:
                result = self.run_mi_ma(
                    included_studies=included_studies,
                    data_type=data_type,
                    metric=metric,
                    data_location=data_location,
                    ma_params=ma_details,
                    imputations=imputations,
                    cov_ref_values=cov_ref_values,
                    reg_covariates=covariates_for_regression,
                    imp_covariates=covariates_for_imputation,
                    interactions=interactions,
                )
            except CrazyRError as e:
                if SOUND_EFFECTS:
                    silly.play()
                QMessageBox.critical(self.main_form, "Oops", str(e))
            self._display_results(result, summary)

    # run multiply imputed meta analysis

    def run_mi_ma(
        self,
        included_studies,
        data_type,
        metric,
        data_location,
        ma_params,
        imputations,
        cov_ref_values={},
        reg_covariates=[],
        imp_covariates=[],
        interactions=[],
    ):
        '''
        run_mi_ma

        Parameters:
            included_studies
            data_type
            metric
            data_location
            ma_params - regression details includes: method, confidence level,
                        digits, zero cell correction factor, etc.
            imputations - R list of imputed covariates
            cov_ref_values
            reg_covariates - regression covariates
            imp_covariates - imputation covariates
            interactions
        '''

        model = self._get_model()

        bar = MetaProgress()
        bar.show()

        # regression and imputation covaraites
        all_covs = set(reg_covariates+imp_covariates)
        # Make dataframe of data with associated covariates (both those for
        # imputation and for regression)
        original_dataset = python_to_R.dataset_to_dataframe(
            model=model,
            included_studies=included_studies,
            data_location=data_location,
            covariates=all_covs,
            cov_ref_values=cov_ref_values)

        # Make R list of datasets with imputed data and insert into workspace
        imputed_datasets_name = "imputed.datasets"
        python_to_R.make_imputed_datasets(
            original_dataset,
            imputations,
            imputed_datasets_name=imputed_datasets_name,
        )

        result = python_to_R.run_multiple_imputation_meta_analysis(
            ma_params,
            covariates=reg_covariates,
            interactions=interactions,
            imputed_datasets_name=imputed_datasets_name,
            results_name="results_obj",
        )

        bar.hide()
        bar.deleteLater()
        return result

    def PermutationAnalysis(self, meta_reg_mode):
        model = self._get_model()
        wizard = PermutationWizard(
            model=model,
            meta_reg_mode=meta_reg_mode,
            parent=self.main_form,
        )
        # get out of the analysis if we quit the wizard
        if not wizard.exec_():
            return

        parameters = wizard.get_parameters()
        summary = wizard.get_summary()
        try:
            result = self.run_permutation_analysis(parameters, meta_reg_mode)
        except CrazyRError as e:
            if SOUND_EFFECTS:
                silly.play()
            QMessageBox.critical(self.main_form, "Oops", str(e))
        self._display_results(result, summary)

    def run_permutation_analysis(self, parameters, meta_reg_mode):
        model = self._get_model()
        bar = MetaProgress()
        bar.show()

        # Make dataframe of data with associated covariates
        if meta_reg_mode:
            python_to_R.dataset_to_dataframe(
                model=model,
                included_studies=parameters['studies'],
                data_location=parameters['data_location'],
                covariates=parameters['covariates'],
                cov_ref_values=parameters['reference_values'],
                var_name="tmp_obj",
            )
        else:
            python_to_R.dataset_to_dataframe(
                model=model,
                included_studies=parameters['studies'],
                data_location=parameters['data_location'],
                var_name="tmp_obj",
            )

        print("Running PermutationAnalysis with parameters %s", parameters)
        result = python_to_R.run_permutation_analysis(
            parameters, meta_reg_mode)

        bar.hide()
        bar.deleteLater()
        return result

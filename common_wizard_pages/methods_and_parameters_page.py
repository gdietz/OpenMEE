##################
#                #
# George Dietz   #
# Byron Wallace  #
# CEBM@Brown     #################
#                                #
# This is basically a modified   #
# version of the same thing from #
# OpenMetaAnalyst                #
##################################

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from ome_globals import *

import python_to_R
import ui_methods_and_parameters_page

class MethodsAndParametersPage(QWizardPage, ui_methods_and_parameters_page.Ui_WizardPage):
    def __init__(self, model, meta_f_str=None, external_params=None, disable_forest_plot_tab=False, funnel_mode=False, parent=None):
        super(MethodsAndParametersPage, self).__init__(parent)
        self.setupUi(self)
        
        self.external_params = external_params
        self.model = model
        self.meta_f_str = meta_f_str
        self.funnel_mode = funnel_mode
        
        # previous values not restored currently
        self.default_method     = self.model.get_method_selection()
        self.default_param_vals = self.model.get_ma_param_vals()
        
        if disable_forest_plot_tab:
            self.specs_tab.setTabEnabled(1, False)
        
    def initializePage(self):
        self.current_param_vals = self.external_params or {}
        
        self.data_type, self.metric = self.wizard().get_data_type_and_metric()
        self.data_location = self.wizard().get_data_location()
        
        QObject.connect(self.save_btn, SIGNAL("pressed()"), self.select_out_path)
        QObject.connect(self.method_cbo_box, SIGNAL("currentIndexChanged(QString)"), self.method_changed)
        
        if self.meta_f_str is not None:
            # we pre-prend the data type to the meta-method function
            # name. thus the caller (meta_form) needn't worry about
            # the data type, only about the method name (e.g., cumulative)
            
            if not self.meta_f_str.endswith(OMA_CONVENTION[self.data_type]): 
                self.meta_f_str = ".".join((self.meta_f_str, OMA_CONVENTION[self.data_type]))
                
        if self.data_type != TWO_BY_TWO_CONTINGENCY_TABLE:
            self.disable_bin_only_fields()
            
#        # disable second arm display for one-arm analyses
#        if self.model.current_effect in ONE_ARM_METRICS:
#            self.setup_fields_for_one_arm()

        self.current_widgets = []
        self.current_method = None
        self.current_params = None
        self.current_defaults = None
        self.var_order = None
        
        self.populate_cbo_box()
    
    def get_included_studies_in_proper_order(self):
        return self.wizard().get_included_studies_in_proper_order()
        
    def get_modified_meta_f_str(self):
        return self.meta_f_str

    def select_out_path(self):
        out_f = "."
        out_f = unicode(QFileDialog.getSaveFileName(self, "OpenMeta[analyst] - Plot Path",
                                                    out_f, "png image files: (.png)"))
        if out_f == "" or out_f == None:
            return None
        else:
            self.image_path.setText(out_f)
            
    def disable_bin_only_fields(self):
        self.col3_str_edit.setEnabled(False)
        self.col4_str_edit.setEnabled(False)
        self.show_3.setChecked(False)
        self.show_3.setEnabled(False)
        self.show_4.setChecked(False)
        self.show_4.setEnabled(False)
        
    def method_changed(self):
        if self.parameter_grp_box.layout() is not None:
            print("Layout items count before: %d" % self.parameter_grp_box.layout().count())
        self.clear_param_ui()
        self.current_widgets= []
        self.current_method = self.available_method_d[str(self.method_cbo_box.currentText())]
        self.setup_params()
        self.parameter_grp_box.setTitle(self.current_method)
        self.ui_for_params()
        
    def clear_param_ui(self):
        for widget in self.current_widgets:
            widget.deleteLater()
            widget = None
            
    def ui_for_params(self):
        if self.parameter_grp_box.layout() is None:
            layout = QGridLayout()
            self.parameter_grp_box.setLayout(layout)

        cur_grid_row = 0
        
        # add the method description
        method_description = python_to_R.get_method_description(self.current_method)
        
        self.add_label(self.parameter_grp_box.layout(), cur_grid_row, \
                            "Description: %s" % method_description)
        cur_grid_row += 1
        

        if self.var_order is not None:
            for var_name in self.var_order:
                val = self.current_params[var_name]
                self.add_param(self.parameter_grp_box.layout(), cur_grid_row, var_name, val)
                cur_grid_row+=1
        else:
            # no ordering was provided; let's try and do something
            # sane with respect to the order in which parameters
            # are displayed.
            #
            # we want to add the parameters in groups, for example,
            # we add combo boxes (which will be lists of values) together,
            # followed by numerical inputs. thus we create an ordered list
            # of functions to check if the argument is the corresponding
            # type (float, list); if it is, we add it otherwise we pass. this isn't
            # the most efficient way to do things, but the number of parameters
            # is going to be relatively tiny anyway
            ordered_types = [lambda x: isinstance(x, list),
                             lambda x: isinstance(x, str) and x.lower()=="float"]

            for is_right_type in ordered_types:
                for key, val in self.current_params.items():
                    if is_right_type(val):
                        self.add_param(self.parameter_grp_box.layout(), cur_grid_row, key, val)
                        cur_grid_row+=1

        # do we need to set forest plot parameters? if not,
        # e.g., in the case of HSROC or other methdos that
        # don't use our forest plotting, we don't show the
        # corresponding tab for forest plot params.
        # @TODO this is hacky; plus, really we should keep
        # a list of methods that *DO* take forest plot params
        if self.current_method in METHODS_WITH_NO_FOREST_PLOT:
            self.plot_tab.setEnabled(False)
        else:
            self.plot_tab.setEnabled(True)
        
        
    def populate_cbo_box(self):
        print("populating combo box")
        
        self.method_cbo_box.clear()
        
        # we first build an R object with the current data. this is to pass off         
        # to the R side to check the feasibility of the methods over the current data.
        # i.e., we do not display methods that cannot be performed over the 
        # current data.
        tmp_obj_name = "tmp_obj"
        
        covs_to_include = []
        #if self.mode==SUBGROUP_MODE:
        #       covs_to_include = [self.wizard().get_subgroup_variable(),]
        covs_to_include = []
        
        if OMA_CONVENTION[self.data_type] == "binary":
            python_to_R.dataset_to_simple_binary_robj(self.model,
                                                      included_studies = self.get_included_studies_in_proper_order(),
                                                      data_location = self.data_location,
                                                      var_name = tmp_obj_name,
                                                      covs_to_include=covs_to_include,
                                                      one_arm=False)
        elif OMA_CONVENTION[self.data_type] == "continuous":
            python_to_R.dataset_to_simple_continuous_robj(model=self.model,
                                                          included_studies=self.get_included_studies_in_proper_order(),
                                                          data_location=self.data_location, 
                                                          data_type=self.data_type, 
                                                          var_name=tmp_obj_name, 
                                                          covs_to_include=covs_to_include,
                                                          one_arm=False)
            
        self.available_method_d = python_to_R.get_available_methods(
                                                for_data_type=OMA_CONVENTION[self.data_type],
                                                data_obj_name=tmp_obj_name,
                                                metric=self.metric,
                                                funnel_mode=self.funnel_mode)
        print "\n\navailable %s methods: %s" % (self.data_type, ", ".join(self.available_method_d.keys()))
        method_names = self.available_method_d.keys()
        method_names.sort(reverse=True)
        
        for method in method_names:
            self.method_cbo_box.addItem(method)
        self.current_method = self.available_method_d[str(self.method_cbo_box.currentText())]
        self.setup_params()
        self.parameter_grp_box.setTitle(self.current_method)

        
    def setup_params(self):
        # parses out information about the parameters of the current method
        # param_d holds (meta) information about the parameter -- it's a each param
        # itself maps to a dictionary with a pretty name and description (assuming
        # they were provided for the given param)
        self.current_params, self.current_defaults, self.var_order, self.param_d = \
                    python_to_R.get_params(self.current_method)

        ###
        # user selections overwrite the current parameter defaults.
        # ie., if the user has run this analysis before, the preferences
        # they selected then are automatically set as the defaults now.
        # these defaults, if they exist, are stored in the user_preferences 
        # dictionary

        # override default from openmetar with choice from table preferences
        self.current_defaults['digits'] = self.model.get_precision()
        print self.current_defaults
        
    def add_label(self, layout, cur_grid_row, name, tool_tip_text=None):
        lbl = QLabel(name, self.parameter_grp_box)
        if not tool_tip_text is None:
            lbl.setToolTip(tool_tip_text)
        self.current_widgets.append(lbl)
        layout.addWidget(lbl, cur_grid_row, 0)
        
    def add_enum(self, layout, cur_grid_row, name, values):
        '''
        Adds an enumeration to the UI, with the name and possible
        values as specified per the parameters.
        '''
       
        ### 
        # using the pretty name for the label now.
        self.add_label(layout, cur_grid_row, self.param_d[name]["pretty.name"], \
                                tool_tip_text=self.param_d[name]["description"])
        cbo_box = QComboBox()
        for index, value in enumerate(values):
            name_str = self._get_enum_item_pretty_name(name,value)
            cbo_box.addItem(name_str)  # TODO: replace value with pretty values
            cbo_box.setItemData(index, QVariant(value))

        if self.current_defaults.has_key(name):
            cbo_box.setCurrentIndex(cbo_box.findData(self.current_defaults[name]))
            self.current_param_vals[name] = self.current_defaults[name]

        QObject.connect(cbo_box, QtCore.SIGNAL("currentIndexChanged(int)"),
                                 self.set_param_f_from_itemdata(name))

        self.current_widgets.append(cbo_box)
        layout.addWidget(cbo_box, cur_grid_row, 1)
        
    def _get_enum_item_pretty_name(self, enum_name, item_name):
        if "rm.method.names" in self.param_d[enum_name]:
            if item_name in self.param_d[enum_name]["rm.method.names"]:
                return item_name + ": " + str(self.param_d[enum_name]["rm.method.names"][item_name])
        return item_name
    
    def add_float_box(self, layout, cur_grid_row, name):
        self.add_label(layout, cur_grid_row, self.param_d[name]["pretty.name"],\
                                tool_tip_text=self.param_d[name]["description"])
        # now add the float input line edit
        finput = QLineEdit()

        # if a default value has been specified, use it
        if self.current_defaults.has_key(name):
            finput.setText(str(self.current_defaults[name]))
            self.current_param_vals[name] = self.current_defaults[name]


        finput.setMaximumWidth(50)
        QObject.connect(finput, QtCore.SIGNAL("textChanged(QString)"),
                                 self.set_param_f(name, to_type=float))
        self.current_widgets.append(finput)
        layout.addWidget(finput, cur_grid_row, 1)
        
    def add_int_box(self, layout, cur_grid_row, name):
        self.add_label(layout, cur_grid_row, self.param_d[name]["pretty.name"],\
                                tool_tip_text=self.param_d[name]["description"])
        # now add the int input line edit
        iinput = QLineEdit()

        # if a default value has been specified, use it
        if self.current_defaults.has_key(name):
            iinput.setText(str(int(self.current_defaults[name])))
            self.current_param_vals[name] = self.current_defaults[name]

        iinput.setMaximumWidth(50)
        QObject.connect(iinput, QtCore.SIGNAL("textChanged(QString)"),
                                 self.set_param_f(name, to_type=int))
        self.current_widgets.append(iinput)
        layout.addWidget(iinput, cur_grid_row, 1)
        
    def add_param(self, layout, cur_grid_row, name, value):
        print "adding param. name: %s, value: %s" % (name, value)
        if isinstance(value, list):
            # then it's an enumeration of values
            self.add_enum(layout, cur_grid_row, name, value)
        elif value.lower() == "float":
            self.add_float_box(layout, cur_grid_row, name)
        elif value.lower() == "int":
            self.add_int_box(layout, cur_grid_row, name)
        # should we add an array type?
        elif value.lower() == "string":
            self.add_text_box(layout, cur_grid_row, name)
        else:
            print "unknown type! throwing up. bleccch."
            print "name:%s. value: %s" % (name, value)
            # throw exception here
            
    def add_text_box(self, layout, cur_grid_row, name):
        self.add_label(layout, cur_grid_row, self.param_d[name]["pretty.name"],\
                                tool_tip_text=self.param_d[name]["description"])
        # now add the text
        txt_input = QLineEdit()

        # if a default value has been specified, use it
        if self.current_defaults.has_key(name):
            txt_input.setText(str(self.current_defaults[name]))
            self.current_param_vals[name] = self.current_defaults[name]

        txt_input.setMaximumWidth(200)
        QObject.connect(txt_input, QtCore.SIGNAL("textChanged(QString)"),
                                 self.set_param_f(name, to_type=float))
        self.current_widgets.append(txt_input)
        layout.addWidget(txt_input, cur_grid_row, 1)

    def set_param_f(self, name, to_type=str):
        '''
        Returns a function f(x) such that f(x) will set the key
        name in the parameters dictionary to the value x.
        '''
        def set_param(x):
            self.current_param_vals[name] = to_type(x)
            print self.current_param_vals

        return set_param
    
    @QtCore.pyqtSlot()
    def set_param_f_from_itemdata(self, name, to_type=str):
        '''
        hackier version....
        Returns a function f(x) such that f(x) will set the key
        name in the parameters dictionary to the value x.
        '''
        
        def set_param(index):
            combo_box = self.sender()
            x = combo_box.itemData(index).toString()
            self.current_param_vals[name] = to_type(x)
            print str(self.current_param_vals) + " -> weirdo sender thing"

        return set_param
    
    def setup_fields_for_one_arm(self):
        self.show_4.setChecked(False)
        self.show_4.setEnabled(False)
    
    ############### Getters ###################################################
    
    # adapted from 'add_plot_params' in ma_specs in OMA, also returns params for the meta-analysis
    def get_plot_params(self):
        self.current_param_vals["fp_show_col1"] = self.show_1.isChecked()
        self.current_param_vals["fp_col1_str"]  = unicode(self.col1_str_edit.text().toUtf8(), "utf-8")
        self.current_param_vals["fp_show_col2"] = self.show_2.isChecked()
        self.current_param_vals["fp_col2_str"]  = unicode(self.col2_str_edit.text().toUtf8(), "utf-8")
        self.current_param_vals["fp_show_col3"] = self.show_3.isChecked()
        self.current_param_vals["fp_col3_str"]  = unicode(self.col3_str_edit.text().toUtf8(), "utf-8")
        self.current_param_vals["fp_show_col4"] = self.show_4.isChecked()
        self.current_param_vals["fp_col4_str"]  = unicode(self.col4_str_edit.text().toUtf8(), "utf-8")
        self.current_param_vals["fp_xlabel"]    = unicode(self.x_lbl_le.text().toUtf8(), "utf-8")
        self.current_param_vals["fp_outpath"]   = unicode(self.image_path.text().toUtf8(), "utf-8")
        
        plot_lb = unicode(self.plot_lb_le.text().toUtf8(), "utf-8")
        self.current_param_vals["fp_plot_lb"] = "[default]"
        if plot_lb != "[default]" and check_plot_bound(plot_lb):
            self.current_param_vals["fp_plot_lb"] = plot_lb
    
        plot_ub = unicode(self.plot_ub_le.text().toUtf8(), "utf-8")
        self.current_param_vals["fp_plot_ub"] = "[default]"
        if plot_ub != "[default]" and check_plot_bound(plot_ub):
            self.current_param_vals["fp_plot_ub"] = plot_ub
    
        xticks = unicode(self.x_ticks_le.text().toUtf8(), "utf-8")
        self.current_param_vals["fp_xticks"] = "[default]"
        if xticks != "[default]" and seems_sane(xticks):
            self.current_param_vals["fp_xticks"] = xticks
        
        self.current_param_vals["fp_show_summary_line"] = self.show_summary_line.isChecked()
        
        return self.current_param_vals
    
    def get_current_method(self):
        return self.current_method
    
    def get_current_method_pretty_name(self):
        return str(self.method_cbo_box.currentText())
    
    ###########################################################################
    
    def __str__(self):
        chosen_method_str = "Chosen Method: %s" % self.get_current_method_pretty_name()
        random_effects_method_str = None
        # stupid fix....
        if "fixed" not in self.get_current_method() and "rm.method" in self.current_param_vals:
            random_effects_method_str = "Random Effects Method: " + python_to_R.get_random_effects_methods_descriptions(self.get_current_method())[self.current_param_vals['rm.method']]
            summary = "\n".join([chosen_method_str, random_effects_method_str])
        else:
            summary = chosen_method_str
        return summary
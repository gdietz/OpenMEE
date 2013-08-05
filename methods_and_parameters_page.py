from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *

import python_to_R
import ui_methods_and_parameters_page

class MethodsAndParametersPage(QWizardPage, ui_methods_and_parameters_page.Ui_WizardPage):
    def __init__(self, model, meta_f_str=None, parent=None):
        super(MethodsAndParametersPage, self).__init__(parent)
        self.setupUi(self)
        
        self.model = model
        
    def initializePage(self):
        self.data_type = self.wizard().selected_data_type
        self.metric = self.wizard().selected_metric
        self.data_location = self.wizard().data_location
        self.studies_included_table = self.wizard().studies_included_table
        
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
    
    def get_included_studies_in_proper_order(self):
        all_studies = self.model.get_studies_in_current_order()
        included_studies = [study for study in all_studies if self.studies_included_table[study]==True]
        return included_studies
        

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
        
    def populate_cbo_box(self):
        # we first build an R object with the current data. this is to pass off         
        # to the R side to check the feasibility of the methods over the current data.
        # i.e., we do not display methods that cannot be performed over the 
        # current data.
        tmp_obj_name = "tmp_obj" 
        if OMA_CONVENTION[self.data_type] == "binary":
            python_to_R.dataset_to_simple_binary_robj(self.model,
                                                      studies = self.get_included_studies_in_proper_order(),
                                                      data_location = self.data_location,
                                                      var_name = tmp_obj_name,
                                                      covs_to_include=None, one_arm=False)
        elif OMA_CONVENTION[self.data_type] == "continuous":
            python_to_R.dataset_to_simple_continuous_robj(model=self.model,
                                                          included_studies=self.get_included_studies_in_proper_order(),
                                                          data_location=self.data_location, 
                                                          data_type=self.data_type, 
                                                          var_name=tmp_obj_name, 
                                                          covs_to_include=None, one_arm=False)
            
        self.available_method_d = python_to_R.get_available_methods(
                                                for_data_type=OMA_CONVENTION[self.data_type],
                                                data_obj_name=tmp_obj_name,
                                                metric=self.metric)
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
# TODO: save preferences like in OMA???
#        method_params = self.parent().user_prefs["method_params"]
#        if self.current_method in method_params:
#            print "loading default from user preferences!"
#            self.current_defaults = method_params[self.current_method]
            
#        # override conf.level with global conf.level
#        self.current_defaults['conf.level'] = self.conf_level

        print self.current_defaults
        

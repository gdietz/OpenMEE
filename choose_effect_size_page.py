
from functools import partial

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *

from globals import *
import ui_choose_effect_size_page



class ChooseEffectSizePage(QWizardPage, ui_choose_effect_size_page.Ui_choose_effect_size_page):
    def __init__(self, parent=None, add_generic_effect=False):
        super(ChooseEffectSizePage, self).__init__(parent)
        self.setupUi(self)
        
        self.add_generic_effect = add_generic_effect
        self.selected_data_type = None
        self.selected_metric = None
        
    def initializePage(self):
        self._populate_data_type_groupBox()
        
    def isComplete(self):
        if self.selected_data_type is None:
            return False
        if self.selected_metric is None:
            return False
        return True
        
    def _populate_data_type_groupBox(self):
        layout = self.data_type_groupBox.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.data_type_groupBox.setLayout(layout)
        
        # clear groupbox first
        self._unfill(layout)
        
        for data_type in DATA_TYPE_TO_METRICS.keys():            
            dt_btn = QRadioButton(DATA_TYPE_TEXT[data_type])
            layout.addWidget(dt_btn)
            # the btn ids will simply be the enumerated data type ids
            QObject.connect(dt_btn, SIGNAL("clicked(bool)"), partial(self._update_data_type_selection, data_type=data_type))

        self.wizard().adjustSize()
        
    def _update_data_type_selection(self, state, data_type):
        if state:
            self.selected_data_type = data_type
            self.wizard().selected_data_type = data_type
            self.selected_metric = self.wizard().selected_metric = None
            self.emit(SIGNAL("completeChanged()"))
            print("Selected data type is now %s" % DATA_TYPE_TEXT[self.wizard().selected_data_type])
            
        self._populate_effect_size_groupBox()
        self.wizard().adjustSize()
        
    def _populate_effect_size_groupBox(self):
        layout = self.effect_size_groupBox.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.effect_size_groupBox.setLayout(layout)
        
        # clear groupbox layout first
        self._unfill(layout)

        metrics = DATA_TYPE_TO_METRICS[self.selected_data_type]
        
        for effect_size in metrics:
            if not self.add_generic_effect:
                if effect_size == GENERIC_EFFECT:
                    continue
            
            btn = QRadioButton(METRIC_TEXT[effect_size])
            layout.addWidget(btn)
            # the buttons ids are simply the effect size ids
            QObject.connect(btn, SIGNAL("clicked(bool)"), partial(self._update_effect_size_selection, effect_size=effect_size))
    
    def _update_effect_size_selection(self, state, effect_size):
        if state:
            self.selected_metric = effect_size
            self.wizard().selected_metric = effect_size
            self.emit(SIGNAL("completeChanged()"))
            print("Selected metric is now %s" % METRIC_TEXT[self.wizard().selected_metric])
    
    #http://www.riverbankcomputing.com/pipermail/pyqt/2009-November/025214.html
    def _unfill(self, layout2delete):
        def deleteItems(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        deleteItems(item.layout())
        deleteItems(layout2delete)

# Delete a layout
#import sip
#sip.delete(widget.layout())
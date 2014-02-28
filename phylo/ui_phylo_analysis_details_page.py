# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'phylo_analysis_details_page.ui'
#
# Created: Fri Feb 28 13:41:36 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName(_fromUtf8("WizardPage"))
        WizardPage.resize(444, 286)
        self.verticalLayout_2 = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(WizardPage)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.effect_comboBox = QtGui.QComboBox(self.groupBox)
        self.effect_comboBox.setObjectName(_fromUtf8("effect_comboBox"))
        self.gridLayout.addWidget(self.effect_comboBox, 0, 1, 1, 1)
        self.variance_comboBox = QtGui.QComboBox(self.groupBox)
        self.variance_comboBox.setObjectName(_fromUtf8("variance_comboBox"))
        self.gridLayout.addWidget(self.variance_comboBox, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(38, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.species_comboBox = QtGui.QComboBox(self.groupBox)
        self.species_comboBox.setObjectName(_fromUtf8("species_comboBox"))
        self.horizontalLayout_2.addWidget(self.species_comboBox)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.line = QtGui.QFrame(WizardPage)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.groupBox_2 = QtGui.QGroupBox(WizardPage)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.random_effects_method_GroupBox = QtGui.QGroupBox(self.groupBox_2)
        self.random_effects_method_GroupBox.setObjectName(_fromUtf8("random_effects_method_GroupBox"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.random_effects_method_GroupBox)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.random_effects_method_ComboBox = QtGui.QComboBox(self.random_effects_method_GroupBox)
        self.random_effects_method_ComboBox.setObjectName(_fromUtf8("random_effects_method_ComboBox"))
        self.random_effects_method_ComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.random_effects_method_ComboBox)
        self.horizontalLayout_5.addWidget(self.random_effects_method_GroupBox)
        self.conf_level_groupBox = QtGui.QGroupBox(self.groupBox_2)
        self.conf_level_groupBox.setObjectName(_fromUtf8("conf_level_groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.conf_level_groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.conf_level_spinbox = QtGui.QDoubleSpinBox(self.conf_level_groupBox)
        self.conf_level_spinbox.setDecimals(1)
        self.conf_level_spinbox.setMinimum(70.0)
        self.conf_level_spinbox.setMaximum(99.9)
        self.conf_level_spinbox.setSingleStep(0.1)
        self.conf_level_spinbox.setProperty("value", 95.0)
        self.conf_level_spinbox.setObjectName(_fromUtf8("conf_level_spinbox"))
        self.horizontalLayout.addWidget(self.conf_level_spinbox)
        self.horizontalLayout_5.addWidget(self.conf_level_groupBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.include_species_checkBox = QtGui.QCheckBox(self.groupBox_2)
        self.include_species_checkBox.setChecked(True)
        self.include_species_checkBox.setObjectName(_fromUtf8("include_species_checkBox"))
        self.verticalLayout.addWidget(self.include_species_checkBox)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        spacerItem2 = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.groupBox.setTitle(_translate("WizardPage", "Data Location", None))
        self.label.setText(_translate("WizardPage", "Effect Size", None))
        self.label_2.setText(_translate("WizardPage", "Variance", None))
        self.label_3.setText(_translate("WizardPage", "Species", None))
        self.groupBox_2.setTitle(_translate("WizardPage", "Analysis Details", None))
        self.random_effects_method_GroupBox.setTitle(_translate("WizardPage", "Random Effects Method", None))
        self.random_effects_method_ComboBox.setItemText(0, _translate("WizardPage", "clear and then populate me", None))
        self.conf_level_groupBox.setTitle(_translate("WizardPage", "Confidence Level", None))
        self.conf_level_spinbox.setSuffix(_translate("WizardPage", " %", None))
        self.include_species_checkBox.setText(_translate("WizardPage", "Include species as random factor?", None))


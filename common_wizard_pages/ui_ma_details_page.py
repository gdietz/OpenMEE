# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ma_details_page.ui'
#
# Created: Sun Aug 31 18:44:10 2014
#      by: PyQt4 UI code generator 4.10.4
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
        WizardPage.resize(339, 283)
        self.verticalLayout = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(WizardPage)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.rand_effects_radio_btn = QtGui.QRadioButton(self.groupBox)
        self.rand_effects_radio_btn.setChecked(True)
        self.rand_effects_radio_btn.setObjectName(_fromUtf8("rand_effects_radio_btn"))
        self.gridLayout.addWidget(self.rand_effects_radio_btn, 1, 0, 1, 1)
        self.rand_effects_method_cbo_box = QtGui.QComboBox(self.groupBox)
        self.rand_effects_method_cbo_box.setObjectName(_fromUtf8("rand_effects_method_cbo_box"))
        self.gridLayout.addWidget(self.rand_effects_method_cbo_box, 1, 1, 1, 1)
        self.fixed_effects_radio_btn = QtGui.QRadioButton(self.groupBox)
        self.fixed_effects_radio_btn.setObjectName(_fromUtf8("fixed_effects_radio_btn"))
        self.gridLayout.addWidget(self.fixed_effects_radio_btn, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.intercept_chkbox = QtGui.QCheckBox(WizardPage)
        self.intercept_chkbox.setChecked(True)
        self.intercept_chkbox.setObjectName(_fromUtf8("intercept_chkbox"))
        self.verticalLayout.addWidget(self.intercept_chkbox)
        self.weighted_chkbox = QtGui.QCheckBox(WizardPage)
        self.weighted_chkbox.setChecked(True)
        self.weighted_chkbox.setObjectName(_fromUtf8("weighted_chkbox"))
        self.verticalLayout.addWidget(self.weighted_chkbox)
        self.knha_chkbox = QtGui.QCheckBox(WizardPage)
        self.knha_chkbox.setObjectName(_fromUtf8("knha_chkbox"))
        self.verticalLayout.addWidget(self.knha_chkbox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(WizardPage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.level_spinbox = QtGui.QDoubleSpinBox(WizardPage)
        self.level_spinbox.setDecimals(1)
        self.level_spinbox.setProperty("value", 95.0)
        self.level_spinbox.setObjectName(_fromUtf8("level_spinbox"))
        self.horizontalLayout.addWidget(self.level_spinbox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(WizardPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.digits_spinBox = QtGui.QSpinBox(WizardPage)
        self.digits_spinBox.setMaximum(10)
        self.digits_spinBox.setProperty("value", 4)
        self.digits_spinBox.setObjectName(_fromUtf8("digits_spinBox"))
        self.horizontalLayout_2.addWidget(self.digits_spinBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(WizardPage)
        QtCore.QObject.connect(self.rand_effects_radio_btn, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label.setVisible)
        QtCore.QObject.connect(self.rand_effects_radio_btn, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.rand_effects_method_cbo_box.setVisible)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.groupBox.setTitle(_translate("WizardPage", "Model Type", None))
        self.label.setText(_translate("WizardPage", "Random Effects Method:", None))
        self.rand_effects_radio_btn.setText(_translate("WizardPage", "Random Effects", None))
        self.fixed_effects_radio_btn.setText(_translate("WizardPage", "Fixed Effects", None))
        self.intercept_chkbox.setToolTip(_translate("WizardPage", "Add intercept term to the model? (default: yes)", None))
        self.intercept_chkbox.setText(_translate("WizardPage", "Add intercept to the model? (default: yes)", None))
        self.weighted_chkbox.setToolTip(_translate("WizardPage", "Use weighted (default) or unweighted least-squares when fitting the model.", None))
        self.weighted_chkbox.setText(_translate("WizardPage", "Weighted least squares? (default: yes)", None))
        self.knha_chkbox.setToolTip(_translate("WizardPage", "Adjust test statistics and conidence intervals using the method of Knapp and Hartung (default: no)", None))
        self.knha_chkbox.setText(_translate("WizardPage", "Knapp and Hartung? (default: no)", None))
        self.label_2.setText(_translate("WizardPage", "Confidence Level:", None))
        self.level_spinbox.setSuffix(_translate("WizardPage", "%", None))
        self.label_3.setToolTip(_translate("WizardPage", "# of decimal places to which to round the printed results", None))
        self.label_3.setText(_translate("WizardPage", "Digits:", None))
        self.digits_spinBox.setToolTip(_translate("WizardPage", "# of decimal places to which to round the printed results", None))


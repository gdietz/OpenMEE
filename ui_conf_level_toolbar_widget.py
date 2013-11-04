# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conf_level_toolbar_widget.ui'
#
# Created: Fri Nov  1 14:10:10 2013
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(95, 42)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.conf_level_spinbox = QtGui.QDoubleSpinBox(Form)
        self.conf_level_spinbox.setDecimals(1)
        self.conf_level_spinbox.setMinimum(50.0)
        self.conf_level_spinbox.setMaximum(99.9)
        self.conf_level_spinbox.setSingleStep(0.1)
        self.conf_level_spinbox.setProperty("value", 95.0)
        self.conf_level_spinbox.setObjectName(_fromUtf8("conf_level_spinbox"))
        self.verticalLayout.addWidget(self.conf_level_spinbox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Conf. Level", None))
        self.conf_level_spinbox.setSuffix(_translate("Form", "%", None))


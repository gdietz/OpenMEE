# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'overwrite_effect_sizes.ui'
#
# Created: Tue Oct 22 12:52:30 2013
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

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName(_fromUtf8("WizardPage"))
        WizardPage.resize(287, 172)
        self.verticalLayout_3 = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.no_btn = QtGui.QRadioButton(WizardPage)
        self.no_btn.setChecked(True)
        self.no_btn.setObjectName(_fromUtf8("no_btn"))
        self.buttonGroup = QtGui.QButtonGroup(WizardPage)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.no_btn)
        self.verticalLayout.addWidget(self.no_btn)
        self.yes_btn = QtGui.QRadioButton(WizardPage)
        self.yes_btn.setObjectName(_fromUtf8("yes_btn"))
        self.buttonGroup.addButton(self.yes_btn)
        self.verticalLayout.addWidget(self.yes_btn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.same_col_grp_lbl = QtGui.QLabel(WizardPage)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.same_col_grp_lbl.setFont(font)
        self.same_col_grp_lbl.setObjectName(_fromUtf8("same_col_grp_lbl"))
        self.horizontalLayout.addWidget(self.same_col_grp_lbl)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.frame = QtGui.QFrame(WizardPage)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.effect_cbo_box = QtGui.QComboBox(self.frame)
        self.effect_cbo_box.setObjectName(_fromUtf8("effect_cbo_box"))
        self.gridLayout.addWidget(self.effect_cbo_box, 1, 0, 1, 1)
        self.var_cbo_box = QtGui.QComboBox(self.frame)
        self.var_cbo_box.setObjectName(_fromUtf8("var_cbo_box"))
        self.gridLayout.addWidget(self.var_cbo_box, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_3.addWidget(self.frame)
        spacerItem1 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)

        self.retranslateUi(WizardPage)
        QtCore.QObject.connect(self.yes_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.frame.show)
        QtCore.QObject.connect(self.no_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.frame.hide)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        WizardPage.setTitle(_translate("WizardPage", "Overwrite Existing Effects?", None))
        self.no_btn.setText(_translate("WizardPage", "No", None))
        self.yes_btn.setText(_translate("WizardPage", "Yes", None))
        self.same_col_grp_lbl.setText(_translate("WizardPage", "selected columns must belong\n"
"to the same column group", None))
        self.label.setText(_translate("WizardPage", "Effect Size", None))
        self.label_2.setText(_translate("WizardPage", "Variance", None))


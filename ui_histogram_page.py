# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'histogram_page.ui'
#
# Created: Thu Jan  2 10:45:44 2014
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
        WizardPage.resize(405, 389)
        self.verticalLayout_3 = QtGui.QVBoxLayout(WizardPage)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.xlab_layout = QtGui.QHBoxLayout()
        self.xlab_layout.setObjectName(_fromUtf8("xlab_layout"))
        self.xlabCheckBox = QtGui.QCheckBox(WizardPage)
        self.xlabCheckBox.setObjectName(_fromUtf8("xlabCheckBox"))
        self.xlab_layout.addWidget(self.xlabCheckBox)
        self.label_3 = QtGui.QLabel(WizardPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.xlab_layout.addWidget(self.label_3)
        self.xlab_le = QtGui.QLineEdit(WizardPage)
        self.xlab_le.setEnabled(False)
        self.xlab_le.setText(_fromUtf8(""))
        self.xlab_le.setObjectName(_fromUtf8("xlab_le"))
        self.xlab_layout.addWidget(self.xlab_le)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.xlab_layout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.xlab_layout)
        self.ylab_layout = QtGui.QHBoxLayout()
        self.ylab_layout.setObjectName(_fromUtf8("ylab_layout"))
        self.ylabCheckBox = QtGui.QCheckBox(WizardPage)
        self.ylabCheckBox.setObjectName(_fromUtf8("ylabCheckBox"))
        self.ylab_layout.addWidget(self.ylabCheckBox)
        self.label_2 = QtGui.QLabel(WizardPage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.ylab_layout.addWidget(self.label_2)
        self.ylab_le = QtGui.QLineEdit(WizardPage)
        self.ylab_le.setEnabled(False)
        self.ylab_le.setText(_fromUtf8(""))
        self.ylab_le.setObjectName(_fromUtf8("ylab_le"))
        self.ylab_layout.addWidget(self.ylab_le)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ylab_layout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.ylab_layout)
        self.xlim_layout = QtGui.QHBoxLayout()
        self.xlim_layout.setObjectName(_fromUtf8("xlim_layout"))
        self.xlimCheckBox = QtGui.QCheckBox(WizardPage)
        self.xlimCheckBox.setObjectName(_fromUtf8("xlimCheckBox"))
        self.xlim_layout.addWidget(self.xlimCheckBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_7 = QtGui.QLabel(WizardPage)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout.addWidget(self.label_7)
        self.xlimLowSpinBox = QtGui.QDoubleSpinBox(WizardPage)
        self.xlimLowSpinBox.setEnabled(False)
        self.xlimLowSpinBox.setMinimum(-10000.0)
        self.xlimLowSpinBox.setMaximum(10000.0)
        self.xlimLowSpinBox.setSingleStep(0.1)
        self.xlimLowSpinBox.setObjectName(_fromUtf8("xlimLowSpinBox"))
        self.horizontalLayout.addWidget(self.xlimLowSpinBox)
        self.label_11 = QtGui.QLabel(WizardPage)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout.addWidget(self.label_11)
        self.xlimHighSpinBox = QtGui.QDoubleSpinBox(WizardPage)
        self.xlimHighSpinBox.setEnabled(False)
        self.xlimHighSpinBox.setMinimum(-10000.0)
        self.xlimHighSpinBox.setMaximum(10000.0)
        self.xlimHighSpinBox.setSingleStep(0.1)
        self.xlimHighSpinBox.setObjectName(_fromUtf8("xlimHighSpinBox"))
        self.horizontalLayout.addWidget(self.xlimHighSpinBox)
        self.label_9 = QtGui.QLabel(WizardPage)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout.addWidget(self.label_9)
        self.xlim_layout.addLayout(self.horizontalLayout)
        spacerItem2 = QtGui.QSpacerItem(38, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.xlim_layout.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.xlim_layout)
        self.ylim_layout_2 = QtGui.QHBoxLayout()
        self.ylim_layout_2.setObjectName(_fromUtf8("ylim_layout_2"))
        self.ylimCheckBox = QtGui.QCheckBox(WizardPage)
        self.ylimCheckBox.setObjectName(_fromUtf8("ylimCheckBox"))
        self.ylim_layout_2.addWidget(self.ylimCheckBox)
        self.ylim_layout = QtGui.QHBoxLayout()
        self.ylim_layout.setObjectName(_fromUtf8("ylim_layout"))
        self.label_8 = QtGui.QLabel(WizardPage)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.ylim_layout.addWidget(self.label_8)
        self.ylimLowSpinBox = QtGui.QDoubleSpinBox(WizardPage)
        self.ylimLowSpinBox.setEnabled(False)
        self.ylimLowSpinBox.setMinimum(-10000.0)
        self.ylimLowSpinBox.setMaximum(10000.0)
        self.ylimLowSpinBox.setSingleStep(0.1)
        self.ylimLowSpinBox.setObjectName(_fromUtf8("ylimLowSpinBox"))
        self.ylim_layout.addWidget(self.ylimLowSpinBox)
        self.label_12 = QtGui.QLabel(WizardPage)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.ylim_layout.addWidget(self.label_12)
        self.ylimHighSpinBox = QtGui.QDoubleSpinBox(WizardPage)
        self.ylimHighSpinBox.setEnabled(False)
        self.ylimHighSpinBox.setMinimum(-10000.0)
        self.ylimHighSpinBox.setMaximum(10000.0)
        self.ylimHighSpinBox.setSingleStep(0.1)
        self.ylimHighSpinBox.setObjectName(_fromUtf8("ylimHighSpinBox"))
        self.ylim_layout.addWidget(self.ylimHighSpinBox)
        self.label_10 = QtGui.QLabel(WizardPage)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.ylim_layout.addWidget(self.label_10)
        self.ylim_layout_2.addLayout(self.ylim_layout)
        spacerItem3 = QtGui.QSpacerItem(38, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ylim_layout_2.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.ylim_layout_2)
        self.binwidth_layout = QtGui.QHBoxLayout()
        self.binwidth_layout.setObjectName(_fromUtf8("binwidth_layout"))
        self.binwidth_checkBox = QtGui.QCheckBox(WizardPage)
        self.binwidth_checkBox.setObjectName(_fromUtf8("binwidth_checkBox"))
        self.binwidth_layout.addWidget(self.binwidth_checkBox)
        self.binwidth_spinBox = QtGui.QDoubleSpinBox(WizardPage)
        self.binwidth_spinBox.setEnabled(False)
        self.binwidth_spinBox.setMaximum(100.0)
        self.binwidth_spinBox.setSingleStep(0.1)
        self.binwidth_spinBox.setProperty("value", 1.0)
        self.binwidth_spinBox.setObjectName(_fromUtf8("binwidth_spinBox"))
        self.binwidth_layout.addWidget(self.binwidth_spinBox)
        self.label = QtGui.QLabel(WizardPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.binwidth_layout.addWidget(self.label)
        self.verticalLayout_3.addLayout(self.binwidth_layout)
        self.groupBox = QtGui.QGroupBox(WizardPage)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.no_gradient_radiobtn = QtGui.QRadioButton(self.groupBox)
        self.no_gradient_radiobtn.setChecked(True)
        self.no_gradient_radiobtn.setObjectName(_fromUtf8("no_gradient_radiobtn"))
        self.verticalLayout_2.addWidget(self.no_gradient_radiobtn)
        self.gradient_radiobtn = QtGui.QRadioButton(self.groupBox)
        self.gradient_radiobtn.setChecked(False)
        self.gradient_radiobtn.setObjectName(_fromUtf8("gradient_radiobtn"))
        self.verticalLayout_2.addWidget(self.gradient_radiobtn)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.fixed_color_layout = QtGui.QHBoxLayout()
        self.fixed_color_layout.setObjectName(_fromUtf8("fixed_color_layout"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.fixed_color_layout.addWidget(self.label_6)
        self.fill_color_btn = QtGui.QPushButton(self.groupBox)
        self.fill_color_btn.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);"))
        self.fill_color_btn.setObjectName(_fromUtf8("fill_color_btn"))
        self.fixed_color_layout.addWidget(self.fill_color_btn)
        self.outline_color_btn = QtGui.QPushButton(self.groupBox)
        self.outline_color_btn.setStyleSheet(_fromUtf8("color: rgb(200, 200, 200);\n"
"background-color: rgb(0, 0, 0);"))
        self.outline_color_btn.setObjectName(_fromUtf8("outline_color_btn"))
        self.fixed_color_layout.addWidget(self.outline_color_btn)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.fixed_color_layout.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.fixed_color_layout)
        self.gradient_layout = QtGui.QVBoxLayout()
        self.gradient_layout.setObjectName(_fromUtf8("gradient_layout"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_13 = QtGui.QLabel(self.groupBox)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_6.addWidget(self.label_13)
        self.low_color_change_btn = QtGui.QPushButton(self.groupBox)
        self.low_color_change_btn.setStyleSheet(_fromUtf8("background-color: rgb(255, 0, 0);color: rgb(255, 255, 255);"))
        self.low_color_change_btn.setObjectName(_fromUtf8("low_color_change_btn"))
        self.horizontalLayout_6.addWidget(self.low_color_change_btn)
        self.high_color_change_btn = QtGui.QPushButton(self.groupBox)
        self.high_color_change_btn.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);color: rgb(255, 255, 255);"))
        self.high_color_change_btn.setObjectName(_fromUtf8("high_color_change_btn"))
        self.horizontalLayout_6.addWidget(self.high_color_change_btn)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.gradient_layout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_14 = QtGui.QLabel(self.groupBox)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_10.addWidget(self.label_14)
        self.count_le = QtGui.QLineEdit(self.groupBox)
        self.count_le.setObjectName(_fromUtf8("count_le"))
        self.horizontalLayout_10.addWidget(self.count_le)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.gradient_layout.addLayout(self.horizontalLayout_10)
        self.verticalLayout.addLayout(self.gradient_layout)
        spacerItem8 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.label_3.setBuddy(self.xlab_le)
        self.label_2.setBuddy(self.ylab_le)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):
        WizardPage.setWindowTitle(_translate("WizardPage", "WizardPage", None))
        self.xlabCheckBox.setText(_translate("WizardPage", "set xlabel?", None))
        self.label_3.setText(_translate("WizardPage", "xlabel:", None))
        self.ylabCheckBox.setText(_translate("WizardPage", "set ylabel?", None))
        self.label_2.setText(_translate("WizardPage", "ylabel:", None))
        self.xlimCheckBox.setToolTip(_translate("WizardPage", "x axis limits. If not checked, the function tries to set the xaxis limits to some sensible values.", None))
        self.xlimCheckBox.setText(_translate("WizardPage", "set xlims?", None))
        self.label_7.setText(_translate("WizardPage", "[", None))
        self.label_11.setText(_translate("WizardPage", ",", None))
        self.label_9.setText(_translate("WizardPage", "]", None))
        self.ylimCheckBox.setToolTip(_translate("WizardPage", "y axis limits. If not checked, the function tries to set the yaxis limits to some sensible values.", None))
        self.ylimCheckBox.setText(_translate("WizardPage", "set ylims?", None))
        self.label_8.setText(_translate("WizardPage", "[", None))
        self.label_12.setText(_translate("WizardPage", ",", None))
        self.label_10.setText(_translate("WizardPage", "]", None))
        self.binwidth_checkBox.setText(_translate("WizardPage", "set bin width?", None))
        self.label.setText(_translate("WizardPage", "(defaults to range/30 if not checked)", None))
        self.groupBox.setTitle(_translate("WizardPage", "Histogram Bar Colors", None))
        self.no_gradient_radiobtn.setText(_translate("WizardPage", "No Gradient", None))
        self.gradient_radiobtn.setText(_translate("WizardPage", "gradient", None))
        self.label_6.setText(_translate("WizardPage", "Fixed Color:", None))
        self.fill_color_btn.setText(_translate("WizardPage", "change\n"
"fill color", None))
        self.outline_color_btn.setText(_translate("WizardPage", "change\n"
"outline color", None))
        self.label_13.setText(_translate("WizardPage", "Gradient:", None))
        self.low_color_change_btn.setText(_translate("WizardPage", "change\n"
"low color", None))
        self.high_color_change_btn.setText(_translate("WizardPage", "change\n"
"high color", None))
        self.label_14.setText(_translate("WizardPage", "Count legend title:", None))
        self.count_le.setText(_translate("WizardPage", "Count", None))


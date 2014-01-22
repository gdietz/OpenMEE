# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bootstrap_page.ui'
#
# Created: Wed Oct 16 14:56:05 2013
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

class Ui_BootstrapPage(object):
    def setupUi(self, BootstrapPage):
        BootstrapPage.setObjectName(_fromUtf8("BootstrapPage"))
        BootstrapPage.resize(371, 293)
        self.verticalLayout_2 = QtGui.QVBoxLayout(BootstrapPage)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(BootstrapPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.replicates_spinBox = QtGui.QSpinBox(BootstrapPage)
        self.replicates_spinBox.setMinimum(10)
        self.replicates_spinBox.setMaximum(100000)
        self.replicates_spinBox.setProperty("value", 1000)
        self.replicates_spinBox.setObjectName(_fromUtf8("replicates_spinBox"))
        self.horizontalLayout.addWidget(self.replicates_spinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(BootstrapPage)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.plot_path_le = QtGui.QLineEdit(BootstrapPage)
        self.plot_path_le.setObjectName(_fromUtf8("plot_path_le"))
        self.horizontalLayout_2.addWidget(self.plot_path_le)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(BootstrapPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.plot_title_le = QtGui.QLineEdit(BootstrapPage)
        self.plot_title_le.setObjectName(_fromUtf8("plot_title_le"))
        self.horizontalLayout_3.addWidget(self.plot_title_le)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(BootstrapPage)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.xlab_le = QtGui.QLineEdit(BootstrapPage)
        self.xlab_le.setObjectName(_fromUtf8("xlab_le"))
        self.horizontalLayout_4.addWidget(self.xlab_le)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem = QtGui.QSpacerItem(20, 131, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(BootstrapPage)
        QtCore.QMetaObject.connectSlotsByName(BootstrapPage)

    def retranslateUi(self, BootstrapPage):
        BootstrapPage.setWindowTitle(_translate("BootstrapPage", "WizardPage", None))
        BootstrapPage.setTitle(_translate("BootstrapPage", "Bootstrap Parameters", None))
        BootstrapPage.setSubTitle(_translate("BootstrapPage", "Bootstrap parameters", None))
        self.label.setText(_translate("BootstrapPage", "# bootstrap replicates:", None))
        self.label_2.setText(_translate("BootstrapPage", "Plot Path:", None))
        self.plot_path_le.setText(_translate("BootstrapPage", "./r_tmp/bootstrap.png", None))
        self.label_3.setText(_translate("BootstrapPage", "Plot Title:", None))
        self.plot_title_le.setText(_translate("BootstrapPage", "Bootstrap Histogram", None))
        self.label_4.setText(_translate("BootstrapPage", "horizontal label:", None))
        self.xlab_le.setText(_translate("BootstrapPage", "Effect Size", None))


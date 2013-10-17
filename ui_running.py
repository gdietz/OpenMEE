# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'running.ui'
#
# Created: Thu Oct 17 10:51:01 2013
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

class Ui_running(object):
    def setupUi(self, running):
        running.setObjectName(_fromUtf8("running"))
        running.setWindowModality(QtCore.Qt.ApplicationModal)
        running.resize(394, 64)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        running.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/meta.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        running.setWindowIcon(icon)
        running.setSizeGripEnabled(False)
        running.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(running)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(running)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.progress_bar = QtGui.QProgressBar(running)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setProperty("value", -1)
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_bar.setObjectName(_fromUtf8("progress_bar"))
        self.verticalLayout.addWidget(self.progress_bar)

        self.retranslateUi(running)
        QtCore.QMetaObject.connectSlotsByName(running)

    def retranslateUi(self, running):
        running.setWindowTitle(_translate("running", "running analysis...", None))
        self.label.setText(_translate("running", "Reticulating splines....", None))

import icons_rc

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Fri Dec 13 10:23:30 2013
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(490, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(490, 300))
        Dialog.setMaximumSize(QtCore.QSize(490, 300))
        Dialog.setBaseSize(QtCore.QSize(490, 300))
        Dialog.setSizeGripEnabled(False)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/general/images/logo.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.contents = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contents.sizePolicy().hasHeightForWidth())
        self.contents.setSizePolicy(sizePolicy)
        self.contents.setWordWrap(True)
        self.contents.setObjectName(_fromUtf8("contents"))
        self.verticalLayout_2.addWidget(self.contents)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.ok_btn = QtGui.QPushButton(Dialog)
        self.ok_btn.setObjectName(_fromUtf8("ok_btn"))
        self.horizontalLayout_2.addWidget(self.ok_btn)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.ok_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "About", None))
        self.contents.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">About OpenMEE</span></p><p><a href=\"http://www.cebm.brown.edu/open_mee\"><span style=\" text-decoration: underline; color:#0000ff;\">OpenMEE</span></a> is a cross-platform tool for performing Meta-Analysis suited to the needs of ecologists and evolutionary biologists.</p><p>OpenMEE was developed at the Brown University <a href=\"http://www.cebm.brown.edu/\"><span style=\" text-decoration: underline; color:#0000ff;\">Center for Evidence-Based Medicine</span></a> by George Dietz and Byron Wallace.</p><p>OpenMEE is based on the earlier meta-analysis program <a href=\"http://www.cebm.brown.edu/open_meta\"><span style=\" text-decoration: underline; color:#0000ff;\">OpenMetaAnalyst</span></a> developed by Byron Wallace, George Dietz, Paul Trow, and Issa Dahabreh also at the Brown CEBM.</p><p>OpenMEE heavily leverages and can largely be considered as a GUI to the <a href=\"http://www.metafor-project.org/\"><span style=\" text-decoration: underline; color:#0000ff;\">metafor</span></a> R package by Wolfgang Viechtbauer.</p></body></html>", None))
        self.ok_btn.setText(_translate("Dialog", "OK", None))

import icons_rc

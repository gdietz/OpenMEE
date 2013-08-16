# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'csv_export_options_dlg.ui'
#
# Created: Fri Aug 16 12:10:35 2013
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(275, 230)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.excel_dialect_chkbox = QtGui.QCheckBox(Dialog)
        self.excel_dialect_chkbox.setObjectName(_fromUtf8("excel_dialect_chkbox"))
        self.verticalLayout.addWidget(self.excel_dialect_chkbox)
        self.quote_text_cells_chkbox = QtGui.QCheckBox(Dialog)
        self.quote_text_cells_chkbox.setChecked(True)
        self.quote_text_cells_chkbox.setObjectName(_fromUtf8("quote_text_cells_chkbox"))
        self.verticalLayout.addWidget(self.quote_text_cells_chkbox)
        self.include_headers_chkbox = QtGui.QCheckBox(Dialog)
        self.include_headers_chkbox.setChecked(True)
        self.include_headers_chkbox.setObjectName(_fromUtf8("include_headers_chkbox"))
        self.verticalLayout.addWidget(self.include_headers_chkbox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.delimter_lbl = QtGui.QLabel(Dialog)
        self.delimter_lbl.setObjectName(_fromUtf8("delimter_lbl"))
        self.horizontalLayout.addWidget(self.delimter_lbl)
        self.delimeter_le = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delimeter_le.sizePolicy().hasHeightForWidth())
        self.delimeter_le.setSizePolicy(sizePolicy)
        self.delimeter_le.setMaximumSize(QtCore.QSize(20, 16777215))
        self.delimeter_le.setObjectName(_fromUtf8("delimeter_le"))
        self.horizontalLayout.addWidget(self.delimeter_le)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.quotechar_lbl = QtGui.QLabel(Dialog)
        self.quotechar_lbl.setObjectName(_fromUtf8("quotechar_lbl"))
        self.horizontalLayout_2.addWidget(self.quotechar_lbl)
        self.quotechar_le = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quotechar_le.sizePolicy().hasHeightForWidth())
        self.quotechar_le.setSizePolicy(sizePolicy)
        self.quotechar_le.setMaximumSize(QtCore.QSize(20, 16777215))
        self.quotechar_le.setObjectName(_fromUtf8("quotechar_le"))
        self.horizontalLayout_2.addWidget(self.quotechar_le)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "CSV Export Tool", None))
        self.label.setText(_translate("Dialog", "Formatting options for CSV export", None))
        self.excel_dialect_chkbox.setText(_translate("Dialog", "excel CSV dialect?", None))
        self.quote_text_cells_chkbox.setText(_translate("Dialog", "Quote text cells?", None))
        self.include_headers_chkbox.setText(_translate("Dialog", "include column headers", None))
        self.delimter_lbl.setText(_translate("Dialog", "Delimiter: ", None))
        self.delimeter_le.setText(_translate("Dialog", ",", None))
        self.quotechar_lbl.setText(_translate("Dialog", "Quote character: ", None))
        self.quotechar_le.setText(_translate("Dialog", "\"", None))


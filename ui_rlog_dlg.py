# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rlog_dlg.ui'
#
# Created: Thu Mar  6 14:45:34 2014
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
        Dialog.resize(695, 462)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Dialog)
        self.plainTextEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setPlainText(_fromUtf8(""))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.command_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.command_lineEdit.setMinimumSize(QtCore.QSize(400, 0))
        self.command_lineEdit.setObjectName(_fromUtf8("command_lineEdit"))
        self.verticalLayout_2.addWidget(self.command_lineEdit)
        self.show_output_checkBox = QtGui.QCheckBox(self.groupBox)
        self.show_output_checkBox.setChecked(True)
        self.show_output_checkBox.setObjectName(_fromUtf8("show_output_checkBox"))
        self.verticalLayout_2.addWidget(self.show_output_checkBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.inject_command_pushButton = QtGui.QPushButton(self.groupBox)
        self.inject_command_pushButton.setObjectName(_fromUtf8("inject_command_pushButton"))
        self.horizontalLayout_3.addWidget(self.inject_command_pushButton)
        self.verticalLayout.addWidget(self.groupBox)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.save_file_PushButton = QtGui.QPushButton(Dialog)
        self.save_file_PushButton.setObjectName(_fromUtf8("save_file_PushButton"))
        self.horizontalLayout.addWidget(self.save_file_PushButton)
        self.record_pushButton = QtGui.QPushButton(Dialog)
        self.record_pushButton.setObjectName(_fromUtf8("record_pushButton"))
        self.horizontalLayout.addWidget(self.record_pushButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.file_path_Label = QtGui.QLabel(Dialog)
        self.file_path_Label.setObjectName(_fromUtf8("file_path_Label"))
        self.horizontalLayout_2.addWidget(self.file_path_Label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.command_lineEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.inject_command_pushButton.click)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "View R Terminal", None))
        self.groupBox.setTitle(_translate("Dialog", "Command Injection", None))
        self.show_output_checkBox.setText(_translate("Dialog", "Show output from injected commands", None))
        self.inject_command_pushButton.setText(_translate("Dialog", "inject command\n"
"into R session", None))
        self.save_file_PushButton.setText(_translate("Dialog", "Choose File...", None))
        self.record_pushButton.setText(_translate("Dialog", "Start Recording...", None))
        self.label.setText(_translate("Dialog", "Record to file:", None))
        self.file_path_Label.setText(_translate("Dialog", "File Path label", None))

import icons_rc

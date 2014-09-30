# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pathUi.ui'
#
# Created: Sun Aug 31 23:10:09 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_path_form(object):
    def setupUi(self, path_form):
        path_form.setObjectName("path_form")
        path_form.resize(682, 41)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(path_form.sizePolicy().hasHeightForWidth())
        path_form.setSizePolicy(sizePolicy)
        path_form.setMinimumSize(QtCore.QSize(0, 40))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(path_form)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(path_form)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.pathLE = QtGui.QLineEdit(path_form)
        self.pathLE.setObjectName("pathLE")
        self.horizontalLayout_2.addWidget(self.pathLE)
        self.pickPB = QtGui.QPushButton(path_form)
        self.pickPB.setObjectName("pickPB")
        self.horizontalLayout_2.addWidget(self.pickPB)

        self.retranslateUi(path_form)
        QtCore.QMetaObject.connectSlotsByName(path_form)

    def retranslateUi(self, path_form):
        path_form.setWindowTitle(QtGui.QApplication.translate("path_form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("path_form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pickPB.setText(QtGui.QApplication.translate("path_form", "...", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1188, 759)
        MainWindow.setStyleSheet("background-color: rgb(185, 217, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(430, 10, 291, 101))
        self.titleLabel.setAutoFillBackground(False)
        self.titleLabel.setScaledContents(False)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.textBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textBox.setGeometry(QtCore.QRect(20, 140, 1141, 461))
        self.textBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textBox.setReadOnly(True)
        self.textBox.setPlainText("")
        self.textBox.setCenterOnScroll(False)
        self.textBox.setObjectName("textBox")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(530, 630, 151, 61))
        self.startButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 16pt \"Nirmala UI\";")
        self.startButton.setObjectName("startButton")
        self.textBox.raise_()
        self.titleLabel.raise_()
        self.startButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1188, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.titleLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; font-weight:600;\">RIPv2</span></p></body></html>"))
        self.startButton.setText(_translate("MainWindow", "Start"))
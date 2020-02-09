# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addSheetDetails.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(618, 400)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lable_sheet1 = QtWidgets.QLabel(self.centralwidget)
        self.lable_sheet1.setGeometry(QtCore.QRect(480, 20, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lable_sheet1.setFont(font)
        self.lable_sheet1.setObjectName("lable_sheet1")
        self.lable_sheet2 = QtWidgets.QLabel(self.centralwidget)
        self.lable_sheet2.setGeometry(QtCore.QRect(480, 100, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lable_sheet2.setFont(font)
        self.lable_sheet2.setObjectName("lable_sheet2")
        self.file1SheetName = QtWidgets.QComboBox(self.centralwidget)
        self.file1SheetName.setGeometry(QtCore.QRect(500, 50, 113, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file1SheetName.setFont(font)
        self.file1SheetName.setObjectName("file1SheetName")
        self.file2SheetName = QtWidgets.QComboBox(self.centralwidget)
        self.file2SheetName.setGeometry(QtCore.QRect(500, 130, 113, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file2SheetName.setFont(font)
        self.file2SheetName.setObjectName("file2SheetName")
        self.statusView = QtWidgets.QTextBrowser(self.centralwidget)
        self.statusView.setEnabled(True)
        self.statusView.setGeometry(QtCore.QRect(20, 230, 431, 111))
        self.statusView.setReadOnly(True)
        self.statusView.setObjectName("statusView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 21))
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
        self.lable_sheet1.setText(_translate("MainWindow", "TextLabel"))
        self.lable_sheet2.setText(_translate("MainWindow", "TextLabel"))
        self.statusView.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><title>JS Bin</title><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:600;\">Sarbajit</span> </h3>\n"
"<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">123 </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">345 </li>\n"
"<li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">567 </li></ol></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

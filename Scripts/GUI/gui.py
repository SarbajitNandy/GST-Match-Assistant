import pandas as pd
import re
import time

from Scripts.GUI.backEnd import Purchase_Sales_Match

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread;

from Scripts.Exceptions import *;

class Ui_MainWindow(Purchase_Sales_Match, QThread):

    def __init__(self):
        Purchase_Sales_Match.__int__(self)
        QThread.__init__(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(620, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file1 = QtWidgets.QLabel(self.centralwidget)
        self.file1.setGeometry(QtCore.QRect(10, 20, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file1.setFont(font)
        self.file1.setTextFormat(QtCore.Qt.RichText)
        self.file1.setObjectName("file1")
        self.file2 = QtWidgets.QLabel(self.centralwidget)
        self.file2.setGeometry(QtCore.QRect(10, 90, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file2.setFont(font)
        self.file2.setTextFormat(QtCore.Qt.RichText)
        self.file2.setObjectName("file2")
        self.lineFile1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineFile1.setGeometry(QtCore.QRect(10, 50, 231, 21))
        self.lineFile1.setObjectName("lineFile1")
        self.lineFile2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineFile2.setGeometry(QtCore.QRect(10, 130, 231, 21))
        self.lineFile2.setObjectName("lineFile2")
        self.browseFile1 = QtWidgets.QPushButton(self.centralwidget)
        self.browseFile1.setGeometry(QtCore.QRect(250, 50, 75, 23))
        self.browseFile1.setObjectName("browseFile1")
        self.browseFile2 = QtWidgets.QPushButton(self.centralwidget)
        self.browseFile2.setGeometry(QtCore.QRect(250, 130, 75, 23))
        self.browseFile2.setObjectName("browseFile2")

        # header list details
        self.headerFile1 = QtWidgets.QLabel(self.centralwidget)
        self.headerFile1.setGeometry(QtCore.QRect(500, 20, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.headerFile1.setFont(font)
        self.headerFile1.setTextFormat(QtCore.Qt.RichText)
        self.headerFile1.setObjectName("headerFile1")
        self.headerFile2 = QtWidgets.QLabel(self.centralwidget)
        self.headerFile2.setGeometry(QtCore.QRect(500, 100, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.headerFile2.setFont(font)
        self.headerFile2.setTextFormat(QtCore.Qt.RichText)
        self.headerFile2.setObjectName("headerFile2")
        self.headerLineFile1 = QtWidgets.QLineEdit(self.centralwidget)
        self.headerLineFile1.setGeometry(QtCore.QRect(500, 50, 113, 20))
        self.headerLineFile1.setObjectName("headerLineFile1")
        self.headerLineFile2 = QtWidgets.QLineEdit(self.centralwidget)
        self.headerLineFile2.setGeometry(QtCore.QRect(500, 130, 113, 20))
        self.headerLineFile2.setObjectName("headerLineFile2")

        # start button
        self.startProcess = QtWidgets.QPushButton(self.centralwidget)
        self.startProcess.setGeometry(QtCore.QRect(490, 300, 91, 41))
        self.startProcess.setObjectName("startProcess")

        # File write button
        self.download = QtWidgets.QPushButton(self.centralwidget)
        self.download.setGeometry(QtCore.QRect(490, 350, 91, 41))
        self.download.setObjectName("download")
        self.download.setVisible(False)


        # sheet lables
        self.lable_sheet1 = QtWidgets.QLabel(self.centralwidget)
        self.lable_sheet1.setGeometry(QtCore.QRect(350, 20, 100, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lable_sheet1.setFont(font)
        self.lable_sheet1.setObjectName("lable_sheet1")
        self.lable_sheet2 = QtWidgets.QLabel(self.centralwidget)
        self.lable_sheet2.setGeometry(QtCore.QRect(350, 100, 100, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lable_sheet2.setFont(font)
        self.lable_sheet2.setObjectName("lable_sheet2")

        # combo box for sheet name
        self.file1SheetName = QtWidgets.QComboBox(self.centralwidget)
        self.file1SheetName.setGeometry(QtCore.QRect(350, 50, 120, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.file1SheetName.setFont(font)
        self.file1SheetName.setObjectName("file1SheetName")
        self.file2SheetName = QtWidgets.QComboBox(self.centralwidget)
        self.file2SheetName.setGeometry(QtCore.QRect(350, 130, 120, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.file2SheetName.setFont(font)
        self.file2SheetName.setObjectName("file2SheetName")

        # # Status view
        # self.statusView = QtWidgets.QTextBrowser(self.centralwidget)
        # self.statusView.setEnabled(True)
        # self.statusView.setGeometry(QtCore.QRect(20, 230, 431, 111))
        # self.statusView.setObjectName("statusView")
        # self.statusView.setReadOnly(True)

        # Progress bar
        font = QtGui.QFont()
        self.progressBar1 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar1.setEnabled(True)
        self.progressBar1.setGeometry(QtCore.QRect(20, 310, 411, 23))
        self.progressBar1.setMouseTracking(False)
        self.progressBar1.setAutoFillBackground(False)
        # self.progressBar1.setProperty("value", 0)
        self.progressBar1.setValue(0)
        self.progressBar1.setTextVisible(True)
        self.progressBar1.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar1.setInvertedAppearance(False)
        self.progressBar1.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar1.setObjectName("progressBar1")
        self.progressBar1.setMaximum(100)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 563, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.init_button()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.file1.setText(_translate("MainWindow", "Import file from Tally"))
        self.file2.setText(_translate("MainWindow", "Import file from GST Portal"))
        self.browseFile1.setText(_translate("MainWindow", "Browse"))
        self.browseFile2.setText(_translate("MainWindow", "Browse"))
        self.headerFile1.setText(_translate("MainWindow", "Header value(s)"))
        self.headerFile2.setText(_translate("MainWindow", "Header value(s)"))
        self.startProcess.setText(_translate("MainWindow", "Start"))
        self.download.setText(_translate("MainWindow", "Download"))
        self.lable_sheet1.setText(_translate("MainWindow", "Sheet Name"))
        self.lable_sheet2.setText(_translate("MainWindow", "Sheet Name"))

    def open_dialog_box(self):
        fileName = QFileDialog.getOpenFileName()
        return fileName[0]

    def click(self):
        print(self.compiledExp)

    def brwsFile1_handler(self):
        self.file1Path = self.open_dialog_box()
        self.lineFile1.setText(self.file1Path)
        self.myExcel = self.read_file1()

    def brwsFile2_handler(self):
        self.file2Path = self.open_dialog_box()
        self.lineFile2.setText(self.file2Path)
        self.givenExcel = self.read_file2()

    def run(self):
        print("run process")
        self.main()
        # self.download_work_handler()
        print("run finished")

    def startProcess_handler(self):

        def getPoint(n):
            return [ (i-1) for i in n ]

        # self.file1Path = self.lineFile1.text()
        # self.file2Path = self.lineFile2.text()
        self.outFilePath = '/'.join(self.file1Path.split("/")[0:-1]) +'/mergedFile.xlsx'
        header1 = self.headerLineFile1.text()
        header2 = self.headerLineFile2.text()
        # self.file1Sheet = self.sheetName1.text().strip()
        # self.file2Sheet = self.sheetName2.text().strip()
        self.file1Sheet = self.file1SheetName.currentText()
        self.file2Sheet = self.file2SheetName.currentText()
        try:
            self.file1Header = getPoint(list(map(int, header1.strip().split(','))))
            self.file2Header = getPoint(list(map(int, header2.strip().split(','))))
        except:
            # print("Problem with file Header. Enter value correctly")
            raise MsgException("Header format error")

        self.start()
        print("StartBtn Finished")

    def download_work_handler(self):
        print("download work handler started")
        while (not self.Done_with_match):
            continue
        self.download.setVisible(True)
        # self.download.setDisabled(False)
        print("download work handler finished")

    def download_work(self):
        self.write_Result_to_excel()

    def init_button(self):
        self.browseFile1.clicked.connect(self.brwsFile1_handler)
        self.browseFile2.clicked.connect(self.brwsFile2_handler)
        self.startProcess.clicked.connect(self.startProcess_handler)
        self.download.clicked.connect(self.download_work)

    def read_file1(self):
        self.file1SheetName.clear()
        try:
            # print("reading " + self.file1Path)
            file1 = pd.ExcelFile(self.file1Path)
            for i in file1.sheet_names:
                self.file1SheetName.addItem(i)
            # self.success_status("{} file is OK".format(self.file1Path))
            return file1
        except Exception as e:
            # self.failure_status(str(e))
            self.file1Path=None
            self.lineFile1.clear()
            self.file1SheetName.clear()
            return None

    def read_file2(self):
        self.file2SheetName.clear()

        try:
            # print("reading " + self.file2Path)
            file2 = pd.ExcelFile(self.file2Path)
            for i in file2.sheet_names:
                self.file2SheetName.addItem(i)
            # self.success_status("{} file is OK".format(self.file2Path))
            return file2
        except Exception as e:
            # self.failure_status(str(e))
            self.file2Path = None
            self.lineFile2.clear()
            self.file2SheetName.clear()
            return None



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
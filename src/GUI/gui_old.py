import pandas as pd
import re
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

class ExcelReadException(Exception):
    demo = "Can not read {} successfully"
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return ExcelReadException.demo.format(self.name)

class MsgException(Exception):
    def __init__(self, value:str="Unknown Exception"):
        self.value = value

    def __str__(self):
        return self.value

class Ui_MainWindow(QtWidgets.QMainWindow):
    compiledExp = re.compile('/[A-Z]?[0-9]+/')

    def __int__(self):
        # Details of file 1
        self.file1Path = None
        self.file1Header = None
        self.file1Sheet = None

        # details of file 2
        self.file2Path = None
        self.file2Header = None
        self.file2Sheet = None

        self.outFilePath = None

        self.myExcel : pd.ExcelFile = None
        self.givenExcel: pd.ExcelFile = None

        self.myVouchar: pd.DataFrame = None
        self.givenVouchar: pd.DataFrame = None
        self.mergedData: pd.DataFrame = None

        # #Status view html
        # self.statusViewHtml: str = None

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(620, 400)
        self.centralwidget = QtWidgets.QWidget(self)
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

        # Status view
        self.statusView = QtWidgets.QTextBrowser(self.centralwidget)
        self.statusView.setEnabled(True)
        self.statusView.setGeometry(QtCore.QRect(20, 230, 431, 111))
        self.statusView.setObjectName("statusView")
        self.statusView.setReadOnly(True)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 563, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.init_button()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.file1.setText(_translate("MainWindow", "Import file from Tally"))
        self.file2.setText(_translate("MainWindow", "Import file from GST Portal"))
        self.browseFile1.setText(_translate("MainWindow", "Browse"))
        self.browseFile2.setText(_translate("MainWindow", "Browse"))
        self.headerFile1.setText(_translate("MainWindow", "Header value(s)"))
        self.headerFile2.setText(_translate("MainWindow", "Header value(s)"))
        self.startProcess.setText(_translate("MainWindow", "Start"))
        self.lable_sheet1.setText(_translate("MainWindow", "Sheet Name"))
        self.lable_sheet2.setText(_translate("MainWindow", "Sheet Name"))


    @staticmethod
    def validation(n):
        return n and not (n == '')

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
            print("Problem with file Header. Enter value correctly")
            return

        print(self.file1Path)
        print(self.file2Path)
        print(self.outFilePath)
        print(self.file1Header)
        print(self.file2Header)
        print(self.file1Sheet)
        print(self.file2Sheet)

        # if self.validation(self.file2Sheet) and self.validation(self.file2Path) and self.validation(self.file2Sheet):
        #     self.main()
        # else:
        #     print("Try again")
        self.main()

    def init_button(self):
        self.browseFile1.clicked.connect(self.brwsFile1_handler)
        self.browseFile2.clicked.connect(self.brwsFile2_handler)
        self.startProcess.clicked.connect(self.startProcess_handler)

#     Fail-safe status
    def normal_status(self, n:str):
        html = """
           <span>{}</span>
        """
        self.statusView.append(html.format(n))

    def success_status(self, n:str):
        html = """
            <span style="color: green">{}</span>
        """
        self.statusView.append(html.format(n))

    def failure_status(self, n:str):
        html = """
            <span style="color: red">{0}</span>
        """
        self.statusView.append(html.format(n))

#     panda part
    @staticmethod
    def join(i):
        si = list(i)
        if len(si) >= 2:
            for j in range(len(si)):
                if ('Unnamed' in si[j]):
                    del si[j]

        return " ".join(si)

    @staticmethod
    def spl(i):
        i = str(i)
        try:
            val = Ui_MainWindow.compiledExp.search('/' + str(i) + '/').group()
            return re.search('\d+', val).group()
        except:
            if i != 'nan':
                try:
                    return re.search('\d+', i).group()
                except:
                    return i;
            return i

    @staticmethod
    def float_compare(a, b):
        a, b = round(float(a)), round(float(b))
        if a == b:
            return True
        else:
            if abs(a - b) <= 1:
                return True
            else:
                return False

    @staticmethod
    def match_work(data):
        count = 0
        matchresult = []
        for i, j in data.iterrows():
            r: bool = True
            gst1, gst2 = j['Taxable Value'], j['Taxable Value (₹)']
            igst1, igst2 = j['Integrated Tax Amount'], j['Tax Amount Integrated Tax  (₹)']
            cgst1, cgst2 = j['Central Tax Amount'], j['Tax Amount Central Tax (₹)']
            sgst1, sgst2 = j['State Tax Amount'], j['Tax Amount State/UT tax (₹)']

            if not Ui_MainWindow.float_compare(gst1, gst2):
                r = False
            if not Ui_MainWindow.float_compare(igst1, igst2):
                r = False
            if not Ui_MainWindow.float_compare(sgst1, sgst2):
                r = False
            if not Ui_MainWindow.float_compare(cgst1, cgst2):
                r = False
            if r:
                count += 1
                matchresult.append("MATCHED")
            else:
                matchresult.append("NOT MATCHED")

        data['Result'] = matchresult
        print("Found match in {0}/{1}".format(count, len(matchresult)))
        return

    def format_header(self):
        try:
            mv, gv = self.myVouchar.keys(), self.givenVouchar.keys()
            print(mv)
            print(gv)
            m = [self.join(i)
                 for i in mv]

            g = [self.join(i)
                 for i in gv]
            print(m)
            print(g)
            return (m, g)
        except:
            raise MsgException("Wrong Header format")

    def data_sanit(self, mycols, gvcols):
        mvNew, gvNew = self.myVouchar.keys(), self.givenVouchar.keys()
        for i in mvNew:
            if i not in mycols:
                del self.myVouchar[i]

        for i in gvNew:
            if i not in gvcols:
                del self.givenVouchar[i]
        return


    def format_invoice(self):
        self.myVouchar["Invoice"] = [self.spl(i) for i in self.myVouchar["Invoice No."]]
        self.givenVouchar["Invoice"] = [self.spl(i) for i in self.givenVouchar["Invoice details Invoice number"]]
        return


    def read_file1(self):
        self.file1SheetName.clear()
        print("reading " + self.file1Path)
        file1 = pd.ExcelFile(self.file1Path)
        for i in file1.sheet_names:
            self.file1SheetName.addItem(i)
        return file1


    def read_file2(self):
        self.file2SheetName.clear()
        print("reading " + self.file2Path)
        file2 = pd.ExcelFile(self.file2Path)
        for i in file2.sheet_names:
            self.file2SheetName.addItem(i)
        return file2


    def main(self):
        start = time.time()
        self.statusView.clear()
        try:
            mycols, gvcols = None, None
            if self.myExcel:
                self.normal_status("Reading {}".format(self.file1Path))
                mycols = ['Particulars', 'GSTIN/UIN', 'Invoice No.', 'Taxable Value', 'Integrated Tax Amount',
                          'Central Tax Amount', 'State Tax Amount', 'Total Tax Amount']
                self.myVouchar = pd.read_excel(self.myExcel, self.file1Sheet, header=self.file1Header)
                self.success_status("file read successful, format OK")
            else:
                # raise exception
                raise ExcelReadException(self.file1Path)


            if self.givenExcel:
                self.normal_status("Reading {}".format(self.file2Path))
                gvcols = ['GSTIN of supplier', 'Trade/Legal name of the Supplier','Invoice details Invoice number', 'Invoice details Invoice Value (₹)',
                          'Taxable Value (₹)', 'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)',
                          'Tax Amount State/UT tax (₹)']
                self.givenVouchar = pd.read_excel(self.givenExcel, self.file2Sheet, header=self.file2Header)
                self.success_status("file read successful, format OK")
            else:
                #raise exception
                raise ExcelReadException(self.file2Path)

            if self.myExcel and self.givenExcel:
                self.normal_status("formatting columns")
                self.myVouchar.columns, self.givenVouchar.columns = self.format_header()
                self.success_status("Done")

                # Sanitary check of data
                self.normal_status("Sanitizing Data")
                self.data_sanit(mycols, gvcols)
                self.success_status("Done")

                #  format invoice
                self.normal_status("formatting invoice")
                self.format_invoice()
                self.success_status("Done")

                #  check columns
                self.normal_status("checking columns")
                self.myVouchar.rename(columns={'GSTIN/UIN': 'GSTno.'}, inplace=True)
                self.givenVouchar.rename(columns={'GSTIN of supplier': 'GSTno.'}, inplace=True)
                self.success_status("Done")

                #  data join
                self.normal_status("merging two files")
                self.mergedData = pd.merge(self.myVouchar, self.givenVouchar, on=['GSTno.', 'Invoice'], how='outer').fillna(0)
                self.success_status("Done")

                # match
                self.normal_status("finding for match")
                self.match_work(self.mergedData)
                self.success_status("Done")

                # write into a file
                self.normal_status("Creating output file")
                self.mergedData.to_excel(self.outFilePath, sheet_name='Sheet1', engine='xlsxwriter')
                self.success_status("Done")
                self.success_status("output file path {} ".format(self.outFilePath))

        except Exception as e:
            self.failure_status(str(e))
            self.failure_status("Main Process failed")
        print("Process finished in : {0} secs".format(round(time.time() - start), 3))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # self = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi()
    ui.show()
    sys.exit(app.exec_())

"""
import pandas as pd
import re
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

class Ui_MainWindow(object):
    compiledExp = re.compile('/[A-Z]?[0-9]+/')

    def __int__(self):
        # Details of file 1
        self.file1Path = None
        self.file1Header = None
        self.file1Sheet = None

        # details of file 2
        self.file2Path = None
        self.file2Header = None
        self.file2Sheet = None

        self.outFilePath = None

        self.myExcel : pd.ExcelFile = None
        self.givenExcel: pd.ExcelFile = None

        self.myVouchar: pd.DataFrame = None
        self.givenVouchar: pd.DataFrame = None
        self.mergedData: pd.DataFrame = None


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
        self.startProcess.setGeometry(QtCore.QRect(460, 300, 91, 41))
        self.startProcess.setObjectName("startProcess")

        font = QtGui.QFont()
        self.progressBar1 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar1.setEnabled(True)
        self.progressBar1.setGeometry(QtCore.QRect(20, 310, 411, 23))
        self.progressBar1.setMouseTracking(False)
        self.progressBar1.setAutoFillBackground(False)
        self.progressBar1.setProperty("value", 0)
        self.progressBar1.setTextVisible(True)
        self.progressBar1.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar1.setInvertedAppearance(False)
        self.progressBar1.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar1.setObjectName("progressBar1")

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
        self.lable_sheet1.setText(_translate("MainWindow", "Sheet Name"))
        self.lable_sheet2.setText(_translate("MainWindow", "Sheet Name"))

    @staticmethod
    def validation(n):
        return n and not (n == '')

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
            print("Problem with file Header. Enter value correctly")
            return

        print(self.file1Path)
        print(self.file2Path)
        print(self.outFilePath)
        print(self.file1Header)
        print(self.file2Header)
        print(self.file1Sheet)
        print(self.file2Sheet)

        # if self.validation(self.file2Sheet) and self.validation(self.file2Path) and self.validation(self.file2Sheet):
        #     self.main()
        # else:
        #     print("Try again")
        self.main()

    def init_button(self):
        self.browseFile1.clicked.connect(self.brwsFile1_handler)
        self.browseFile2.clicked.connect(self.brwsFile2_handler)
        self.startProcess.clicked.connect(self.startProcess_handler)

#     panda part
    @staticmethod
    def join(i):
        si = list(i)
        if len(si) >= 2:
            for j in range(len(si)):
                if ('Unnamed' in si[j]):
                    del si[j]

        return " ".join(si)

    @staticmethod
    def spl(i):
        i = str(i)
        try:
            val = Ui_MainWindow.compiledExp.search('/' + str(i) + '/').group()
            return re.search('\d+', val).group()
        except:
            if i != 'nan':
                try:
                    return re.search('\d+', i).group()
                except:
                    return i;
            return i

    @staticmethod
    def float_compare(a, b):
        a, b = round(float(a)), round(float(b))
        if a == b:
            return True
        else:
            if abs(a - b) <= 1:
                return True
            else:
                return False

    @staticmethod
    def match_work(data):
        count = 0
        matchresult = []
        for i, j in data.iterrows():
            r: bool = True
            gst1, gst2 = j['Taxable Value'], j['Taxable Value (₹)']
            igst1, igst2 = j['Integrated Tax Amount'], j['Tax Amount Integrated Tax  (₹)']
            cgst1, cgst2 = j['Central Tax Amount'], j['Tax Amount Central Tax (₹)']
            sgst1, sgst2 = j['State Tax Amount'], j['Tax Amount State/UT tax (₹)']

            if not Ui_MainWindow.float_compare(gst1, gst2):
                r = False
            if not Ui_MainWindow.float_compare(igst1, igst2):
                r = False
            if not Ui_MainWindow.float_compare(sgst1, sgst2):
                r = False
            if not Ui_MainWindow.float_compare(cgst1, cgst2):
                r = False
            if r:
                count += 1
                matchresult.append("MATCHED")
            else:
                matchresult.append("NOT MATCHED")

        data['Result'] = matchresult
        print("Found match in {0}/{1}".format(count, len(matchresult)))
        return

    def format_header(self):
        mv, gv = self.myVouchar.keys(), self.givenVouchar.keys()
        print(mv)
        print(gv)
        m = [ self.join(i)
             for i in mv]

        g = [self.join(i)
             for i in gv]
        print(m)
        print(g)
        return (m,g)

    def data_sanit(self, mycols, gvcols):
        mvNew, gvNew = self.myVouchar.keys(), self.givenVouchar.keys()
        for i in mvNew:
            if i not in mycols:
                del self.myVouchar[i]

        for i in gvNew:
            if i not in gvcols:
                del self.givenVouchar[i]
        return

    def format_invoice(self):
        print(1)
        self.myVouchar["Invoice"] = [self.spl(i) for i in self.myVouchar["Invoice No."]]
        print(2)
        self.givenVouchar["Invoice"] = [self.spl(i) for i in self.givenVouchar["Invoice details Invoice number"]]
        return

    def read_file1(self):
        self.file1SheetName.clear()
        try:
            print("reading " + self.file1Path)
            file1 = pd.ExcelFile(self.file1Path)
            for i in file1.sheet_names:
                self.file1SheetName.addItem(i)
            return file1
        except:
            print("Can't read file " + self.file1Path)
            return

    def read_file2(self):
        self.file2SheetName.clear()
        try:
            print("reading " + self.file2Path)
            file2 = pd.ExcelFile(self.file2Path)
            for i in file2.sheet_names:
                self.file2SheetName.addItem(i)
            return file2
        except:
            print("Can't read file " + self.file2Path)
            return

    def main(self):
        start = time.time()

        mycols, gvcols = None, None
        if self.myExcel:
            mycols = ['Particulars', 'GSTIN/UIN', 'Invoice No.', 'Taxable Value', 'Integrated Tax Amount',
                      'Central Tax Amount', 'State Tax Amount', 'Total Tax Amount']
            try:
                self.myVouchar = pd.read_excel(self.myExcel, self.file1Sheet, header=self.file1Header)
            except:
                print("Can't open Excel file 1")
                return
        else:
            print("myExcel is empty")


        if self.givenExcel:
            gvcols = ['GSTIN of supplier', 'Trade/Legal name of the Supplier','Invoice details Invoice number', 'Invoice details Invoice Value (₹)',
                      'Taxable Value (₹)', 'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)',
                      'Tax Amount State/UT tax (₹)']
            try:
                self.givenVouchar = pd.read_excel(self.givenExcel, self.file2Sheet, header=self.file2Header)
            except:
                print("Can't open Excel file 2")
                return
        else:
            print("givenExcel is empty")

        if self.myExcel and self.givenExcel:
            print("formatting columns")
            self.myVouchar.columns, self.givenVouchar.columns = self.format_header()

            # Sanitary check of data
            print("Data sanit")
            self.data_sanit(mycols, gvcols)

            #  format invoice
            print("format invoice no")
            self.format_invoice()

            #  check columns
            print("checking column names")
            self.myVouchar.rename(columns={'GSTIN/UIN': 'GSTno.'}, inplace=True)
            self.givenVouchar.rename(columns={'GSTIN of supplier': 'GSTno.'}, inplace=True)

            #  data join
            print("merging two files")
            self.mergedData = pd.merge(self.myVouchar, self.givenVouchar, on=['GSTno.', 'Invoice'], how='outer').fillna(0)

            # match
            print("finding for match")
            self.match_work(self.mergedData)
            # write into a file
            print("output file path " + self.outFilePath )
            self.mergedData.to_excel(self.outFilePath, sheet_name='Sheet1', engine='xlsxwriter')
        else:
            print("Process failed")
        print("Process finished in : {0} secs".format(round(time.time() - start), 3))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

"""
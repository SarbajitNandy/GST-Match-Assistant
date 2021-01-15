import pandas as pd
import re
import time
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread;

import logging


class Purchase_Sales_Match(object):
    compiledExp = re.compile('/[A-Z]*[0-9]+[A-Z]*/')
    check = ["1920", '2020', '2019', '2021']

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

        self.myExcel: pd.ExcelFile = None
        self.givenExcel: pd.ExcelFile = None

        self.myVouchar: pd.DataFrame = None
        self.givenVouchar: pd.DataFrame = None
        self.mergedData: pd.DataFrame = None
        self.MatchedDetails : pd.DataFrame = pd.DataFrame()
        self.notMatched_myside: pd.DataFrame = None
        self.notMatched_otherside: pd.DataFrame = None

        # columns values
        self.mycols =  ['Particulars', 'GSTIN/UIN', 'Invoice No.' , 'Date', 'Taxable Value', 'Integrated Tax Amount',
                          'Central Tax Amount', 'State Tax Amount', 'Total Tax Amount']
        self.gvcols =['GSTIN of supplier', 'Trade/Legal name of the Supplier','Invoice details Invoice number','Invoice details Invoice Date', 'Invoice details Invoice Value (₹)',
                          'Taxable Value (₹)', 'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)',
                          'Tax Amount State/UT tax (₹)']
        # success signals
        self.Done_with_match: bool = False


    #     panda part
    @staticmethod
    def validation(n):
        return n and not (n == '')

    '''
    Objective : takes an list of string, remove all values with 'Unnamed' word, then join rest of the part 
    Example   : ['Vouchar','Unnamed','Number']  ---->  ['Vouchar Number'] 
    '''
    @staticmethod
    def join(i):
        si = list(i)
        if len(si) >= 2:
            for j in range(len(si)):
                if ('Unnamed' in si[j]):
                    del si[j]

        return " ".join(si)

    '''
    Not in use , to be documented later
    '''
    @staticmethod
    def makeInt(n):

        def sanit(x):
            inter = re.search("\d+", x[1:-1]).group()
            for i in Purchase_Sales_Match.check:
                if (i in inter):
                    return 0
            return int(inter)

        return list(map(sanit, n))

    '''
    Not in use , to be documented later
    '''
    @staticmethod
    def spl(i):
        i = str(i)
        if ("/" not in i):
            return i
        try:
            j = i.replace('/', "//")
            j = "/{}/".format(j)
            print(j)
            val = Purchase_Sales_Match.compiledExp.findall(j)
            if (len(val) == 0):
                raise ValueError
            ret = max(Purchase_Sales_Match.makeInt(val))
            return str(ret)
        except:
            if i!='nan':
                try:
                    val = re.findall('\d+', i)
                    return str(max(list(map(int, val))))
                except:
                    return i
            return i

    '''
    This method compares same columns of two sides of data
    for emample, 
    1. takes a rows from purchase side, and another row from sales side
    2. compares between their values on cgst column
    '''
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

    '''
    Objective : converts two row header into single row
    Example   : 1. sample data : [['Purchase','data'],['Voucher','No.']] ---> ['Purchase data', 'Vouchar No.'] 
    Dependency: Make use of join method which resolves the merging work
    '''
    def format_header(self):
        try:
            mv, gv = self.myVouchar.keys(), self.givenVouchar.keys()
            m = [self.join(i)
                 for i in mv]
            g = [self.join(i)
                 for i in gv]
            logging.info("Head format successful")
            return (m, g)
        except:
            logging.error("Wrong header format")
            raise MsgException("Wrong Header format")

    '''
    Objective : filtering out not-required columns from purchase and sales voucher sheet
    Dependency: make use of mycols and gvcols mentioned  in the constructor  
    '''
    def data_sanit(self):
        mvNew, gvNew = self.myVouchar.keys(), self.givenVouchar.keys()
        for i in mvNew:
            if i not in self.mycols:
                del self.myVouchar[i]

        for i in gvNew:
            if i not in self.gvcols:
                del self.givenVouchar[i]
        return

    '''
    Objective : self-explanetory function name
    '''
    @staticmethod
    def make_int_if_possible(invoice):
        try:
            return int(invoice)
        except:
            return str(invoice)

    '''
    Objective : Format all the Invoice values and store them into new columns 
    Output    : Prepare a match report 
    '''
    def format_invoice(self):
        matching_excel = {}

        # self.myVouchar["Invoice"] = [self.spl(i) for i in self.myVouchar["Invoice No."]]
        # self.givenVouchar["Invoice"] = [self.spl(i) for i in self.givenVouchar["Invoice details Invoice number"]]

        # self.myVouchar["Invoice"] = self.myVouchar["Invoice No."].copy()
        # self.givenVouchar["Invoice"] = self.givenVouchar["Invoice details Invoice number"].copy()

        '''
        Objective : These two methods converts all invoice number into integer if possible
        Example   : '1234' --> 1234 |  '12/21/2020' --> '12/21/2020' (can't be converted into Integer)
        '''
        self.myVouchar["Invoice"] = [ Purchase_Sales_Match.make_int_if_possible(item) for item in self.myVouchar["Invoice No."]]
        self.givenVouchar["Invoice"] = [ Purchase_Sales_Match.make_int_if_possible(item) for item in self.givenVouchar["Invoice details Invoice number"]]

        logging.info("Purchase side and Sales side invoice numbers have been formatted")

        # for item in self.myVouchar['Invoice']:
        #     print(item.__str__())
        #
        # for item in self.givenVouchar['Invoice']:
        #     print(item.__str__())

        '''
        Objective : Shows both values for 'before sanitization' and 'after sanitization' side by side 
        '''
        matching_excel['Invoice']  = self.myVouchar["Invoice No."].append(self.givenVouchar["Invoice details Invoice number"])
        matching_excel['Sanitized Data'] = self.myVouchar["Invoice"].append(self.givenVouchar["Invoice"])

        self.match_report = pd.DataFrame(matching_excel)
        return

    def convert_to_float(self):
        # self.givenVouchar['Taxable Value (₹)'] = self.givenVouchar['Taxable Value (₹)'].astype(float)
        # self.givenVouchar['Tax Amount Integrated Tax  (₹)'] = self.givenVouchar[
        #     'Tax Amount Integrated Tax  (₹)'].astype(float)
        # self.givenVouchar['Tax Amount Central Tax (₹)'] = self.givenVouchar['Tax Amount Central Tax (₹)'].astype(float)
        # self.givenVouchar['Tax Amount State/UT tax (₹)'] = self.givenVouchar['Tax Amount State/UT tax (₹)'].astype(float)

        purchaseSideCols = [
                'Taxable Value',
                'Integrated Tax Amount',
                'Central Tax Amount',
                'State Tax Amount'
            ]

        self.myVouchar[
            purchaseSideCols
        ] = self.myVouchar[
            purchaseSideCols
        ].astype(float)

        logging.info("Convertion to float process on Purchase side Column:{} succeed".format(purchaseSideCols))

        salesSideCols = [
                'Taxable Value (₹)',
                'Tax Amount Integrated Tax  (₹)',
                'Tax Amount Central Tax (₹)',
                'Tax Amount State/UT tax (₹)'
            ]

        self.givenVouchar[
            salesSideCols
        ] = self.givenVouchar[
            salesSideCols
        ].astype(float)

        logging.info("Convertion to float process on Sales side Column:{} succeed".format(salesSideCols))

    def check_positive(self,data,cols=[]):
        for i in cols:
            if data[i]<0:
                return False
        return True

    '''
    Objective : Marks all the positive taxable values as "Debit" and negetive taxable values as "Credit"
    '''
    def format_type(self):
        self.convert_to_float()
        mv = []
        gv = []
        mvCols = [
            'Taxable Value',
            'Integrated Tax Amount',
            'Central Tax Amount',
            'State Tax Amount'
        ]
        gvCols = [
            'Taxable Value (₹)',
            'Tax Amount Integrated Tax  (₹)',
            'Tax Amount Central Tax (₹)',
            'Tax Amount State/UT tax (₹)'
        ]
        mySideDebitCreditCount = [0,0]
        for i, row in self.myVouchar.iterrows():
            if self.check_positive(row, mvCols):
                mv.append('d')
                mySideDebitCreditCount[0] += 1
            else:
                mv.append('c')
                mySideDebitCreditCount[1] += 1
        logging.info("Debit-Credit Count on Purchase side: {}".format(mySideDebitCreditCount))

        otherSideDebitCreditCount = [0, 0]
        for i, row in self.givenVouchar.iterrows():
            if self.check_positive(row, gvCols):
                gv.append('d')
                otherSideDebitCreditCount[0]+=1
            else:
                gv.append('c')
                otherSideDebitCreditCount[1]+=1

        logging.info("Debit-Credit Count on Sales side: {}".format(otherSideDebitCreditCount))
        self.myVouchar['type'] = mv
        self.givenVouchar['type'] = gv

    '''
    Objective : Combine multiple bills with same Gst no, Invoice Number, and type (Credit or Debit) into a single bills by summing up their values
    '''
    def combine_bill_mySide(self):
        # Combine separate bills in GST side
        initialLength = len(self.myVouchar)
        newVouchar = self.myVouchar.groupby(['GSTno.', 'Invoice', 'type'])[
            [
                'Taxable Value',
                'Integrated Tax Amount',
                'Central Tax Amount',
                'State Tax Amount'
            ]
        ].transform('sum')
        logging.info("Number of duplicate rows found on Purchase Side: {}".format(len(newVouchar) - initialLength))
        for i in newVouchar.keys():
            self.myVouchar[i] = newVouchar[i]

        self.myVouchar = self.myVouchar.drop_duplicates(subset=['GSTno.', 'Invoice', 'type'])
        logging.info("Duplicates dropped successfully")

    '''
    Objective : Combine multiple bills with same Gst no, Invoice Number, and type (Credit or Debit) into a single bills by summing up their values
    '''
    def combine_bill_otherSide(self):
        # Combine separate bills in GST side
        initialLength = len(self.givenVouchar)
        newVouchar = self.givenVouchar.groupby(['GSTno.', 'Invoice', 'type'])[
            [
                'Taxable Value (₹)',
                'Tax Amount Integrated Tax  (₹)',
                'Tax Amount Central Tax (₹)',
                'Tax Amount State/UT tax (₹)'
            ]
        ].transform('sum')
        logging.info("Number of duplicate rows found on Sales Side: {}".format(len(newVouchar)-initialLength))
        for i in newVouchar.keys():
            self.givenVouchar[i] = newVouchar[i]

        self.givenVouchar = self.givenVouchar.drop_duplicates(subset=['GSTno.', 'Invoice', 'type'])
        logging.info("Duplicates dropped successfully")

    '''
    Objective : write changes to Excel file
    '''
    def write_Result_to_excel(self):
        # Creating excel writer
        if self.Done_with_match:
            logging.info("Writting results")
            print(self.outFilePath)
            outFileWriter = pd.ExcelWriter(self.outFilePath, engine='xlsxwriter')

            #delete types in match_details
            if not self.MatchedDetails.empty:
                del self.MatchedDetails['type']
                logging.info("Matched details not empty, Type column deleted")

            # write into a file
            self.mergedData.to_excel(outFileWriter, sheet_name='All Data')
            logging.info("changes in Merged data written")
            self.MatchedDetails.to_excel(outFileWriter, sheet_name="Matched Data")
            logging.info("changes in Matched Details written")
            self.notMatched_myside.to_excel(outFileWriter, sheet_name="My Side")
            logging.info("changes in Unmatched Data on Purchase side written")
            self.notMatched_otherside.to_excel(outFileWriter, sheet_name="GST portal")
            logging.info("changes in Unmatched Data on Sales side written")
            self.match_report.to_excel(outFileWriter, sheet_name="Sanit of Invoice Report")
            logging.info("changes in Match Report written")
            self.givenVouchar.to_excel(outFileWriter, sheet_name="new sales")
            outFileWriter.save()
            # print("DONE")

        else:
            logging.info("Writter is not ready")


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


class Ui_MainWindow(Purchase_Sales_Match, QThread):

    def __init__(self):
        Purchase_Sales_Match.__int__(self)
        QThread.__init__(self)

    def setupUi(self, MainWindow):
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        MainWindow.setWindowTitle("Auto Match")
        MainWindow.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + "assets/icons/window.png"))

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(620, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.file1 = QtWidgets.QLabel(self.centralwidget)
        self.file1.setGeometry(QtCore.QRect(10, 20, 200, 21))
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
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.startProcess = QtWidgets.QPushButton(self.centralwidget)
        self.startProcess.setGeometry(QtCore.QRect(490, 300, 91, 41))
        self.startProcess.setFont(font)
        self.startProcess.setStyleSheet('''
            text-align: center;
            border: 1px solid transparent;
            background-color: transparent;
            color: #28a745;
            border-color: #28a745;
            padding-top: 5px;
            padding-bottom: 5px;
        ''')
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

        # # Progress bar
        # font = QtGui.QFont()
        # self.progressBar1 = QtWidgets.QProgressBar(self.centralwidget)
        # self.progressBar1.setEnabled(True)
        # self.progressBar1.setGeometry(QtCore.QRect(20, 310, 411, 23))
        # self.progressBar1.setMouseTracking(False)
        # self.progressBar1.setAutoFillBackground(False)
        # # self.progressBar1.setProperty("value", 0)
        # self.progressBar1.setValue(0)
        # self.progressBar1.setTextVisible(True)
        # self.progressBar1.setOrientation(QtCore.Qt.Horizontal)
        # self.progressBar1.setInvertedAppearance(False)
        # self.progressBar1.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        # self.progressBar1.setObjectName("progressBar1")
        # self.progressBar1.setMaximum(100)

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
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        MainWindow.setWindowTitle(_translate("MainWindow", "Auto Match"))
        MainWindow.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + "assets/icons/window.png"))
        self.file1.setText(_translate("MainWindow", "Import file for Purchase bill"))
        self.file2.setText(_translate("MainWindow", "Import file for Sales bill"))
        self.browseFile1.setText(_translate("MainWindow", "Browse"))
        self.browseFile2.setText(_translate("MainWindow", "Browse"))
        self.headerFile1.setText(_translate("MainWindow", "Header value(s)"))
        self.headerFile2.setText(_translate("MainWindow", "Header value(s)"))
        self.startProcess.setText(_translate("MainWindow", "Start"))
        self.lable_sheet1.setText(_translate("MainWindow", "Sheet Name"))
        self.lable_sheet2.setText(_translate("MainWindow", "Sheet Name"))

#     Fail-safe status
    def normal_status(self, n: str):
        logging.info(n)
        html = """
           <span>{}</span>
        """
        self.statusView.append(html.format(n))

    def success_status(self, n: str):
        logging.info(n)
        html = """
            <span style="color: green">{}</span>
        """
        self.statusView.append(html.format(n))

    def failure_status(self, n: str):
        logging.error(n)
        html = """
            <span style="color: red">{0}</span>
        """
        self.statusView.append(html.format(n))


    def open_dialog_box(self):
        fileName = QFileDialog.getOpenFileName()
        logging.info("dialog box opened")
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
        logging.info("Process started")
        # self.statusView.clear()
        self.main()
        logging.info("Process finished")

    @staticmethod
    def check_cronic(n):
        if (len(n)==1):return True
        for i in range(1,len(n)):
            if (n[i] != n[i-1]+1):
                return False
        return True

    def startProcess_handler(self):

        def getPoint(n):
            return [ (i-1) for i in n ]

        # self.file1Path = self.lineFile1.text()
        # self.file2Path = self.lineFile2.text()

        try:
            self.outFilePath = '/'.join(self.file1Path.split("/")[0:-1]) + '/mergedFile.xlsx'
            logging.info("Output file: " + self.outFilePath)
            header1 = self.headerLineFile1.text()
            header2 = self.headerLineFile2.text()
            # self.file1Sheet = self.sheetName1.text().strip()
            # self.file2Sheet = self.sheetName2.text().strip()
            self.file1Sheet = self.file1SheetName.currentText()
            self.file2Sheet = self.file2SheetName.currentText()

            if (header1=='' or header2==''):
                logging.error("Header contains nothing")
                raise MsgException("Header contains nothing")

            self.file1Header = getPoint(list(map(int, header1.strip().split(','))))
            self.file2Header = getPoint(list(map(int, header2.strip().split(','))))

            if not (self.check_cronic(self.file1Header) and self.check_cronic(self.file2Header)):
                raise MsgException("Wrong Header value")
            self.statusView.clear()
            self.start()
        except Exception as e:
            # print("Problem with file Header. Enter value correctly")
            self.failure_status(str(e))
            # raise MsgException("Header format error")


        print("StartBtn Finished")


    def init_button(self):
        self.browseFile1.clicked.connect(self.brwsFile1_handler)
        self.browseFile2.clicked.connect(self.brwsFile2_handler)
        self.startProcess.clicked.connect(self.startProcess_handler)

    def read_file1(self):
        self.file1SheetName.clear()
        try:
            # print("reading " + self.file1Path)
            file1 = pd.ExcelFile(self.file1Path)
            for i in file1.sheet_names:
                self.file1SheetName.addItem(i)
            self.success_status("{} file is OK".format(self.file1Path))
            return file1
        except Exception as e:
            self.failure_status(str(e))
            logging.error("Can't read excel file " + self.file1Path)
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
            self.success_status("{} file is OK".format(self.file2Path))
            return file2
        except Exception as e:
            self.failure_status(str(e))
            logging.error("Can't read excel file " + self.file2Path)
            self.file2Path = None
            self.lineFile2.clear()
            self.file2SheetName.clear()
            return None

    def match_work(self):
        count = 0
        self.Done_with_match = False

        matchresult = []
        data = self.mergedData
        notMatched_myside = {}
        notMatched_otherside = {}
        MatchedDetails = []

        mycols = self.mycols.copy()
        gvcols = self.gvcols.copy()
        self.normal_status("editing GST no")
        mycols[1] = gvcols[0] = "GSTno."
        self.success_status("Done")

        for i in mycols:
            notMatched_myside[i]=[]

        for i in gvcols:
            notMatched_otherside[i]=[]

        for i, j in data.iterrows():
            r: bool = True
            gst1, gst2 = j['Taxable Value'], j['Taxable Value (₹)']
            igst1, igst2 = j['Integrated Tax Amount'], j['Tax Amount Integrated Tax  (₹)']
            cgst1, cgst2 = j['Central Tax Amount'], j['Tax Amount Central Tax (₹)']
            sgst1, sgst2 = j['State Tax Amount'], j['Tax Amount State/UT tax (₹)']

            if not Purchase_Sales_Match.float_compare(gst1, gst2):
                r = False
            if not Purchase_Sales_Match.float_compare(igst1, igst2):
                r = False
            if not Purchase_Sales_Match.float_compare(sgst1, sgst2):
                r = False
            if not Purchase_Sales_Match.float_compare(cgst1, cgst2):
                r = False
            if r:
                count += 1
                matchresult.append("MATCHED")
                MatchedDetails.append(j)
            else:
                matchresult.append("NOT MATCHED")
                if int(gst1)==0 and int(igst1)==0 and int(cgst1)==0 and int(sgst1)==0:
                    for k in gvcols:
                        notMatched_otherside[k].append(j[k])
                elif int(gst2)==0 and int(igst2)==0 and int(cgst2)==0 and int(sgst2)==0:
                    for k in mycols:
                        notMatched_myside[k].append(j[k])
                else:
                    for k in gvcols:
                        notMatched_otherside[k].append(j[k])

                    for k in mycols:
                        notMatched_myside[k].append(j[k])


        data['Result'] = matchresult
        print("Found match in {0}/{1}".format(count, len(matchresult)))
        self.success_status("Found match in {0}/{1}".format(count, len(matchresult)))
        rate = count*100/len(matchresult)
        print("Matched: {}%".format(round(rate,2)))
        self.success_status("Matched: {}%".format(round(rate,2)))
        self.MatchedDetails = pd.DataFrame(MatchedDetails)
        self.notMatched_myside = pd.DataFrame(notMatched_myside)
        self.notMatched_otherside = pd.DataFrame(notMatched_otherside)
        self.Done_with_match = True
        return

    def main(self):
        start = time.time()
        self.Done_with_match = False
        try:
            if self.myExcel:
                self.normal_status("Reading {}".format(self.file1Path))
                self.myVouchar = pd.read_excel(self.myExcel, self.file1Sheet, header=self.file1Header).fillna(0)
                self.success_status("file read successful, format OK")

            else:
                # raise exception
                raise ExcelReadException(self.file1Path)


            if self.givenExcel:
                self.normal_status("Reading {}".format(self.file2Path))
                self.givenVouchar = pd.read_excel(self.givenExcel, self.file2Sheet, header=self.file2Header).fillna(0)
                self.success_status("file read successful, format OK")
            else:
                #raise exception
                raise ExcelReadException(self.file2Path)

            if self.myExcel and self.givenExcel:
                self.normal_status("formatting Headers")
                self.myVouchar.columns, self.givenVouchar.columns = self.format_header()
                self.success_status("Done")

                # Sanitary check of data
                self.normal_status("Sanitizing Data")
                self.data_sanit()
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

                #sorting Data
                self.normal_status("Sorting Data")
                self.myVouchar.sort_values(['GSTno.', 'Invoice'], ascending=[True, True])
                self.givenVouchar.sort_values(['GSTno.', 'Invoice'], ascending=[True, True])
                self.success_status("Done")

                # format type => debit or credit
                self.normal_status("Adding Types")
                self.format_type()
                self.success_status("Done")

                # # Combine separate bills
                # in mySide
                self.normal_status("Combining bills on purchase side")
                self.combine_bill_mySide()
                self.success_status("Done")
                # GST side
                self.normal_status("Combining bills on GST side")
                self.combine_bill_otherSide()
                self.success_status("Done")

                #  data join
                self.normal_status("Merging data Sets")
                self.mergedData = pd.merge(self.myVouchar, self.givenVouchar, on=['GSTno.', 'Invoice', 'type'], how='outer').fillna(0)
                self.success_status("Done")

                # match
                self.normal_status("Finding for match")
                self.match_work()
                self.success_status("Done")

                # spliting
                # self.notMatched_myside = self.myVouchar[self.myVouchar['visited'] == 1]
                # self.notMatched_otherside = self.givenVouchar[self.givenVouchar['visited'] == 1]

                # # Creating excel writer
                # outFileWriter = pd.ExcelWriter(self.outFilePath, engine='xlsxwriter')

                # # write into a file
                # # self.normal_status("Creating output file")
                # self.mergedData.to_excel(outFileWriter, sheet_name='All Data')
                # self.MatchedDetails.to_excel(outFileWriter, sheet_name="Matched Data")
                # self.notMatched_myside.to_excel(outFileWriter, sheet_name="My Side")
                # self.notMatched_otherside.to_excel(outFileWriter, sheet_name="GST portal")
                # outFileWriter.save()

                self.normal_status("Writting Results")
                self.write_Result_to_excel()
                self.success_status("Done")

        except Exception as e:
            print(str(e))
            self.failure_status(str(e))
            self.failure_status("Process cancelled")

        # print("Process finished in : {0} secs".format(round(time.time() - start), 3))
        self.normal_status("Process finished in : {0} secs".format(round(time.time() - start), 3))




if __name__ == "__main__":
    import sys

    logging.basicConfig(filename="assets/log/AutoMatch_Log.txt", level=logging.INFO, format="%(asctime)s : %(levelname)s : %(lineno)d : %(message)s")

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
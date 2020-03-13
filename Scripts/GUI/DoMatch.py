from _hashlib import new

from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QApplication, QHBoxLayout, QMainWindow, \
    QPushButton, QVBoxLayout, QComboBox, QGridLayout, QLabel, QWidget, QLineEdit, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore
import pandas as pd
import sys
from Scripts.GUI.ShowDetailsWidget import show_details
from Scripts.GUI.tableWidget import table_widget


class Input(QDialog):
    send_filePath = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.filePath = None;
        self.Excel: pd.ExcelFile = None;

        self.init_ui()

    def open_dialog_box(self):
        fileName = QFileDialog.getOpenFileName()
        return fileName[0]

    def brwsFile_handler(self):
        self.filePath = self.open_dialog_box()
        self.startLineEdit.setText(self.filePath)
        self.Excel = self.read_file()

        if (self.Excel!=None):
            self.send_filePath.emit(self.filePath)


    def read_file(self):
        try:
            # print("reading " + self.file1Path)
            file1 = pd.ExcelFile(self.filePath)
            # self.success_status("{} file is OK".format(self.file1Path))

            return file1
        except Exception as e:
            # self.failure_status(str(e))
            self.filePath=None
            self.startLineEdit.clear()
            return None

    def init_ui(self):
        gBox_start = QGridLayout()

        self.startLabel = QLabel("Import Merged File Here :- ", )
        self.startLineEdit = QLineEdit()
        self.startBrowseBtn = QPushButton("Browse")
        self.startBrowseBtn.clicked.connect(self.brwsFile_handler);

        gBox_start.addWidget(self.startLabel, 0, 0);
        gBox_start.addWidget(self.startLineEdit, 1, 0)
        gBox_start.addWidget(self.startBrowseBtn, 1, 1)

        self.setLayout(gBox_start)


class do_match_gui(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mySide_data: pd.DataFrame = None
        self.otherSide_data: pd.DataFrame = None

        self.selected_mySide: pd.Series = pd.Series(dtype=float)
        self.selected_otherSide: pd.Series = pd.Series(dtype=float)

        self.read_cols_mySide = [
            'GSTno.', 'Invoice No.', 'Particulars', 'Taxable Value', 'Integrated Tax Amount',
            'Central Tax Amount', 'State Tax Amount'
        ]
        self.read_cols_otherSide = [
            'GSTno.', 'Invoice details Invoice number', 'Trade/Legal name of the Supplier', 'Taxable Value (₹)',
            'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)', 'Tax Amount State/UT tax (₹)'
        ]

        self.mySide_otherSide_intersection = list(set(self.read_cols_mySide).intersection(set(self.read_cols_otherSide)))
        self.write_cols = [
            'GSTNo.', "Invoice", "Company", "TaxableValue", "cgst", 'sgst', 'igst'
        ]

        self.match_store = []

        self.filePath = None;
        self.Excel: pd.ExcelFile= None;

        self.init_ui()
        self.show()

        self.input_window()

    def input_window(self):
        self.In.show()

    def get_file_input(self, filePath):
        self.In.close()
        print(filePath)
        self.filePath = filePath
        self.Excel = pd.ExcelFile(self.filePath)
        try:
            mySide_data = pd.read_excel(self.Excel, sheet_name='My Side')
            otherSide_data = pd.read_excel(self.Excel, sheet_name='GST portal')
            print("get Files")
            if self.load_data(mySide_data, otherSide_data):
                print("load data")
                self.fill_data()
                print("fill data")
        except Exception as e:
            print(str(e))
            self.input_window()


    def match_btn_enable(self):
        if (self.selected_mySide.empty or self.selected_otherSide.empty):
            self.match_btn.setDisabled(True)
        else:
            self.match_btn.setEnabled(True)

    def mySide_item_clicked(self, row, col):
        print(row, col)
        # read_cols = [
        #     'GSTno.', 'Invoice No.', 'Particulars', 'Taxable Value', 'Integrated Tax Amount',
        #     'Central Tax Amount', 'State Tax Amount'
        # ]
        # write_cols = [
        #     'GSTNo.', "Invoice", "Company", "TaxableValue", "cgst", 'sgst', 'igst'
        # ]
        data = self.mySide.select_rows(row)
        print("Myside" ,data)
        self.selected_mySide = pd.Series(data)
        write_data = {}
        for to, frm in zip(self.write_cols, self.read_cols_mySide):
            write_data[to] = data[frm]
        print(write_data)
        self.left_side.set_data(write_data)
        self.match_btn_enable()


    def otherSide_item_clicked(self, row, col):
        print(row, col)
        # read_cols = [
        #     'GSTno.', 'Invoice details Invoice number', 'Trade/Legal name of the Supplier', 'Taxable Value (₹)',
        #     'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)', 'Tax Amount State/UT tax (₹)'
        # ]
        # write_cols = [
        #     'GSTNo.', "Invoice", "Company", "TaxableValue", "cgst", 'sgst', 'igst'
        # ]
        data = self.otherSide.select_rows(row)
        print("other side ", data)
        self.selected_otherSide = pd.Series(data)
        write_data = {}
        for to, frm in zip(self.write_cols, self.read_cols_otherSide):
            write_data[to] = data[frm]
        # print(write_data)
        self.right_side.set_data(write_data)
        self.match_btn_enable()

    def filter(self):
        text = self.filter_line.currentText()
        # print(text)
        if text == 'Select all':
            text = ''
        self.mySide.filter_rows(text, on='GSTno.')
        self.otherSide.filter_rows(text, on='GSTno.')

    def msg_box(self, message):
        msgBox = QMessageBox(self)
        reply = msgBox.question(self, 'Warning',
                                (
                                    str(message)
                                ),
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply

    def load_data(self, first:pd.DataFrame=None, second:pd.DataFrame=None):
        if not (first.empty or second.empty):
            self.mySide_data, self.otherSide_data = first, second
            del self.mySide_data['Unnamed: 0']
            del self.otherSide_data['Unnamed: 0']
            return True
        return False

    def fill_data(self):
        self.mySide.fill_Data(self.mySide_data)
        self.otherSide.fill_Data(self.otherSide_data)

        keys = pd.Series(["Select all"]).append(self.mySide_data['GSTno.']).append(self.otherSide_data['GSTno.'])
        keys = keys.drop_duplicates()
        for i in keys:
            self.filter_line.addItem(str(i))

    def finalize_match(self):
        try:
            del self.selected_mySide["GSTno."]
            data = self.selected_mySide.append(self.selected_otherSide)
            self.match_store.append(data)
            print(data)
            # Make selecteddata Null
            self.selected_mySide = self.selected_otherSide = pd.Series(dtype=float)
            # clearing show_details widgets
            self.left_side.clear_data()
            self.right_side.clear_data()
            # deleting rows from tables
            self.mySide.delete_row()
            self.otherSide.delete_row()
            # making match_btn disable
            self.match_btn_enable()
        except Exception as e:
            print(str(e))

    def match_work(self):
        try:
            if not (self.selected_mySide.empty or self.selected_otherSide.empty):
                print("inside match_work")
                left = self.left_side.get_data()
                right = self.right_side.get_data()
                print("left right")

                if (left['TaxableValue'] == right['TaxableValue'] and left['cgst'] == right['cgst'] and left['sgst'] ==
                        right['sgst'] and left['igst'] == right['igst']):
                    self.finalize_match()
                else:
                    reply = self.msg_box("Are you sure to match?  The selected items don't seem to be matching")
                    if reply == QMessageBox.Yes:
                        self.finalize_match()
        except Exception as ve:
            print(str(ve))

    def save_work(self):
        if self.match_store!=[]:
            reply = self.msg_box("You are in the middle of your work. Would you like to Save it? ")
            if reply == QMessageBox.Yes:
                self.write_Result_to_excel()
        else:
            print("Nothing to write")

    def init_ui(self):
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.mySide = table_widget()
        self.mySide.setFixedHeight(300)
        self.otherSide = table_widget()
        self.otherSide.setFixedHeight(300)

        self.mySide.cellClicked.connect(self.mySide_item_clicked)

        self.otherSide.cellClicked.connect(self.otherSide_item_clicked)

        self.filter_line = QComboBox()
        self.filter_line.currentTextChanged.connect(self.filter)

        self.left_side = show_details()
        self.right_side = show_details()

        self.left_side.setFixedHeight(150)
        self.left_side.setFixedWidth(400)
        self.right_side.setFixedHeight(150)
        self.right_side.setFixedWidth(400)

        # match button
        self.match_btn = QPushButton('Match')
        self.match_btn_enable()
        self.match_btn.clicked.connect(self.match_work)

        # Save button
        self.save_work_btn = QPushButton("Save Work")
        self.save_work_btn.clicked.connect(self.save_work)

        Main_gBox = QGridLayout()

        Main_gBox.addWidget(self.filter_line, 0, 1)
        Main_gBox.addWidget(self.save_work_btn, 0,2)
        Main_gBox.addWidget(self.mySide, 1, 0)
        Main_gBox.addWidget(self.otherSide, 1, 2)
        Main_gBox.addWidget(self.left_side, 2, 0)
        Main_gBox.addWidget(self.match_btn, 2,1)
        Main_gBox.addWidget(self.right_side, 2, 2)

        self.setLayout(Main_gBox)

        self.In = Input()
        self.In.send_filePath.connect(self.get_file_input)

    def closeEvent(self, QCloseEvent):
        self.In.close()
        self.save_work()
        super().closeEvent(QCloseEvent)

    def write_Result_to_excel(self):
        try:
            # Creating excel writer
            print("Writting results")
            print(self.filePath)
            outFileWriter = pd.ExcelWriter(self.filePath, engine='xlsxwriter')

            prev_matched = pd.read_excel(self.Excel, sheet_name='Matched Data')
            del prev_matched['Unnamed: 0']
            new_data = pd.DataFrame(self.match_store)
            current_matched = prev_matched.append(new_data, ignore_index=True)

            print(new_data.shape, prev_matched.shape, current_matched.shape)

            # write into a file
            current_matched.to_excel(outFileWriter, sheet_name="Matched Data")
            self.mySide.data.to_excel(outFileWriter, sheet_name="My Side")
            self.otherSide.data.to_excel(outFileWriter, sheet_name="GST portal")

            outFileWriter.save()
            self.match_store=[]
            # print("DONE")
        except Exception as e:
            print(str(e))




if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = do_match_gui()

    # file = pd.ExcelFile('E:\\Programs\\Py\\TallyProject\media\\testSet5\\mergedFile.xlsx')
    #
    # mySide_data = pd.read_excel(file, sheet_name='My Side')
    # otherSide_data = pd.read_excel(file, sheet_name='GST portal')
    # if main.load_data(mySide_data, otherSide_data):
    #     main.fill_data()

    # main.show()
    # main.setDisabled(True)

    sys.exit(app.exec_())

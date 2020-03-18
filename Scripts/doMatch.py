from PyQt5.QtCore import QRect, Qt

from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QApplication, QHBoxLayout, QMainWindow, \
    QPushButton, QVBoxLayout, QComboBox, QGridLayout, QLabel, QWidget, QLineEdit, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon
import pandas as pd
import sys


class pair_label(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLabel()
        self.second = QLabel()

        hbox = QHBoxLayout()
        hbox.addWidget(self.first)
        hbox.addWidget(self.second)

        self.setLayout(hbox)

class show_details(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.gstNo = pair_label()
        self.gstNo.first.setText("GSTNo :-")


        self.invoice_no = pair_label()
        self.invoice_no.first.setText("Invoice no. :-")

        self.company_name = pair_label()
        self.company_name.first.setText('Company name :-')

        self.taxableValue = pair_label()
        self.taxableValue.first.setText("Taxable Value :-")

        self.cgst = pair_label()
        self.sgst = pair_label()
        self.igst = pair_label()

        self.cgst.first.setText("CGST :-")
        self.sgst.first.setText("SGST :-")
        self.igst.first.setText("IGST :-")

        grid = QGridLayout()

        grid.addWidget(self.gstNo, 0,0)
        grid.addWidget(self.invoice_no, 0,1)
        grid.addWidget(self.company_name, 1,0,1,0)
        grid.addWidget(self.taxableValue, 2,0)
        grid.addWidget(self.cgst, 2,1)
        grid.addWidget(self.igst, 3,0)
        grid.addWidget(self.sgst, 3,1)


        self.setLayout(grid)

    # setters
    def set_gstno(self, value):
        self.gstNo.second.setText(value)

    def set_invoice(self, value):
        self.invoice_no.second.setText(value)
    def set_company(self,value):
        self.company_name.second.setText(value)
    def set_cgst(self,value):
        self.cgst.second.setText(value)
    def set_taxablevalue(self,value):
        self.taxableValue.second.setText(value)
    def set_sgst(self,value):
        self.sgst.second.setText(value)
    def set_igst(self,value):
        self.igst.second.setText(value)

    # getters
    def get_gstno(self):
        return self.gstNo.second.text()
    def get_invoice(self):
        return self.invoice_no.second.text()
    def get_company(self):
        return self.company_name.second.text()
    def get_cgst(self):
        return float(self.cgst.second.text())
    def get_taxablevalue(self):
        return float(self.taxableValue.second.text())
    def get_sgst(self):
        return float(self.sgst.second.text())
    def get_igst(self):
        return float(self.igst.second.text())

    # format of data
    # {
    #     'GSTNo.' : "<>",
    #     'Invoice' : "<>",
    #     'Company' : "<>",
    #     'TaxableValue' : "<>",
    #     'cgst' : "<>",
    #     'sgst' : "<>",
    #     'igst' : "<>"
    # }
    def set_data(self, dict_data):  # follow the format mentioned above
        try:
            self.set_gstno(dict_data['GSTNo.'])
            self.set_invoice(dict_data['Invoice'])
            self.set_company(dict_data['Company'])
            self.set_taxablevalue(dict_data['TaxableValue'])
            self.set_cgst(dict_data['cgst'])
            self.set_sgst(dict_data['sgst'])
            self.set_igst(dict_data['igst'])
        except Exception as e:
            print(str(e))

    # format of data
    # {
    #     'GSTNo.' : "<>",
    #     'Invoice' : "<>",
    #     'Company' : "<>",
    #     'TaxableValue' : "<>",
    #     'cgst' : "<>",
    #     'sgst' : "<>",
    #     'igst' : "<>"
    # }
    def get_data(self):
        try:
            return {
                'GSTNo.': self.get_gstno(),
                'Invoice': self.get_invoice(),
                'Company': self.get_company(),
                'TaxableValue': self.get_taxablevalue(),
                'cgst': self.get_cgst(),
                'sgst': self.get_sgst(),
                'igst': self.get_igst()
            }
        except Exception as e:
            print(str(e))

    def clear_data(self):
        self.set_gstno('')
        self.set_invoice('')
        self.set_company('')
        self.set_taxablevalue('')
        self.set_cgst('')
        self.set_sgst('')
        self.set_igst('')


class table_widget(QTableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data : pd.DataFrame = None
        self.retranslateUi()

        self.selected_row = -1

    def fill_Data(self, Data: pd.DataFrame ):
        row, column = Data.shape
        self.data = Data
        self.setRowCount(row)
        self.setColumnCount(column)
        self.key = list(self.data.keys())
        self.render_items()

    def render_items(self):
        column = len(self.key)
        self.setHorizontalHeaderLabels(self.key)

        for i, j in self.data.iterrows():
            for k in range(column):
                item = QTableWidgetItem(str(j[self.key[k]]))
                item.setFlags(Qt.ItemIsEnabled)
                self.setItem(i,k, item)

        self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)
        # self.setStyleSheet("alternate-background-color: white;background-color: red;")

    def retranslateUi(self):
        pass

    def select_rows(self, row):
        # return tuple(self.item(row, col).text() for col in range(self.columnCount()))
        d = {}
        for i,col in zip(self.key,range(self.columnCount())):
            j = self.item(row, col).text()
            d[i]=j

        self.selected_row=row
        return d

    def delete_row(self):
        if self.selected_row!= -1:
            self.removeRow(self.selected_row)
            self.data = self.data.drop(self.data.index[self.selected_row])
            return True
        return False

    def filter_rows(self, filter_text, on='name'):
        # print(filter_text)
        column_index = self.key.index(on)
        # print(column_index)
        try:
            for row in range(self.rowCount()):
                match = False
                item = self.item(row, column_index)
                # print("item")
                if ( filter_text.lower() in item.text().lower()):
                    # print(row)
                    match = True
                self.setRowHidden(row, not match)
        except Exception as e:
            print(str(e))

    def get_data(self):
        return self.data




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

        self.filter_line_selected_index = -1
        self.keys = []

        self.selected_mySide: pd.Series = pd.Series(dtype=float)
        self.selected_otherSide: pd.Series = pd.Series(dtype=float)

        self.read_cols_mySide = [
            'GSTno.', 'Invoice No.', 'Particulars', 'Taxable Value', 'Integrated Tax Amount',
            'Central Tax Amount', 'State Tax Amount', 'Date'
        ]
        self.read_cols_otherSide = [
            'GSTno.', 'Invoice details Invoice number', 'Trade/Legal name of the Supplier', 'Taxable Value (₹)',
            'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)', 'Tax Amount State/UT tax (₹)','Invoice details Invoice Date'
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
        self.setEnabled(True)
        self.filePath = filePath
        self.Excel = pd.ExcelFile(self.filePath)
        try:
            mySide_data = pd.read_excel(self.Excel, sheet_name='My Side')
            otherSide_data = pd.read_excel(self.Excel, sheet_name='GST portal')
            if self.load_data(mySide_data, otherSide_data):
                self.fill_data()
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
        data = self.mySide.select_rows(row)
        self.selected_mySide = pd.Series(data)
        write_data = {}
        for to, frm in zip(self.write_cols, self.read_cols_mySide):
            write_data[to] = data[frm]
        print(write_data)
        self.left_side.set_data(write_data)
        self.match_btn_enable()


    def otherSide_item_clicked(self, row, col):
        print(row, col)
        data = self.otherSide.select_rows(row)
        self.selected_otherSide = pd.Series(data)
        write_data = {}
        for to, frm in zip(self.write_cols, self.read_cols_otherSide):
            write_data[to] = data[frm]
        # print(write_data)
        self.right_side.set_data(write_data)
        self.match_btn_enable()

    def filter(self):
        text = self.filter_line.currentText()
        self.filter_line_selected_index = self.keys.index(text)
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
            self.keys.append(str(i))
            self.filter_line.addItem(str(i))

    def finalize_match(self):
        try:
            del self.selected_mySide["GSTno."]
            data = self.selected_mySide.append(self.selected_otherSide)
            self.match_store.append(data)
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
                left = self.left_side.get_data()
                right = self.right_side.get_data()

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

    def go_prev(self):
        if (self.filter_line_selected_index>0):
            self.filter_line_selected_index-=1
            self.filter_line.setCurrentText(self.keys[self.filter_line_selected_index])
    def go_next(self):
        if (self.filter_line_selected_index < len(self.keys) -1):
            self.filter_line_selected_index += 1
            self.filter_line.setCurrentText(self.keys[self.filter_line_selected_index])

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
        self.save_work_btn = QPushButton("Save")
        self.save_work_btn.clicked.connect(self.save_work)

        gBox = QGridLayout()
        self.filter_prev_btn = QPushButton()
        self.filter_prev_btn.setIcon(QIcon('E:\Programs\Py\TallyProject\media\icons\provious.png'))
        self.filter_prev_btn.clicked.connect(self.go_prev)
        self.filter_next_btn = QPushButton()
        self.filter_next_btn.setIcon(QIcon('E:\Programs\Py\TallyProject\media\icons\\next.png'))
        self.filter_next_btn.clicked.connect(self.go_next)
        gBox.addWidget(self.filter_prev_btn,1,0)
        gBox.addWidget(self.filter_next_btn,1,1)
        gBox.addWidget(self.filter_line,0,0,1,0)

        Main_gBox = QGridLayout()

        Main_gBox.addItem(gBox, 0, 1)
        Main_gBox.addWidget(self.save_work_btn, 3,1)
        Main_gBox.addWidget(self.mySide, 1, 0)
        Main_gBox.addWidget(self.otherSide, 1, 2)
        Main_gBox.addWidget(self.left_side, 2, 0)
        Main_gBox.addWidget(self.match_btn, 2,1)
        Main_gBox.addWidget(self.right_side, 2, 2)

        self.setLayout(Main_gBox)
        self.setDisabled(True)

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

    sys.exit(app.exec_())

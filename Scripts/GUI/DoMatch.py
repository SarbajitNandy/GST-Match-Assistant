from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem,  QApplication, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QComboBox, QGridLayout, QLabel, QWidget
import pandas as pd
import sys
from Scripts.GUI.ShowDetailsWidget import show_details
from Scripts.GUI.tableWidget import table_widget

class do_match_gui(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

        self.show()

    def student_item_clicked(self, row, col):
        print(row, col)
        read_cols = [
            'GSTno.', 'Invoice No.', 'Particulars', 'Taxable Value', 'Integrated Tax Amount',
            'Central Tax Amount', 'State Tax Amount'
        ]
        write_cols = [
            'GSTNo.', "Invoice", "Company", "TaxableValue", "cgst", 'sgst', 'igst'
        ]
        read_data = self.mySide.select_rows(row)
        write_data = {}
        for to, frm in zip(write_cols, read_cols):
            write_data[to] = read_data[frm]
        # print(write_data)
        self.left_side.set_data(write_data)

    def dept_item_clicked(self, row, col):
        print(row, col)
        read_cols = [
            'GSTno.', 'Invoice details Invoice number', 'Trade/Legal name of the Supplier', 'Taxable Value (₹)',
            'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)', 'Tax Amount State/UT tax (₹)'
        ]
        write_cols = [
            'GSTNo.', "Invoice", "Company", "TaxableValue", "cgst", 'sgst', 'igst'
        ]
        read_data = self.otherSide.select_rows(row)
        write_data = {}
        for to, frm in zip(write_cols, read_cols):
            write_data[to] = read_data[frm]
        # print(write_data)
        self.right_side.set_data(write_data)

    def filter(self):
        text = self.filter_line.currentText()
        # print(text)
        if text == 'Select all':
            text = ''
        self.mySide.filter_rows(text, on='GSTno.')
        self.otherSide.filter_rows(text, on='GSTno.')

    def init_ui(self):

        self.mySide = table_widget()
        self.mySide.setFixedHeight(300)
        self.otherSide = table_widget()
        self.otherSide.setFixedHeight(300)

        # take two dataframes
        file_path = 'D:\\Programs\\Py\\TallyProject\\media\\testSet5\\mergedFile.xlsx'
        file = pd.ExcelFile(file_path)

        mySide = pd.read_excel(file, sheet_name='My Side')
        otherSide = pd.read_excel(file, sheet_name='GST portal')

        self.mySide.fill_Data(mySide)
        self.mySide.cellClicked.connect(self.student_item_clicked)
        self.otherSide.fill_Data(otherSide)
        self.otherSide.cellClicked.connect(self.dept_item_clicked)

        self.filter_line = QComboBox()

        keys = pd.Series(["Select all"]).append(mySide['GSTno.']).append(otherSide['GSTno.'])
        keys = keys.drop_duplicates()
        for i in keys:
            self.filter_line.addItem(str(i))

        self.filter_line.currentTextChanged.connect(self.filter)

        self.left_side = show_details()
        self.right_side = show_details()

        self.left_side.setFixedHeight(150)
        self.left_side.setFixedWidth(400)
        self.right_side.setFixedHeight(150)
        self.right_side.setFixedWidth(400)

        gBox = QGridLayout()

        gBox.addWidget(self.filter_line, 0, 1)
        gBox.addWidget(self.mySide, 1, 0)
        gBox.addWidget(self.otherSide, 1, 3)
        # gBox.addWidget(filter_line, 1,0)
        gBox.addWidget(self.left_side, 2, 0)
        gBox.addWidget(self.right_side, 2, 3)

        self.setLayout(gBox)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = do_match_gui()

    sys.exit(app.exec_())

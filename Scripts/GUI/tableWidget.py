from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem,  QApplication, QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QComboBox, QGridLayout, QLabel, QWidget
import pandas as pd
import sys
from Scripts.GUI.ShowDetailsWidget import show_details

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

    def clicked(self):
        print("clicked")

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
            print(self.selected_row)
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
        return self.data;

# if __name__ == "__main__":
#     def student_item_clicked(row, col):
#         print(row, col)
#         read_cols = [
#             'GSTno.', 'Invoice No.', 'Particulars', 'Taxable Value', 'Integrated Tax Amount', 'Central Tax Amount', 'State Tax Amount'
#         ]
#         write_cols = [
#             'GSTNo.', "Invoice", "Company", "TaxableValue", "cgst", 'sgst', 'igst'
#         ]
#         read_data = student_details.select_rows(row)
#         write_data = {}
#         for to, frm in zip(write_cols, read_cols):
#             write_data[to] = read_data[frm]
#         # print(write_data)
#         left_side.set_data(write_data)
#
#
#     def dept_item_clicked(row, col):
#         print(row, col)
#         read_cols = [
#             'GSTno.', 'Invoice details Invoice number', 'Trade/Legal name of the Supplier', 'Taxable Value (₹)', 'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)', 'Tax Amount State/UT tax (₹)'
#         ]
#         write_cols = [
#             'GSTNo.', "Invoice", "Company", "TaxableValue", "cgst", 'sgst', 'igst'
#         ]
#         read_data = dept_details.select_rows(row)
#         write_data = {}
#         for to, frm in zip(write_cols, read_cols):
#             write_data[to] = read_data[frm]
#         # print(write_data)
#         right_side.set_data(write_data)
#
#
#     def filter():
#         text = filter_line.currentText()
#         # print(text)
#         if text == 'Select all':
#             text = ''
#         student_details.filter_rows(text, on='GSTno.')
#         dept_details.filter_rows(text, on='GSTno.')
#
#
#     app = QApplication(sys.argv)
#     main = QWidget()
#
#     student_details = table_widget()
#     student_details.setFixedHeight(300)
#     dept_details = table_widget()
#     dept_details.setFixedHeight(300)
#
#     # take two dataframes
#     file_path = 'D:\\Programs\\Py\\TallyProject\\media\\testSet5\\mergedFile.xlsx'
#     file = pd.ExcelFile(file_path)
#
#     mySide = pd.read_excel(file, sheet_name='My Side')
#     otherSide = pd.read_excel(file, sheet_name='GST portal')
#
#     student_details.fill_Data(mySide)
#     student_details.cellClicked.connect(student_item_clicked)
#     dept_details.fill_Data(otherSide)
#     dept_details.cellClicked.connect(dept_item_clicked)
#
#     filter_line = QComboBox()
#
#     keys = pd.Series(["Select all"]).append(mySide['GSTno.']).append(otherSide['GSTno.'])
#     keys = keys.drop_duplicates()
#     for i in keys:
#         filter_line.addItem(str(i))
#
#     filter_line.currentTextChanged.connect(filter)
#
#     # show details block starts
#     # for left side
#     # left_name = QLabel("Name")
#     # left_name_value = QLabel()
#     #
#     # left_dept = QLabel("Department")
#     # left_dept_value = QLabel()
#     left_side = show_details()
#     right_side = show_details()
#
#     left_side.setFixedHeight(150)
#     left_side.setFixedWidth(400)
#     right_side.setFixedHeight(150)
#     right_side.setFixedWidth(400)
#
#     gBox = QGridLayout()
#
#     gBox.addWidget(filter_line, 0,1)
#     gBox.addWidget(student_details, 1,0)
#     gBox.addWidget(dept_details, 1,3)
#     # gBox.addWidget(filter_line, 1,0)
#     gBox.addWidget(left_side, 2,0)
#     gBox.addWidget(right_side, 2,3)
#
#
#     main.setLayout(gBox)
#
#     main.show()
#
#     sys.exit(app.exec_())
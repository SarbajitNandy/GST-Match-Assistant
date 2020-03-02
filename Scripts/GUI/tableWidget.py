from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem,  QApplication, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QGridLayout, QLabel
import pandas as pd
import sys

class table_widget(QTableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data : pd.DataFrame = None
        self.retranslateUi()

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
        return tuple(self.item(row, col).text() for col in range(self.columnCount()))


    def delete_row(self, row):
        print(row)
        self.data = self.data.drop(self.data.index[row])
        print(self.data)
        # self.removeRow(row)

    def filter_rows(self, filter_text, on='name'):
        print(filter_text)
        column_index = self.key.index(on)
        print(column_index)
        try:
            for row in range(self.rowCount()):
                match = False
                item = self.item(row, column_index)
                print("item")
                if ( filter_text.lower() in item.text().lower()):
                    print(row)
                    match = True
                self.setRowHidden(row, not match)
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    def student_item_clicked(row, col):
        print(row, col)
        name, dept = student_details.select_rows(row)
        print(name, dept)
        left_name_value.setText(name)
        left_dept_value.setText(dept)


    def dept_item_clicked(row, col):
        print(row, col)


    def filter():
        text = filter_line.currentText()
        # print(text)
        if text == 'Select all':
            text = ''
        student_details.filter_rows(text)
        dept_details.filter_rows(text)


    app = QApplication(sys.argv)
    main = QDialog()

    student_details = table_widget()
    dept_details = table_widget()

    # take two dataframes
    s1 = [
        { 'name':"Sarbajit Nandy", "dept": "CSE"},
        { 'name':'Shalmoli Neogi', "dept": "CSE"},
        { 'name':"Shuvankar Roy", "dept": "CSE"},
        { 'name':"Supriya Kundu", "dept": "CSE"}
    ]
    d1 = pd.DataFrame(s1)

    s2 = [
        {'name':'Sarbajit Nandy', 'dept':'CSE', 'hod':'SST'},
        { 'name':'Shalmoli Neogi', 'dept':'IT', 'hod':'ABC'},
        { 'name': 'Supriya Kundu', 'dept':'ECE', 'hod':'XYZ'},
    ]
    d2 = pd.DataFrame(s2)

    student_details.fill_Data(d1)
    student_details.cellClicked.connect(student_item_clicked)
    dept_details.fill_Data(d2)
    dept_details.cellClicked.connect(dept_item_clicked)

    filter_line = QComboBox()

    keys = pd.Series(["Select all"]).append(d1['name']).append(d2['name'])
    keys = keys.drop_duplicates()
    for i in keys:
        filter_line.addItem(i)

    filter_line.currentTextChanged.connect(filter)

    # show details block starts
    # for left side
    left_name = QLabel("Name")
    left_name_value = QLabel()

    left_dept = QLabel("Department")
    left_dept_value = QLabel()

    gBox = QGridLayout()

    gBox.addWidget(student_details, 0,0)
    gBox.addWidget(dept_details, 0,1)
    gBox.addWidget(filter_line, 1,0)
    gBox.addWidget(left_name, 2,0)
    gBox.addWidget(left_name_value, 2,1)
    gBox.addWidget(left_dept, 3,0)
    gBox.addWidget(left_dept_value, 3,1)


    main.setLayout(gBox)

    main.show()

    sys.exit(app.exec_())
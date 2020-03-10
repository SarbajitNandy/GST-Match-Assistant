from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QApplication, QHBoxLayout, QMainWindow, \
    QPushButton, QVBoxLayout, QComboBox, QGridLayout, QLabel, QWidget
import pandas as pd
import sys
from Scripts.GUI.ShowDetailsWidget import show_details
from Scripts.GUI.tableWidget import table_widget


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
        self.write_cols = [
            'GSTNo.', "Invoice", "Company", "TaxableValue", "cgst", 'sgst', 'igst'
        ]

        self.match_store : pd.DataFrame = pd.DataFrame();

        self.init_ui()

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
        print(data)
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

    def match_work(self):
        if not (self.selected_mySide.empty or self.selected_otherSide.empty):
            print("inside match_work")
            try:
                data = self.selected_mySide.append(self.selected_otherSide).drop_duplicates()
                print(data)
                self.match_store = self.match_store.append(pd.DataFrame(data))
                print(self.match_store)

                # Make selected data Null
                self.selected_mySide=self.selected_otherSide=pd.Series(dtype=float)
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
        else:
            pass

    def init_ui(self):

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

        gBox = QGridLayout()

        gBox.addWidget(self.filter_line, 0, 1)
        gBox.addWidget(self.mySide, 1, 0)
        gBox.addWidget(self.otherSide, 1, 2)
        gBox.addWidget(self.left_side, 2, 0)
        gBox.addWidget(self.match_btn, 2,1)
        gBox.addWidget(self.right_side, 2, 2)

        self.setLayout(gBox)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = do_match_gui()

    file = pd.ExcelFile('E:\\Programs\\Py\\TallyProject\media\\testSet5\\mergedFile.xlsx')

    mySide_data = pd.read_excel(file, sheet_name='My Side')
    otherSide_data = pd.read_excel(file, sheet_name='GST portal')
    if main.load_data(mySide_data, otherSide_data):
        main.fill_data()

    main.show()

    sys.exit(app.exec_())

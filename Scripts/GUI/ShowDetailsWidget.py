from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem,  QApplication, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QGridLayout, QLabel, QWidget, QSizePolicy
from PyQt5.QtCore import QRect
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


# if __name__ == "__main__" :
#     app = QApplication(sys.argv)
#     main = QDialog()
#     main.setGeometry(QRect(100, 100, 400, 400))
#
#     det = show_details(main)
#
#     d = {
#         'GSTNo.': "123",
#         'Invoice': "sad",
#         'Company': "ABCDEFGHI",
#         'TaxableValue': "123",
#         'cgst': "12",
#         'sgst': "23",
#         'igst': "34"
#     }
#
#     det.set_data(d)
#
#     main.show()
#
#     sys.exit(app.exec_())
import pandas as pd
import re

from src.main.exception.HandleException import MsgException

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

        logging.info("Convertion to float process on Purchase side Column:{} succeed".format(str(purchaseSideCols)))

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

        logging.info("Convertion to float process on Sales side Column:{} succeed".format(str(salesSideCols)))

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
            logging.info("Output file path : "+self.outFilePath)
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

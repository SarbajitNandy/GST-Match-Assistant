import pandas as pd
import re
import time

from Scripts.Exceptions import *;

class Purchase_Sales_Match(object):
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

        self.myExcel: pd.ExcelFile = None
        self.givenExcel: pd.ExcelFile = None

        self.myVouchar: pd.DataFrame = None
        self.givenVouchar: pd.DataFrame = None
        self.mergedData: pd.DataFrame = None
        self.notMatched_myside: pd.DataFrame = None
        self.notMatched_otherside: pd.DataFrame = None

        # columns values
        self.mycols =  ['Particulars', 'GSTIN/UIN', 'Invoice No.', 'Taxable Value', 'Integrated Tax Amount',
                          'Central Tax Amount', 'State Tax Amount', 'Total Tax Amount']
        self.gvcols =['GSTIN of supplier', 'Trade/Legal name of the Supplier','Invoice details Invoice number', 'Invoice details Invoice Value (₹)',
                          'Taxable Value (₹)', 'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)',
                          'Tax Amount State/UT tax (₹)']

    #     panda part
    @staticmethod
    def validation(n):
        return n and not (n == '')

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
            val = Purchase_Sales_Match.compiledExp.search('/' + str(i) + '/').group()
            r = re.search('\d+', val).group()
            return int(r)
        except:
            if i != 'nan':
                try:
                    r = re.search('\d+', i).group()
                    return int(r)
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

    def format_header(self):
        try:
            mv, gv = self.myVouchar.keys(), self.givenVouchar.keys()
            # print(mv)
            # print(gv)
            m = [self.join(i)
                 for i in mv]

            g = [self.join(i)
                 for i in gv]
            # print(m)
            # print(g)
            return (m, g)
        except:
            raise MsgException("Wrong Header format")

    def data_sanit(self):
        mvNew, gvNew = self.myVouchar.keys(), self.givenVouchar.keys()
        for i in mvNew:
            if i not in self.mycols:
                del self.myVouchar[i]

        for i in gvNew:
            if i not in self.gvcols:
                del self.givenVouchar[i]
        return


    def format_invoice(self):
        self.myVouchar["Invoice"] = [self.spl(i) for i in self.myVouchar["Invoice No."]]
        self.givenVouchar["Invoice"] = [self.spl(i) for i in self.givenVouchar["Invoice details Invoice number"]]
        return

    def match_work(self):
        count = 0
        matchresult = []
        data = self.mergedData
        notMatched_myside = {}
        notMatched_otherside = {}

        for i in self.mycols:
            notMatched_myside[i]=[]

        for i in self.gvcols:
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
            else:
                matchresult.append("NOT MATCHED")
                if int(gst1)==0 and int(igst1)==0 and int(cgst1)==0 and int(sgst1)==0:
                    for k in self.gvcols:
                        notMatched_otherside[k].append(j[k])
                elif int(gst2)==0 and int(igst2)==0 and int(cgst2)==0 and int(sgst2)==0:
                    for k in self.mycols:
                        notMatched_myside[k].append(j[k])

        data['Result'] = matchresult
        print("Found match in {0}/{1}".format(count, len(matchresult)))
        rate = count*100/len(matchresult)
        self.success_status("Matched: {}%".format(round(rate,2)))
        self.notMatched_myside = pd.DataFrame(notMatched_myside)
        self.notMatched_otherside = pd.DataFrame(notMatched_otherside)
        return






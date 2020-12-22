import pandas as pd
import re
import time
from random import random

# from Scripts.Exceptions import *;

class Purchase_Sales_Match(object):
    compiledExp = re.compile('/[A-Z]*[0-9]+[A-Z]*/')
    check = ["1920", '2020', '2019']

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
        self.MatchedDetails : pd.DataFrame = None
        self.notMatched_myside: pd.DataFrame = None
        self.notMatched_otherside: pd.DataFrame = None

        # columns values
        self.mycols =  ['Particulars', 'GSTIN/UIN', 'Invoice No.', 'Taxable Value', 'Integrated Tax Amount',
                          'Central Tax Amount', 'State Tax Amount', 'Total Tax Amount']
        self.gvcols =['GSTIN of supplier', 'Trade/Legal name of the Supplier','Invoice details Invoice number', 'Invoice details Invoice Value (₹)',
                          'Taxable Value (₹)', 'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)',
                          'Tax Amount State/UT tax (₹)']
        # success signals
        self.Done_with_match: bool = False


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
    def makeInt(n):

        def sanit(x):
            inter = re.search("\d+", x[1:-1]).group()
            for i in Purchase_Sales_Match.check:
                if (i in inter):
                    return 0
            return int(inter)

        return list(map(sanit, n))

    # @staticmethod
    # def spl(i):
    #     i = str(i)
    #     if ("/" not in i):
    #         return i
    #     try:
    #         j = i.replace('/', "//")
    #         j = "/{}/".format(j)
    #         print(j)
    #         val = Purchase_Sales_Match.compiledExp.findall(j)
    #         if (len(val) == 0):
    #             raise ValueError
    #         ret = max(Purchase_Sales_Match.makeInt(val))
    #         return str(ret)
    #     except:
    #         if i!='nan':
    #             try:
    #                 val = re.findall('\d+', i)
    #                 return str(max(list(map(int, val))))
    #             except:
    #                 return i
    #         return  i

    @staticmethod
    def spl(i):
        i = str(i)
        return ''.join(re.findall('\d+', i))



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
        matching_excel = {}

        # self.myVouchar["Invoice"] = [self.spl(i) for i in self.myVouchar["Invoice No."]]
        # self.givenVouchar["Invoice"] = [self.spl(i) for i in self.givenVouchar["Invoice details Invoice number"]]


        self.myVouchar["Invoice"] = self.myVouchar["Invoice No."].copy()
        self.givenVouchar["Invoice"] = self.givenVouchar["Invoice details Invoice number"].copy()

        matching_excel['Invoice']  = self.myVouchar["Invoice No."].append(self.givenVouchar["Invoice details Invoice number"])
        matching_excel['Sanitized Data'] = self.myVouchar["Invoice"].append(self.givenVouchar["Invoice"])

        # outFileWriter = pd.ExcelWriter("D:\Programs\Py\TallyProject\media\Log_report.xlsx", engine='xlsxwriter')
        self.match_report = pd.DataFrame(matching_excel)
        return

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
        print("editing GST no")
        mycols[1] = gvcols[0] = "GSTno."
        print("editing done")

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
                # if int(gst1)==0 and int(igst1)==0 and int(cgst1)==0 and int(sgst1)==0:
                #     for k in gvcols:
                #         notMatched_otherside[k].append(j[k])
                # elif int(gst2)==0 and int(igst2)==0 and int(cgst2)==0 and int(sgst2)==0:
                #     for k in mycols:
                #         notMatched_myside[k].append(j[k])

                for k in gvcols:
                    notMatched_otherside[k].append(j[k])

                for k in mycols:
                    notMatched_myside[k].append(j[k])


        data['Result'] = matchresult
        print("Found match in {0}/{1}".format(count, len(matchresult)))
        rate = count*100/len(matchresult)
        print("Matched: {}%".format(round(rate,2)))
        self.MatchedDetails = pd.DataFrame(MatchedDetails)
        self.notMatched_myside = pd.DataFrame(notMatched_myside)
        self.notMatched_otherside = pd.DataFrame(notMatched_otherside)
        self.Done_with_match = True
        return

    def main(self):
        start = time.time()
        self.Done_with_match = False
        try:
            # mycols, gvcols = None, None
            if self.myExcel:
                self.myVouchar = pd.read_excel(self.myExcel, self.file1Sheet, header=self.file1Header)
                # self.success_status("file read successful, format OK")
            else:
                # raise exception
                raise ExcelReadException(self.file1Path)


            if self.givenExcel:
                self.givenVouchar = pd.read_excel(self.givenExcel, self.file2Sheet, header=self.file2Header)
                # self.success_status("file read successful, format OK")
            else:
                #raise exception
                raise ExcelReadException(self.file2Path)

            if self.myExcel and self.givenExcel:
                # self.normal_status("formatting columns")
                self.myVouchar.columns, self.givenVouchar.columns = self.format_header()
                # self.success_status("Done")

                # Sanitary check of data
                # self.normal_status("Sanitizing Data")
                self.data_sanit()
                # self.success_status("Done")

                #  format invoice
                # self.normal_status("formatting invoice")
                self.format_invoice()
                # self.success_status("Done")

                #  check columns
                # self.normal_status("checking columns")
                self.myVouchar.rename(columns={'GSTIN/UIN': 'GSTno.'}, inplace=True)
                self.givenVouchar.rename(columns={'GSTIN of supplier': 'GSTno.'}, inplace=True)
                # self.mycols[1] = self.gvcols[0] = "GSTno."
                # self.success_status("Done")

                #  data join
                # self.normal_status("merging two files")
                self.mergedData = pd.merge(self.myVouchar, self.givenVouchar, on=['GSTno.', 'Invoice'], how='inner').fillna(0)
                # self.success_status("Done")

                # match
                # self.normal_status("finding for match")
                self.match_work()
                # self.success_status("Done")

                # # Creating excel writer
                # outFileWriter = pd.ExcelWriter(self.outFilePath, engine='xlsxwriter')
                #
                # # write into a file
                # # self.normal_status("Creating output file")
                # self.mergedData.to_excel(outFileWriter, sheet_name='All Data')
                # self.MatchedDetails.to_excel(outFileWriter, sheet_name="Matched Data")
                # self.notMatched_myside.to_excel(outFileWriter, sheet_name="My Side")
                # self.notMatched_otherside.to_excel(outFileWriter, sheet_name="GST portal")
                # outFileWriter.save()
                self.write_Result_to_excel()

                # self.success_status("Done")
                # self.success_status("output file path {} ".format(self.outFilePath))

        except Exception as e:
            print(str(e))
            # self.failure_status(str(e))
            # self.failure_status("Main Process failed")
        print("Process finished in : {0} secs".format(round(time.time() - start), 3))


    def write_Result_to_excel(self):
        # Creating excel writer
        if self.Done_with_match:
            print("Writting results")
            outFileWriter = pd.ExcelWriter(self.outFilePath, engine='xlsxwriter')

            # write into a file
            # self.normal_status("Creating output file")
            self.mergedData.to_excel(outFileWriter, sheet_name='All Data')
            self.MatchedDetails.to_excel(outFileWriter, sheet_name="Matched Data")
            self.notMatched_myside.to_excel(outFileWriter, sheet_name="My Side")
            self.notMatched_otherside.to_excel(outFileWriter, sheet_name="GST portal")
            self.match_report.to_excel(outFileWriter, sheet_name="Sanit of Invoice Report")
            outFileWriter.save()
            print("DONE")

        else:
            print("Writter is not ready")
            
    def read_file1(self):
        # self.file1SheetName.clear()
        try:
            # print("reading " + self.file1Path)
            file1 = pd.ExcelFile(self.file1Path)
            # for i in file1.sheet_names:
            #     self.file1SheetName.addItem(i)
            # self.success_status("{} file is OK".format(self.file1Path))
            return file1
        except Exception as e:
            # self.failure_status(str(e))
            self.file1Path=None
            # self.lineFile1.clear()
            # self.file1SheetName.clear()
            return None

    def read_file2(self):
        # self.file2SheetName.clear()

        try:
            # print("reading " + self.file2Path)
            file2 = pd.ExcelFile(self.file2Path)
            # for i in file2.sheet_names:
            #     self.file2SheetName.addItem(i)
            # self.success_status("{} file is OK".format(self.file2Path))
            return file2
        except Exception as e:
            # self.failure_status(str(e))
            self.file2Path = None
            # self.lineFile2.clear()
            # self.file2SheetName.clear()
            return None

            
if __name__ == '__main__':
    wr = Purchase_Sales_Match()
    
    wr.file1Path = "D:\Programs\Py\TallyProject\media\testSet4\PURCHASE_UPTO_SEP'2019.xls"
    wr.file1Sheet = "Vouchar Register"
    wr.file1Header = [8,9]
    
    wr.file2Path = "D:\Programs\Py\TallyProject\media\testSet4\Summary_GSTR-2A_UPTO SEP'2019.xlsx"
    wr.file2Sheet = "B2B"
    wr.file2Header = [4,5]
    
    wr.outFilePath = '/'.join(wr.file1Path.split("/")[0:-1]) +'/mergedFile.xlsx'
    
    wr.myExcel = wr.read_file1()
    wr.givenExcel = wr.read_file2()
    
    wr.main()
    
    





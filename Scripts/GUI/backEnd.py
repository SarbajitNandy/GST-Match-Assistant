import pandas as pd
import re
import time

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

    #     panda part
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




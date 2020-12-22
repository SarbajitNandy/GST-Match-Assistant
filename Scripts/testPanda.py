import pandas as pd
import re
import time

def join(i):
    si = list(i)
    if len(si)>=2:
        for j in range(len(si)):
            if ('Unnamed' in si[j]):
                del si[j]
        
    return " ".join(si)

def spl(i):
    i=str(i)
    try:
        val = compiledExp.search('/'+str(i)+'/').group()
        return re.search('\d+', val).group()
    except:
        if i!='nan':
            return re.search('\d+', i).group()
        return i
    
def format_invoice():
    myVouchar["Invoice"] = [ spl(i) for i in myVouchar["Invoice No."]]
    givenVouchar["Invoice"] =[ spl(i) for i in givenVouchar["Invoice details Invoice number"]]
    return 


def data_sanit():
    mvNew, gvNew = myVouchar.keys(), givenVouchar.keys()    
    for i in mvNew:
        if i not in mycols:
            del myVouchar[i]
            
    for i in gvNew:
        if i not in gvcols:
            del givenVouchar[i]
    
    return 

def format_header():
    mv, gv = myVouchar.keys(), givenVouchar.keys()
    m = [  join(i)
         for i in mv]

    g = [  join(i)
         for i in gv]
    return (m,g)


def float_compare(a,b):
    a,b=round(float(a)),round(float(b))
    if a==b:
        return True
    else:
        if abs(a-b)<=1:
            return True
        else:
            return False

def match_work(data):
    count = 0
    matchresult= []
    for i, j in data.iterrows():
        r:bool = True
        gst1, gst2=j['Taxable Value'],j['Taxable Value (₹)']
        igst1, igst2 = j['Integrated Tax Amount'], j['Tax Amount Integrated Tax  (₹)']
        cgst1, cgst2 = j['Central Tax Amount'],j['Tax Amount Central Tax (₹)']
        sgst1, sgst2 = j['State Tax Amount'], j['Tax Amount State/UT tax (₹)']
        
        if not float_compare(gst1, gst2):
            r = False
        if not float_compare(igst1, igst2):
            r = False
        if not float_compare(sgst1, sgst2):
            r = False
        if not float_compare(cgst1, cgst2):
            r = False
        if r:
            count += 1
            matchresult.append("MATCHED")
        else:
            matchresult.append("NOT MATCHED")
      
    data['Result'] = matchresult
    print("Found match in {0}/{1}".format(count,len(matchresult)))
    return 

    

if __name__ == "__main__":
    start = time.time()
    exp = '/[A-Z]?[0-9]+/'
    compiledExp = re.compile(exp)

    myExcel = "D:\Programs\Py\TallyProject\media\PURCHASE_QE DEC'2019.xls"
    gstExcel = "D:\Programs\Py\TallyProject\media\SUMMARY OF GSTR-2A_QE DEC'2019.xlsx"

    with pd.ExcelFile(myExcel) as x1:
        mycols = ['Particulars','GSTIN/UIN', 'Invoice No.', 'Taxable Value', 'Integrated Tax Amount', 'Central Tax Amount', 'State Tax Amount', 'Total Tax Amount']
        myVouchar = pd.read_excel(x1, 'Voucher Register', header=[0,1], skipfooter=3)

    with pd.ExcelFile(gstExcel) as x2:
        gvcols = ['GSTIN of supplier', 'Invoice details Invoice number', 'Invoice details Invoice Value (₹)', 'Taxable Value (₹)', 'Tax Amount Integrated Tax  (₹)', 'Tax Amount Central Tax (₹)', 'Tax Amount State/UT tax (₹)']
        givenVouchar = pd.read_excel(x2, 'Sheet1', header=[4, 5], skipfooter=2)
    myVouchar.columns, givenVouchar.columns = format_header()
    # Sanitary check of data
    data_sanit()

    #  format invoice
    format_invoice()

    #  check columns
    myVouchar.rename(columns={'GSTIN/UIN':'GSTno.'}, inplace=True)
    givenVouchar.rename(columns={'GSTIN of supplier':'GSTno.'}, inplace=True)

    #  data join
    newFile = pd.merge(myVouchar, givenVouchar, on=['GSTno.', 'Invoice'], how='outer').fillna(0)

    # match
    match_work(newFile)
    # write into a file
    newFile.to_excel("newFile.xlsx", sheet_name='Sheet1', engine='xlsxwriter')

    print("Process finished in : {0} secs".format(round(time.time()-start),3))
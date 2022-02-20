from unicodedata import name
import xlrd

def open_excel(path):
    try:
        # book = xlrd.open_workbook("C:\\Users\\D\\Desktop\\木工库\\物料名.xlsx")  #文件名，把文件与py文件放在同一目录下
        # book = xlrd.open_workbook(r'D:\mugongData\南侧雕刻机计划表.xlsx')
        book = xlrd.open_workbook(path)
    except:
        print("open excel file failed!")
    try:
        name=path.split("\\")[-1]
        fileName=name.split(".")[0]
        sheet = book.sheet_by_name(fileName)   #execl里面的worksheet1
        return sheet
    except:
        print("locate worksheet in excel failed!")



    
if __name__=="__main__":  

#    a=open_excel(r'C:\Users\DXHQXX\Documents\GitHub\Python\日常使用\1.xls')
   a = open_excel(r'日常使用\1.xls')
   b = open_excel(r'日常使用\2.xls')
   print(a)

from this import d
import pandas as pd

def open_excel(path,sheetname,datatype):
    try:
        # book = xlrd.open_workbook("C:\\Users\\D\\Desktop\\木工库\\物料名.xlsx")  #文件名，把文件与py文件放在同一目录下
        # book = xlrd.open_workbook(r'D:\mugongData\南侧雕刻机计划表.xlsx')
        book = pd.read_excel(path,sheet_name="汇总",dtype={datatype:str})
        return book
    except:
        print("open excel file failed!")
 



    
if __name__=="__main__":  

#    a=open_excel(r'C:\Users\DXHQXX\Documents\GitHub\Python\日常使用\1.xls')
   a = open_excel(r'日常使用\52893交割汇总.xlsx',"汇总",'证券代码')
   b = open_excel(r'日常使用\1540交割汇总.xlsx',"汇总",'证券代码')
#    rows0=a.col_values(0)
#    rows1=a.col_values(1)
#    rows=rows0+rows1
#    c=a.loc('成交日期')
   c=a[['成交日期','业务类型','证券代码','证券名称','成交价格','成交数量','成交金额',
   '发生金额','资金余额','当前持仓']]
   d=b[['交割日期','业务名称','证券代码','证券名称','成交价格','成交数量','成交金额',
   '发生金额','剩余金额','证券数量']]
   d.columns=['成交日期','业务类型','证券代码','证券名称','成交价格','成交数量','成交金额',
   '发生金额','资金余额','当前持仓']
   e=[c,d]
   
   df=pd.concat(e,axis=0,ignore_index = False, join = 'outer')
   
   df.sort_values(by='成交日期',axis=0,inplace=True,)
   # print(df)
   df.to_excel('result.xlsx', index=False)

import pymysql
import xlrd
import xlwt
from datetime import date, datetime


title =datetime.now().strftime("%Y%m%d") + '加工记录.xls'
year=datetime.now().strftime("%Y")
month =datetime.now().strftime("%m")
month=format(int(month)) 
day=datetime.now().strftime("%d")
day=format(int(day))
def creat_excel(result):
    f = xlwt.Workbook() #创建表格
    sheet1 = f.add_sheet(title,cell_overwrite_ok=True)#创建sheet
    # 制作表头 
    sheet1.write(0,0,'取出库位')
    sheet1.write(0,1,'物料名称')
    sheet1.write(0,2,'厚度')
    sheet1.write(0,3,'取出日期')
    sheet1.write(0,4,'取出时间')
    sheet1.write(0,5,'操作员')
    i=0
    for row in result:   
        i+=1
        for j in range(0,6):
                sheet1.write(i,j,row[j])
            
    f.save("D:\\mugongData\\Log\\"+title)


def slect_deta():
    
    cursor = db.cursor()
    sql = "SELECT * FROM guige.wcsreport where 取出日期="+"'"+year+"/"+month+"/"+day+"'"
    
    cursor.execute(sql)  # 执行sql语句"SLECT * FROM guige.wcsreport"
    result = cursor.fetchall()
    cursor.close()  # 关闭连接
    # try:
    #     cursor.execute("""SLECT * FROM guige.wcsreport""")  # 执行sql语句
    #     result = cursor.fetchall()
    # except:
    #     print ("Error: unable to fetch data")
    
    return result

    
 
 # 连接数据库
try:
    db = pymysql.connect(host="127.0.0.1", user="root",
                         passwd="123456",
                         db="mysql",
                         charset='utf8')
except:
    print("could not connect to mysql server")
 
# open_excel()  
# insert_deta()
# creat_excel()
result=slect_deta()

creat_excel(result)
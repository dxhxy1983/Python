import pymysql
import xlrd
 
 


 
def open_excel():
    try:
        # book = xlrd.open_workbook("C:\\Users\\D\\Desktop\\木工库\\物料名.xlsx")  #文件名，把文件与py文件放在同一目录下
        book = xlrd.open_workbook(r'D:\mugongData\北侧雕刻机计划表.xlsx')
    except:
        print("open excel file failed!")
    try:
        sheet = book.sheet_by_name("北侧雕刻机计划表")   #execl里面的worksheet1
        return sheet
    except:
        print("locate worksheet in excel failed!")
 
 
def insert_deta():
    sheet = open_excel()
    cursor = db.cursor()
    row_num = sheet.nrows
    for i in range(1, row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
        row_data = sheet.row_values(i)
        value = (str(row_data[0]),str(row_data[1]),row_data[2],row_data[3],'0')
        
        sql = "INSERT INTO guige.plan2 VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(sql, value)  # 执行sql语句
        db.commit()
        # print('插入{0}条记录完成',i)
    cursor.close()  # 关闭连接
 
 # 连接数据库
try:
    db = pymysql.connect(host="127.0.0.1", user="root",
                         passwd="123456",
                         db="mysql",
                         charset='utf8')
except:
    print("could not connect to mysql server")
 
# open_excel()  
insert_deta()
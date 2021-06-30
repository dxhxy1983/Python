import pymysql
# import xlrd
from datetime import date, datetime
import random
numOfWCS=6

def datestmp():

    seed=random.random()
    date =datetime.now().strftime("%Y%m%d%H%M%S")
    datestmp=date+str(seed)
    datestmp=datestmp[2:15]+datestmp[16:20] 
    return datestmp

 
def insert_data(value):
    
    cursor = db.cursor()   
    # value = (4,1,str("比吗"),1,12,str("反面朝上"),0,str(datestmp))
        
    sql = "INSERT INTO guige.plan3 VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, value)  # 执行sql语句
    db.commit()
        # print('插入{0}条记录完成',i)
    cursor.close()  # 关闭连接
def dsp_data():
    cursor = db.cursor()
    sql = "SELECT * FROM guige.wcsinfo ORDER BY 库位号"
    cursor.execute(sql)  # 执行sql语句"SLECT * FROM guige.wcsreport"
    result = cursor.fetchall()
    print("库位号 物料名称   数量  厚度    物料状态")
    print_data(result)

def print_data(result):    
    for item in result:
        print("=======================================")
        item=list(item)
        for i in range(len(item)-1):
            if i==1 and len(list(item[i]))<8 :
                print(item[i], end='')
                for i in range(5-len(list(item[i]))):
                    print("  ",end='')

            else:
                print(item[i], end='\t')
        print(item[-1])
def enter_data():
    s = input("请输入需要的物料所属库位号并回车确认：") 
    try: 
        if complex(s) == complex(eval(s)):
            if slect_data(eval(s)) != None:
                print("选择的库位信息如下，机器人将在下次任务中执行")
                print_data(slect_data(eval(s)))
                return slect_data(eval(s))
            else:
                print("未查到相关库位数据，请检查输入")
    except:

        print("输入有误")
    
def slect_data(numOfWCS):
    try:
        num=int(numOfWCS)
    except:
        pass
    num=str(num)
    cursor = db.cursor()
    # sql = "SELECT * FROM guige.wcsreport where 取出日期="+"'"+year+"/"+month+"/"+day+"'"
    sql = "SELECT * FROM guige.wcsinfo where 库位号="+num
    
    cursor.execute(sql)  # 执行sql语句"SLECT * FROM guige.wcsreport"
    result = cursor.fetchall()
    # print(result)
    
    cursor.close()  # 关闭连接
    return result
 # 连接数据库
try:
    db = pymysql.connect(host="192.168.0.141", user="win7",
                         passwd="123456",
                         db="mysql",
                         charset='utf8')
except:
    print("could not connect to mysql server")
 
  
if __name__=="__main__":
    dsp_data()
    result=enter_data()

    datestmp=datestmp()
    # result=slect_data(numOfWCS)
    # # value = (4,1,str("比吗"),1,12,str("反面朝上"),0,str(datestmp))
    result=list(result[0])
    value=(result[0],1,result[1],1,result[3],result[4],0,str(datestmp)) 
    # print(value)
    insert_data(value)
   


# from SQL.manualPlan import dsp_data
# from SQL.manualPlan import datestmp
import os
import time
# import PyQt5.sip
from PySide2.QtWidgets import QApplication,QMainWindow
import sys
sys.path.append('C:\\Users\\D\\Documents\\Python\\PYqt5')
from mugong import Ui_ClickandComfort
import pymysql
from datetime import date, datetime
import random
IPhost=""
username="root"
wcsinfo="wcsinfo"
auto_info="plan1"
manul_info="plan3"
parametersList=[IPhost,username,wcsinfo,auto_info,manul_info]
# print(parametersList) 
# print(parametersList)
# abs_path=os.path.dirname(os.path.abspath(__file__))
# print(abs_path)
# file_path=abs_path+'\\settings.txt'
file_path='d:\\mugongData\\settings.txt'
with open(file_path,'r') as f:
    i=0
    for line in f:
        line=line.strip('\n')
        # print(line)
        kye,value=line.split(":")
        parametersList[i]=value
        i+=1
print(parametersList)    
IPhost=parametersList[0]
username=parametersList[1]
wcsinfo=parametersList[2]
auto_info=parametersList[3]
manul_info=str(parametersList[4])

class MainWindow(QMainWindow):

    # 连接数据库
    try:
        # db = pymysql.connect(host="192.168.0.141", user="win7",
        db = pymysql.connect(host=IPhost, user=username,
                            passwd="123456",
                            db="mysql",
                            charset='utf8')
    except:
        print("could not connect to mysql server")
    
    def datestmp(self):

        seed=random.random()
        date =datetime.now().strftime("%Y%m%d%H%M%S")
        datestmp=date+str(seed)
        datestmp=datestmp[2:15]+datestmp[16:20] 
        return datestmp

 
    def insert_data(self,dst:str,value):
        
        cursor = self.db.cursor()   
        # value = (4,1,str("比吗"),1,12,str("反面朝上"),0,str(datestmp))
            
        sql = "INSERT INTO guige."+dst+" VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, value)  # 执行sql语句
        self.db.commit()
            # print('插入{0}条记录完成',i)
        cursor.close()  # 关闭连接
    def dsp_data(self,dst:str,oder:str):
        cursor = self.db.cursor()
        sql = "SELECT * FROM guige."+dst+" ORDER BY "+oder
        cursor.execute(sql)  # 执行sql语句"SLECT * FROM guige.wcsreport"
        result = cursor.fetchall()
        # print("库位号 物料名称   数量  厚度    物料状态")
        
        return self.print_data(result)


    
    def print_data(self,result):
        l=""    
        for item in result:
            # print("=======================================")
            l=l+"==========================================================\n"
            item=list(item)
            # print(item)
            for i in range(len(item)-1):
                if isinstance(item[i],str) and len(item[i])<4:
                    # print(f"{item[i]}",end="\t\t")
                    l=l+item[i]+"\t\t"
                else :
                    # print(f"{item[i]}",end="\t")
                    l=l+str(item[i])+"\t"


            l=l+str(item[-1]) +"\n"   
            
        return l

        
    def slect_data(self,numOfWCS):
        try:
            num=int(numOfWCS)
        except:
            pass
        num=str(num)
        cursor = self.db.cursor()
        # sql = "SELECT * FROM guige.wcsreport where 取出日期="+"'"+year+"/"+month+"/"+day+"'"
        sql = "SELECT * FROM guige.wcsinfo where 库位号="+num
        
        cursor.execute(sql)  # 执行sql语句"SLECT * FROM guige.wcsreport"
        result = cursor.fetchall()
        # print(result)
        
        cursor.close()  # 关闭连接
        return result
    kuwei=[]
    num=0
    
    def btn1_clicked(self):
        result=self.slect_data(1)        
        self.ui.TextLable2.setText(str(self.print_data(result)))
        self.num=1
        self.kuwei=list(result[0])
    def btn2_clicked(self):
        result=self.slect_data(2)        
        self.ui.TextLable2.setText(str(self.print_data(result)))
        self.num=2
        self.kuwei=list(result[0])
    def btn3_clicked(self):
        result=self.slect_data(3)        
        self.ui.TextLable2.setText(str(self.print_data(result)))
        self.num=3
        self.kuwei=list(result[0])
    def btn4_clicked(self):
        result=self.slect_data(4)        
        self.ui.TextLable2.setText(str(self.print_data(result)))
        self.num=4
        self.kuwei=list(result[0])
    def btn5_clicked(self):
        result=self.slect_data(5)        
        self.ui.TextLable2.setText(str(self.print_data(result))) 
        self.num=5
        self.kuwei=list(result[0])  
    def btn6_clicked(self):
        result=self.slect_data(6)        
        self.ui.TextLable2.setText(str(self.print_data(result)))
        self.num=6
        self.kuwei=list(result[0])
    def btn7_clicked(self):
        result=self.slect_data(7)        
        self.ui.TextLable2.setText(str(self.print_data(result)))
        self.num=7
        self.kuwei=list(result[0])
    def btn8_clicked(self):
        result=self.slect_data(8)        
        self.ui.TextLable2.setText(str(self.print_data(result)))
        self.num=8
        self.kuwei=list(result[0])  
    def btn9_clicked(self):
        result=self.slect_data(9)        
        self.ui.TextLable2.setText(str(self.print_data(result)))
        self.num=9
        self.kuwei=list(result[0])
    def btn10_clicked(self):
        result=self.slect_data(10)        
        self.ui.TextLable2.setText(str(self.print_data(result)))
        self.num=10
        self.kuwei=list(result[0])
    def btn11_clicked(self):
        result=self.slect_data(11)        
        self.ui.TextLable2.setText(str(self.print_data(result))) 
        self.num=11
        self.kuwei=list(result[0])
    def btn12_clicked(self):
        result=self.slect_data(12)        
        self.ui.TextLable2.setText(str(self.print_data(result))) 
        self.num=12
        self.kuwei=list(result[0])
    def btnconfirm_clicked(self):
        datestmp=self.datestmp()
             
        # print(self.kuwei)
        result=self.kuwei

        # result=list(result[0])
        if auto_info=="plan1":
            value=(result[0],1,result[1],1,result[3],result[4],0,str(datestmp))
            
        else:
            value=(result[0],2,result[1],1,result[3],result[4],0,str(datestmp))
        self.insert_data(manul_info,value)  
        self.ui.pushButton_confirm.setEnabled(False)
        
        
        self.ui.lab_manul.setText(self.dsp_data(manul_info,"时间戳"))
        self.ui.pushButton_confirm.setEnabled(True)
        # self.close()

    def btn14_clicked(self):
        # print("14btn")
        return self.dsp_data(wcsinfo,'库位号')
        # self.ui.TextLable1.setText("")
        self.ui.TextLable1.setText(str(self.dsp_data()))
    
    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_ClickandComfort()
        # 初始化界面
        self.ui.setupUi(self)

      
        self.ui.pushButton_1.clicked.connect(self.btn1_clicked)
        self.ui.pushButton_2.clicked.connect(self.btn2_clicked)
        self.ui.pushButton_3.clicked.connect(self.btn3_clicked)
        self.ui.pushButton_4.clicked.connect(self.btn4_clicked)
        self.ui.pushButton_5.clicked.connect(self.btn5_clicked)
        self.ui.pushButton_6.clicked.connect(self.btn6_clicked)
        self.ui.pushButton_7.clicked.connect(self.btn7_clicked)
        self.ui.pushButton_8.clicked.connect(self.btn8_clicked)
        self.ui.pushButton_9.clicked.connect(self.btn9_clicked)
        self.ui.pushButton_10.clicked.connect(self.btn10_clicked)
        self.ui.pushButton_11.clicked.connect(self.btn11_clicked)
        self.ui.pushButton_12.clicked.connect(self.btn12_clicked)
        # self.ui.pushButton_refresh.clicked.connect(self.btn14_clicked)
        self.ui.TextLable1.setText(str(self.btn14_clicked()))
        self.ui.lab_auto.setText(self.dsp_data(auto_info,'物料名称'))
        self.ui.lab_manul.setText(self.dsp_data(manul_info,"时间戳"))
        self.ui.pushButton_confirm.clicked.connect(self.btnconfirm_clicked)
        

    
        


     
    
if __name__=="__main__":  

    app = QApplication([])
    mainw = MainWindow()
    mainw.show()
    app.exec_()







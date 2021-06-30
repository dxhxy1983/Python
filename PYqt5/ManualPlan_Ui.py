

# from SQL.manualPlan import dsp_data
# from SQL.manualPlan import datestmp
from PySide2.QtWidgets import QApplication,QMainWindow
from mugong import Ui_ClickandComfort
import pymysql
from datetime import date, datetime
import random


class MainWindow(QMainWindow):

    # 连接数据库
    try:
        # db = pymysql.connect(host="192.168.0.141", user="win7",
        db = pymysql.connect(host="127.0.0.1", user="root",
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

 
    def insert_data(self,value):
        
        cursor = self.db.cursor()   
        # value = (4,1,str("比吗"),1,12,str("反面朝上"),0,str(datestmp))
            
        sql = "INSERT INTO guige.plan3 VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, value)  # 执行sql语句
        self.db.commit()
            # print('插入{0}条记录完成',i)
        cursor.close()  # 关闭连接
    def dsp_data(self):
        cursor = self.db.cursor()
        sql = "SELECT * FROM guige.wcsinfo ORDER BY 库位号"
        cursor.execute(sql)  # 执行sql语句"SLECT * FROM guige.wcsreport"
        result = cursor.fetchall()
        # print("库位号 物料名称   数量  厚度    物料状态")
        
        return self.print_data(result)


    
    def print_data(self,result):
        l="库位号 物料名称   数量  厚度    物料状态\n"    
        for item in result:
            # print("=======================================")
            l=l+"====================================================\n"
            item=list(item)
            for i in range(len(item)-1):
                if i==1 and len(list(item[i]))<8 :
                    # print(item[i], end='')
                    l=l+str(item[i])
                    for i in range(6-len(list(item[i]))):
                        # print("  ",end='')
                        l=l+"  "

                else:
                    # print(item[i], end='\t')
                    l=l+str(item[i])+"\t"
            # print(item[-1])
            l=l+str(item[-1])+"\n"
        return l

    # def enter_data():
    #     s = input("请输入需要的物料所属库位号并回车确认：") 
    #     try: 
    #         if complex(s) == complex(eval(s)):
    #             if slect_data(eval(s)) != None:
    #                 print("选择的库位信息如下，机器人将在下次任务中执行")
    #                 print_data(slect_data(eval(s)))
    #                 return slect_data(eval(s))
    #             else:
    #                 print("未查到相关库位数据，请检查输入")
    #     except:

    #         print("输入有误")
        
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
        value=(result[0],1,result[1],1,result[3],result[4],0,str(datestmp))
        self.insert_data(value)  
        self.close()

    def btn14_clicked(self):
        # print("14btn")
        return self.dsp_data()
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
        self.ui.pushButton_confirm.clicked.connect(self.btnconfirm_clicked)
        

    
        


     
    
   

app = QApplication([])
mainw = MainWindow()
mainw.show()
app.exec_()







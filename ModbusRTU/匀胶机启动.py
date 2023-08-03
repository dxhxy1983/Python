# -*- coding: utf_8 -*-


import serial
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import time
import sys
import os


def mod(PORT,address,FucNum,start_add,num,outputvalue=0):
    red = []
    alarm = ""
    try:
        # 设定串口为从站
        master = modbus_rtu.RtuMaster(serial.Serial(port=PORT,
                                                    baudrate=9600, bytesize=8, parity='N', stopbits=1))
        master.set_timeout(0.5)
        master.set_verbose(True)

        # 读保持寄存器                 功能码    起始地址      寄存器数量  设定值
        red = master.execute(address, FucNum, start_add,         num,  outputvalue)  # 这里可以修改需要读取的功能码
        # print(red)
        # red = master.execute(2, cst.READ_COILS, 0, 2)
        # print(red)
        alarm = "正常"
        return list(red), alarm

    except Exception as exc:
        print(str(exc))
        alarm = (str(exc))

    return red, alarm  ##如果异常就返回[],故障信息


if __name__ == "__main__":
    current_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    file_path=current_path+"\\settings.txt"
    parametersList=[]
    
    with open(file_path,'r',encoding="utf-8") as f:
        i=0
        for line in f:
            line=line.strip('\n')
            # print(line)
            if line!="":
                key,value=line.split(":")
                parametersList.append(value)
    # print(parametersList)        
    num=0
    Port=parametersList[0]
    # print(Port)
    comAdd1=1 #匀胶协议板地址
    #设置工作模式为多步
    readStatus,alarm=mod(Port,comAdd1,FucNum=6,
                    start_add=258,num=1, #工作模式
                    outputvalue=2   #1：单步，2：多步，3：报错，0：系统参数
                    )
    #打开真空泵
    # comAdd2=3 #IO板地址
    # readDing,alarm=mod(Port,comAdd2,FucNum=5,
    #                 start_add=1,num=1, 
    #                 outputvalue=255   
    #                 )
    # print("真空泵状态:{0}",readDing)
    #启动打开定位销
    # readpump,alarm=mod(Port,comAdd2,FucNum=5,
    #                 start_add=0,num=1,
    #                 outputvalue=255)
    # print("定位销状态:{0}",readpump)
    #当定位销打开后启动电机                
    
    readRun,alarm=mod(Port,comAdd1,FucNum=6,
                    start_add=257,num=1, #工作模式
                    outputvalue=255   #0x00：停车，0xFF：启动
                    )
    # print(readRun)
    #启动完成,监控停止

    # while readRun[1]==255:
        
    #     # mod("com2",1,6,1,1,outputvalue=255)
        


    #     time.sleep(0.5)                         #
    #     readSpeed,alarm=mod(Port,comAdd1,3,     #01 05：运行状态：0：停止，1：运行中，2：处于停车过程中（只读）40262
    #                          258,              #01 06：当前转速（只读）40263
    #                          6)                #01 07：剩余时长（只读）40264
    #     # print(readSpeed)                                     
    #     if readSpeed[2]==5 and 10<readSpeed[4]<120:
    #         #复位定位销
    #         readDing,alarm=mod(Port,comAdd2,FucNum=5,
    #                 start_add=0,num=1, 
    #                 outputvalue=0   
    #                 )
    #         #停止真空泵
    #         readpump,alarm=mod(Port,comAdd2,FucNum=5,
    #                 start_add=1,num=1,
    #                 outputvalue=0)
    #         time.sleep(2)
    #         #停止电机
    #         readStop,alarm=mod(Port,comAdd1,FucNum=6,
    #                 start_add=257,num=1,
    #                 outputvalue=0)
    num=1
    #         break
        
    print(num)        
    # sys.exit(num)
        



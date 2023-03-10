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
        print(red)
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
      
    
    Port=parametersList[0]
    comAdd1=parametersList[1]
    FuckNum=parametersList[2]
    num=parametersList[3]
    # comAdd1=3 #IO板地址
    # #设置工作模式为单步
    # readStatus,alarm=mod(Port,comAdd1,FucNum=5,
    #                 start_add=0,num=1, #工作模式
    #                 outputvalue=1   #1：单步，2：多步，3：报错，0：系统参数
    #                 )
    # Port="com6"
    # comAdd1=5 #匀胶协议板地址

    #设置工作模式为单步
    readStatus,alarm=mod(Port,comAdd1,FucNum=FuckNum,
                    start_add=0,num=num, #工作模式
                    outputvalue=0   #1：单步，2：多步，3：报错，0：系统参数
                    )
        



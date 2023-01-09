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
      
    num=0
    Port=parametersList[0]
  
    comAdd1=1 #匀胶协议板地址
    #设置参数
    #设置第一组
    for i in range (0,12):
        address=4352+i
        parameterValue=parametersList[i+1]
        readParameter,alarm=mod(Port,comAdd1,FucNum=6,
                    start_add=address,num=1, #工作模式
                    outputvalue=int(parameterValue)
                    )
    #设置第二组
    for i in range(0,12):
        address=4608+i
        parameterValue=parametersList[i+1+12]
        readParameter,alarm=mod(Port,comAdd1,FucNum=6,
                    start_add=address,num=1, #工作模式
                    outputvalue=int(parameterValue)
                    )
    #设置第三组
    for i in range(0,12):
        address=4864+i
        parameterValue=parametersList[i+1+24]
        readParameter,alarm=mod(Port,comAdd1,FucNum=6,
                    start_add=address,num=1, #工作模式
                    outputvalue=int(parameterValue)
                    ) 
    #设置第四组
    for i in range(0,12):
        address=5120+i
        parameterValue=parametersList[i+1+36]
        readParameter,alarm=mod(Port,comAdd1,FucNum=6,
                    start_add=address,num=1, #工作模式
                    outputvalue=int(parameterValue)
                    ) 
    #设置第五组
    for i in range(0,12):
        address=5376+i
        parameterValue=parametersList[i+1+48]
        readParameter,alarm=mod(Port,comAdd1,FucNum=6,
                    start_add=address,num=1, #工作模式
                    outputvalue=int(parameterValue)
                    )                                 
    num=1
        
        
    print(num)        
   
        



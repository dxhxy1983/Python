

import pandas as pd
Data=pd.read_excel(r'PLC\PLCTags.xlsx',usecols=[3],names=None) #PLC的IO地址表
# d=Data.values.tolist()
len=Data.size

head=pd.read_excel(r'PLC\head.xlsx',usecols=[0],names=None ) #标签名表
# print(head.values())
for i in range(0,48):# 48是输入输出分界线
    m=Data.values[i,0]
    n=head.values[i,0]
    print('"IOs".激光桁架_7.I.{0}:={1};'.format(n,m))
for i in range(48,len):
    m=Data.values[i,0]
    n=head.values[i,0]
    print('{0}:="IOs".激光桁架_7.O.{1};'.format(m,n))





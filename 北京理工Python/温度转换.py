# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 19:22:12 2019

@author: D
"""
def main():
    temp=(input('请输入温度（带温标C/F）：'))
    print(temp[-1])
    if temp[-1] in ['f','F']:
        print("{:.2f}C".format((eval(temp[:-1])-32)/1.8))
    elif temp[-1] in [ 'c' , 'C']:
        c=eval(temp[:-1])*1.8+32
        print("{:.2f}F".format(c))
    else: 
       print('输入格式错误')
main()



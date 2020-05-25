# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import turtle as tl
def main():
    tl.title('数据动态路径绘制')
    tl.setup(800,600,0,0)
    pen=tl.Turtle()
    pen.color(0,1,0)
    pen.width(5)
    pen.shape('turtle')
    pen.speed(3)
    result=[]
    file=open("C:\\Users\\D\\Documents\\Python\\data.txt","r")
    for line in file:
        result.append(list(map(float,line.split(','))))
    print(result)
    for i in range(len(result)):
        pen.color((result[i][3],result[i][4],result[i][5]))
        pen.fd(result[i][0])
        if result[i][1]:
            pen.rt(result[i][2])
        else:
            pen.lt(result[i][2])
    pen.goto(0.0)

if __name__=='__main__':
    main()

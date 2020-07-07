# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 14:40:21 2019

@author: D
"""

from turtle import Turtle
p=Turtle()
p.speed(2)
p.pensize(5)
# p.color("black","yellow")
p.fillcolor("red")
p.begin_fill()
for i in range(5):
    p.forward(200)
    p.right(144)
p.end_fill

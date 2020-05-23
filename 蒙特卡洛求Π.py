from random import random
from time import perf_counter
random.seed(123)
darts=1000*1000*100
hits=0.0
start=perf_counter()
for i in range(0,darts):
    x,y=random(),random()
    dist=pow(x*x+y*y,0.5)
    if dist<=1.0:
        hits=hits+1
pi=4*(hits/darts)
print("圆周率值是:{}".format(pi))
print("运行时间是:{:.5f}s".format(perf_counter()-start))
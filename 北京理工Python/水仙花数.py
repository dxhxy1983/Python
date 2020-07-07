l=[]
for i in range(1000,10000):
    qianwei=i//1000
    baiwei=(i-qianwei*1000)//100
    shiwei=(i-qianwei*1000-baiwei*100)//10
    gewei=i-qianwei*1000-baiwei*100-shiwei*10
    if pow(qianwei,4)+pow(baiwei,4)+pow(shiwei,4)+pow(gewei,4)==i:
       l.append(str(i) )
for i in range(len(l)):
    if i<len(l)-1:
        print('{}'.format(l[i]),end=',')
    else:
        print(l[i],end='')
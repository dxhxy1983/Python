
priceA,coastA=eval(input('请输入A加油站挂牌油价,实付金额(逗号隔开)：'))
priceB,coastB=eval(input("请输入B加油站挂牌油价,实付金额(逗号隔开):"))
compereAB=(priceA*coastA)/(priceB*coastB)
print("{:.2f}".format(compereAB))
if compereAB<1:
    print('A油站便宜')
else:
    print("B油站便宜")
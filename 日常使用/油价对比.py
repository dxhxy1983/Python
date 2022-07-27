coastM=300
priceA,coastA=eval(input('请输入A加油站挂牌油价,实付金额(逗号隔开)：'))
priceB,coastB=eval(input("请输入B加油站挂牌油价,实付金额(逗号隔开):"))
litterA=coastM/priceA
litterB=coastM/priceB
litterCoastA=coastA/litterA
litterCoastB=coastB/litterB
compereAB=(priceA*coastA)/(priceB*coastB)
print("{:.2f}".format(compereAB))
print("A油站加油{0:.2f}升,实际单价{1:.2f}".format(litterA,litterCoastA))
print("B油站加油{0:.2f}升,实际单价{1:.2f}".format(litterB,litterCoastB))
if compereAB<1:
    print('A油站便宜')
else:
    print("B油站便宜")
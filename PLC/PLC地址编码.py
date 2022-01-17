# X=eval(input("请输入起始字节（例如：40.0请输入40）："))
# end=eval(input("请输入结束字节（例如：50.0请输入50）："))
# print("输入的起始字节是：",X)
# print("输入的结束字节是：",end)
X=20
moudul=4
for i in range(X,X+2*moudul):
    for j in range(0,8):
        print("Y{0}{1}".format(i,j))
        

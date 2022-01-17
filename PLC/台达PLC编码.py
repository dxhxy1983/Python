# 32位D寄存器编址
# for i in range(20000,21000):
#     if i%2==0:
#         print("D{0}".format(i))




#与机器人通信地址编址
for i in range(300,332):
    for j in range(0,16):
        # print("D"+'{0}'+"."+'{1}'.format(i,j))
        print("D{0}.{1}".format(i,j))
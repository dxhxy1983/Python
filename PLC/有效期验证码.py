

list=[31,61,127,241,487]
a=[]
c=0
# for i in range(10000,99999):
#     # for j in list:
#         b=(i*31+9973)%10000
#         if b>1000:
#             a.append(b)
# print(a)
# # for mod1 in a:
# #     for mod2 in a:
# #         for mod3 in a:
# #             for mod4 in a:


mod1=6308
shang=9
for i in range(0,10000):
        for j in list:
            b=i*int(j)+9973
            d=shang*10000+mod1
            if b==d:
                # print(mod,i,j)
                if j not in a:
                    a.append(j)
                    print(i,j)
                   
                # else:
                #     print("有重复")
                    
                #     print(mod,i,j)
                #     c=c+1
                    
# print(c)
print(a)




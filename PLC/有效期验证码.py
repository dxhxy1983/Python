list=[0,31,61,127,241,487]
for i in range(1,6):
 j=(i*list[i]*9973)%10000
 print(j)
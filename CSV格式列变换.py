f=open('data.csv').readlines()
# print(f)
for line in f:
    line=line.replace('\n','').split(',')
    # print(line)
    b=[]
    # for i in range(len(line)):
    #     b.insert(0,line[i])
    ls=line[::-1]
    print(','.join(ls))

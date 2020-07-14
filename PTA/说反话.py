def dayin(p):
    if len(p) >= 1:
        for i in range(len(p)-1):
            print(p[i], end=' ')
        print(p[-1], end='')
    else:
        print(p[0])
s=input()
s=s.split(' ')
c=[]
c=s[::-1]
dayin(c)


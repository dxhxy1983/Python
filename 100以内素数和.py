sum=0
l=[]
for i in range(101):
    for j in range(2,i+1):
        yu=i%j
        if yu==0 and j<i:
            break
        elif yu==0 and j==i:
            l.append(i)
for i in range(len(l)):
    sum=sum+l[i]         
print(sum)
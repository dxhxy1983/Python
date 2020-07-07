a=1
b=1
sum=0
for i in range(966):
    sum=sum+a*b
    a=a+1
    b=0-b
print(sum)
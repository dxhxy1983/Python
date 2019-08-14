s=input()
l=set(s)
t=list(l)
sum=0
for i in range(len(t)):
    sum+=eval(t[i])
print(sum)
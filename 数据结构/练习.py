# // n = 9; m = 0; 

# // ‌
# // for (i=1;i<=n;i++)

# // ‌
# //   for (j = 2*i; j<=n; j++)

# // ‌
# //     m=m+1;
# // printf(m);
n=9
m=0
for i in range(1,n+1):
    for j in   range(2*i,n+1):
        m+=1
        print(m)


def main():
    n=eval(input("请输入a："))
    step=0
    while n>1:
        if ((n%2)==0 ):
           n=n/2
           step+=1
        else :
           n=3*n+1
    print(step)

main()

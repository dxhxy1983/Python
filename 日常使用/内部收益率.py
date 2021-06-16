import math

def main():
    irr_year=eval(input("请输入收益率："))
    irr_month=pow((1+irr_year),1/12)-1
    print(irr_month)
    n=eval(input("请输入总期数："))
    a=[]
    sum=0
    for i in range (0,n):
        a.append(eval(input("请输入第{0}期数值：".format(i+1))))
    # print(a)
    for i in range (0,n):
        sum=+a[i]*pow((1+irr_month),n-i)
        print(sum)


if __name__=="__main__":
    main()
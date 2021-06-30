import math

def main():
    irr_year=eval(input("请输入收益率："))
    irr_month=pow((1+irr_year/100.0),1/12)-1
   
    a=[]
    with open(r"C:\Users\DXHQXX\Documents\GitHub\Python\日常使用\现金流.txt") as f:
        lines=f.readlines()
        for line in lines:
            a.append(-int(line))
    



    n=len(a)
    sum=0
    for i in range (0,n):
        sum=sum+a[i]*pow((1+irr_month),n-i)
        print(sum)


if __name__=="__main__":
    main()
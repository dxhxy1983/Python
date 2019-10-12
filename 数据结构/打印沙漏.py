def main():
    rawInput=input()
    num,zifu=rawInput.split(' ')
    m=hangshu(eval(num))
    dayinshuchu(m,zifu)
    zongshu=tongjishuchu(m)
    print(eval(num)-zongshu,end='')
def dayinshuchu(m,zifu):
    for i in range(0,m):
        shuchu(m-i,m,zifu)
        print()
    for i in range(2,m+1):
        shuchu(i,m,zifu)
        print()
def tongjishuchu(hangshu):
    sum=0
    for i in range(1,hangshu+1):
        sum=sum+i*2-1
    for i in range(2,hangshu+1):
        sum=sum+i*2-1
    return sum
    
def hangshu(num):
    sum=0
    j=0
    
    for i in range(num):
        sum=tongjishuchu(i)
        j=i
        if sum>num:
            break
    return j-1

def shuchu(hangDangqian,hangZongji,zifu):
    data=[]
    for i in range(hangZongji*2-1):
        data.append(zifu)
    if hangDangqian<hangZongji:
        chazhi=hangZongji-hangDangqian
        for i in range(chazhi):
            data[i]=' '
            data[-i-1]=' '
    for item in data:
        print(item,end=' ')
  
main()
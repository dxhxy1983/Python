def getNum():       #获取用户不定长度的输入
    num=[]
    n=input("请输入数字：")
    while n!='':
        num.append(eval(n))
        n=input("请输入数字：")
    return num


def mean(numbers):  #计算平均值
    sum=0    
    for i in range(len(numbers)):
        sum+=numbers[i]
    return sum/len(numbers)
    
def dev(numbers, mean): #计算标准差
    sdev = 0.0
    for num in numbers:
        sdev = sdev + (num - mean)**2
    return pow(sdev / (len(numbers)-1), 0.5)

def median(numbers):    #计算中位数
    sorted(numbers)
    if len(numbers)%2==0:
        midnum=(numbers[len(numbers)//2-1]+numbers[len(numbers)//2])/2
    else:
        midnum=numbers[len(numbers)//2]
    return midnum
def main():     
        n=getNum() #主体函数
        m=mean(n)
        d=dev(n, m)
        mid=median(n)
        print("平均值:{:.2f},标准差:{:.2f},中位数:{}".format(m,d,mid))
main()
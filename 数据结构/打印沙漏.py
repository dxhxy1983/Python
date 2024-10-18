def main():
    rawInput=input()
    num,zifu=rawInput.split(' ')
    num=int(num)
    jisuanhangshu,used_num=hangshu((num))  #计算总共多少行
    print_decreasing_pattern(jisuanhangshu,zifu)    
    print(str(num-used_num))
def print_decreasing_pattern(n, char):
    # 计算初始宽度，确保第一次打印的内容居中
    width = n*2-1
    
    for i in range(n, 0, -1):
        # 使用center方法居中显示字符
        print((char * (i*2-1)).center(width))
    for i in range(2, n+1, 1):
        print((char * (i*2-1)).center(width)) 
  
def hangshu(num):
    sum=1
    i=1
    j=0   
    while i>=1:
        sum=2*pow(i,2)-1
        j=i
        i+=1       
        if sum>num:
            return j-1,int(2*pow(j-1,2)-1)
            break  
main()
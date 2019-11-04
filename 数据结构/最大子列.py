def MaxSubseqSum4(A, N ):
    MaxSub=[]
    ThisSum = MaxSum = 0
    for i in range(0,N):
          ThisSum += eval(A[i]) #/* 向右累加 *
          if(ThisSum>0):
              append.MaxSub(A[i])
                  
          if( ThisSum > MaxSum ):
          
                  MaxSum = ThisSum #/* 发现更大和则更新当前结果 */
          elif( ThisSum < 0 ): #/* 如果当前子列和为负 */
                  ThisSum = 0 #/* 则不可能使后面的部分和增大，抛弃之 */
                MaxSub[:]=[]
    return MaxSum 
def main():
    Num=eval(input())
    rawInput=input()
    Arry=rawInput.split(' ')
    MaxSubseqSum=MaxSubseqSum4(Arry,Num)
    print(MaxSubseqSum)

main()
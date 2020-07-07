
def prime(m):
    
    l=[]
    for i in range(m,10000*m):
        if len(l)<5:
            for j in range(2,i+1):
                yu=i%j
                if yu==0 and j<i:
                    break
                elif yu==0 and j==i:
                    l.append(i)
    return l
def main():
    n=eval(input())
    m=int(n)+1
    l=prime(m)
    for i in range(len(l)):
        if i<len(l)-1:
            print(l[i],end=',')
        else:
            print(l[i])
main()

s=input()
# n=eval(s)
# l=s.split()

def dayin(l,weishu):
    l=eval(l)
    if weishu==3:
        for i in range(0,l):
            print('B',end='')
    elif weishu==2:
        for i in range(0,l):
            print('S',end='')  
    else:
        for i in range(1,l+1):
            print(i,end='')
def weishu(s):
    a=s[0]
    l=len(s)
    s=s[1:]
    return a,l,s         

if __name__ == "__main__":
    # l,weishu,s=weishu('430')
    # print(l,weishu,s)
    while len(s)>=1:
         dayin(s[0],len(s))
         s=s[1:]  


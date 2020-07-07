count=0
def hano(n,src,dst,mid):
    if n==1:
        global count
        count+=1
        print("{}:{}->{}".format(1,src,dst))
    else:
        hano(n-1,src,mid,dst)        
        print("{}:{}->{}".format(n,src,dst))
        count+=1
        hano(n-1,mid,dst,src)
       
def main():
    hano(3,'A','C','B')
    print(count)
main()

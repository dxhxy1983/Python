def main():
    n=input()
    su=0
    su=sum(n)
    p=output(su)
    dayin(p)
def sum(n):
    s=n
    sum=0
    for i in range(len(s)):
        sum=sum+eval(s[i])
    return sum
def output(sum):
    trans={'0':'ling','1':'yi','2':'er','3':'san','4':'si','5':'wu',
                '6':'liu','7':'qi','8':'ba','9':'jiu'}
    samplestr = '%d'%sum
    p=[]
    for i in range(len(samplestr)):
        a=samplestr[i]
        p.append(trans[a])
    return p
def dayin(p):
    for i in range(len(p)-1):
        print(p[i],end=' ')
    print(p[-1],end='')
    

main()

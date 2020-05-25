def main():
    s=keyinput()
    letters=s
    for i in range(len(letters)):
        p=juge1(letters[i])
        
        print(p)

    
def keyinput():
    n=int(input())
    s=[]
    for i in range(n):
        s.append(input())
    return s
def juge1(letters):#判断是否有P，A，T之外字符
    dic={'P','A','T'}
    if 'P' in letters and 'A' in letters and 'T' in letters:#判断是否有P，A，T字符
        for i in range(len(letters)):
            if letters[i] not in dic:
                 return False
            elif i==len(letters)-1 :
                 return True
    else :
        return False


main()

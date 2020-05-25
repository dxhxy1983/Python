def main():
    s=input('')
    
    zhi2=['零','一','二','三','四','五','六','七','八','九']
    # print(len(s))
    # print(zhi2[1])
    m=[]
    for i in range(len(s)):
        print(zhi2[eval(s[i])],end='')
    

main()
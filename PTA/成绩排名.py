import pandas as pd 

def keyinput():
    n = int(input('请输入数量：'))
    s = []
    
    for i in range(n):
        print('请输入第', i+1, '个姓名、学号，成绩：', end='')

        s.append(input())
    return s


if __name__ == "__main__":

    s = keyinput()
    l=[]
    d={}
    for i in range(len(s)):
        l=s[i].split()
        a = ['姓名', '学号','成绩']
        dict1=dict(zip(a,l))
        d.update(dict1)
    df=pd.DataFrame(d)
    print(df)


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
    a = ['姓名', '学号','成绩']
    df = pd.DataFrame(index=a) #将输入转换为DataFrame
    for i in range(len(s)):
        l=s[i].split()
        df0=pd.Series(l,index=a)
        df[i]=df0

    dft=df.T
    dfmax=dft[dft['成绩']==dft['成绩'].max()]
    dfmin=dft[dft['成绩']==dft['成绩'].min()]

    print('{0} {1}'.format(dfmax.iloc[0,0],dfmax.iloc[0,1]))
    print('{0} {1}'.format(dfmin.iloc[0,0] ,dfmin.iloc[0,1]))

from random import random
def main():
    printInfo()
    proA,proB,n=getInput()
    winsA,winsB=simNgame(proA,proB,n)
    printSummary(winsA,winsB)
def printInfo():
    print('此程序模拟两名球员进行比赛，并输出结果')
    print('需要输入两名球员能力值（0-1）之间数值表示')
def getInput():
    a=eval(input('请输入球员A能力值（0-1）之间数值表示:'))
    b=eval(input('请输入球员A能力值（0-1）之间数值表示:'))
    n=eval(input("请输入模拟比赛的场次数量："))
    return a,b,n
def simNgame(proA,proB,n):
    winsA,winsB=0,0
    for i in range(n):
        scoreA,scoreB=simOnegame(proA,proB)
        if scoreA>scoreB :
            winsA+=1
        else:
            winsB+=1
    return winsA,winsB
def simOnegame(proA,proB):
    prob='A'
    scoreA,scoreB=0,0
    while not (scoreA==15 or scoreB==15):
        if prob=='A':
            if random()<proA:
                scoreA+=1
            else:
                prob='B'
        if prob=='B':
            if random()<proB:
                scoreB+=1
            else:
                prob='A'
    return scoreA,scoreB           
        

def printSummary(winsA,winsB):
    n=winsA+winsB
    print('共模拟{}场比赛'.format(n))
    print('选手A获胜{}场，占比{:.1%}'.format(winsA,winsA/n))
    print('选手B获胜{}场，占比{:.1%}'.format(winsB,winsB/n))

main()


def dayin(p):
    for i in range(len(p)-1):
        print(p[i], end=' ')
    print(p[-1], end='')


def main():
    m = input()
    a,b = m.split(' ')
    a=eval(a)
    b=eval(b)
    s = input()
    c = s.split(' ')
    c = c[a-b:]+c[:a-b]
    dayin(c)
main()

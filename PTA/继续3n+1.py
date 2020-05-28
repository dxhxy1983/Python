
def Tn(number):
    s = []
    while number > 1:
        if ((number % 2) == 0):
            number = number/2
            s.append(int(number))
        else:
            number = (3*number+1)
    return s


def dayin(p):
    for i in range(len(p)-1):
        print(p[i], end=' ')
    print(p[-1], end='')


if __name__ == "__main__":
    n = eval(input())
    s = input()
    targetNumber = list(map(int, s.split()))
    compareNumber = Tn(n)
    diffNumber = set(targetNumber).difference(set(compareNumber))
    diffNumber = list(diffNumber)
    d = diffNumber.sort(reverse=True)
    dayin(diffNumber)

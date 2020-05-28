n = input()
i = input()
list1 = list(map(int , i.split()))
list2 = list1.copy()

def text(n):
    if n % 2 == 0:
        n = n/2
    else:
        n = (3 * n + 1) / 2
    return n

for i in list1:
    a = i
    while a > 1:
        a = text(a)
        if a in list2:
            list2.remove(a)
list2.sort(reverse=True)
for i in list2 :
    if i!=list2[len(list2)-1]:
        print(i,end=' ')
    else:
        print(i)

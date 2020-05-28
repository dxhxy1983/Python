
d = {}
b = []

n = input('请输入数字:')
for i in range(int(n)):
    print('请输入第', i+1, '个姓名、学号，成绩：', end='')

    a = input().split()
    d[int(a[2])] = a[0]+' '+a[1]
for key in d:
    b.append(key)
print(d[max(b)])
print(d[min(b)])

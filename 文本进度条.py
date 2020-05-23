import time

scal = 50
print('执行开始'.center(scal // 2, '-'))
start = time.perf_counter()
for i in range(scal + 1):
    a = '*' * i
    b = '-' * (scal - i)
    c = (i / scal) * 100
    dur = time.perf_counter() - start
    time.sleep(0.2)
    print('\r{:.3f}%[{}->{:.2f}s{}]'.format(c, a, dur, b), end='')

print('\n' + '执行结束'.center(scal // 2, '-'))

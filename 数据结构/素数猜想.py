def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def find_primes_up_to_n(n):
    primes = []
    for num in range(2, n+1):
        if is_prime(num):
            primes.append(num)
    return primes

def count_twin_primes(primes):
    count = 0
    for i in range(1, len(primes)):
        if primes[i] - primes[i-1] == 2:
            count += 1
    return count

# 读取输入
N = int(input())

# 找出所有不超过N的素数
primes = find_primes_up_to_n(N)

# 计算满足猜想的素数对的个数
twin_prime_count = count_twin_primes(primes)

# 输出结果
print(twin_prime_count)
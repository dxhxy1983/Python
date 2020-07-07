def main():
    df = 0.01
    while fact(df) < pow(1.01, 365):
        df = df + 0.0001
    print('工作日的努力参数是：{:.6f}'.format(df))


def fact(df):
    fact1 = 1.0
    for i in range(365):
        if i % 7 in [6, 0]:
            fact1 = fact1 * (1 - 0.01)
        else:
            fact1 = fact1 * (1 + df)
    print(fact1)
    return fact1


main()

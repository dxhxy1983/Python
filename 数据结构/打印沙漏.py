def main():
    # 获取输入
    raw_input = input()
    num, zifu = raw_input.split(' ')
    num = int(num)
    
    # 计算沙漏可以使用的行数和用掉的符号数
    jisuanhangshu, used_num = hangshu(num)
    
    # 打印沙漏图案
    print_decreasing_pattern(jisuanhangshu, zifu)
    
    # 打印剩余的符号数
    print(num - used_num)

def print_decreasing_pattern(n, char):
    # 计算初始宽度，确保第一次打印的内容居中
    width = n * 2 - 1
    
    # 打印沙漏上半部分（含中间）
    for i in range(n, 0, -1):
        # 每行字符数量为2*i-1，并根据最大宽度居中
        line = char * (2 * i - 1)
        print(' ' * (n - i) + line)
    
    # 打印沙漏下半部分
    for i in range(2, n + 1):
        line = char * (2 * i - 1)
        print(' ' * (n - i) + line)

def hangshu(num):
    sum_used = 1  # 用掉的符号数量
    i = 1         # 当前的行数（从1开始）
    
    while True:
        # 计算2*i^2 - 1表示使用的符号数
        if 2 * i * i - 1 > num:
            # 超过符号数时，返回能使用的行数和用掉的符号数
            return i - 1, 2 * (i - 1) * (i - 1) - 1
        i += 1

main()

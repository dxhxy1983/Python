# -*- coding: utf-8 -*-  
""" 
@author: DoraVemon
@file: autogen_arith.py 
@time: 2018/10/2 8:45 
"""

import random
from datetime import datetime


def add_test(sum_value, count):
    '''
    返回指定个数（count）的计算题，以计算某数(sum_value）以内的加法
    :param sum_value: 指定某数以内（的加法）
    :param count: 随机生成多少题
    :return: 返回count个计算题
    '''

    questions = []
    count_temp = 0  # 计数器

    while True:
        i = random.randrange(1, sum_value)  # 随机生成 第一个加数
        k=random.randrange(1,sum_value)  #随机生成第二个数
        j = random.randrange(1, sum_value )  # 随机生成第三个数
        # l = j - i-k  # 第二个加数
        flag_add1=random.randint(0,1)
        flag_add2=random.randint(0,1)
        if flag_add1==0 and flag_add2==0:
            if i+k+j<=sum_value:
                # questions.append(i,j,k,i+j+k)
                # print(' {} + {} + {} = {} '.format(i,j,k,i+j+k))
                str_temp = str(i) + ' + ' + str(j) + ' + ' + str(k)+' =    '
                # questions += str_temp
                questions.append((str_temp))
                count_temp+=1
        elif flag_add1==1 and flag_add2==0:
            if i>j  and i-j+k<sum_value:
                # print(' {} - {} + {} = {} '.format(i,j,k,i-j+k))
                str_temp = str(i) + ' - ' + str(j) + ' + ' + str(k)+' =    '
                # questions += str_temp
                questions.append((str_temp))
                count_temp+=1
        elif flag_add1==0 and flag_add2==1:
            if i+j>k and i+j<=sum_value:
                # print(' {} + {} - {} = {} '.format(i,j,k,i+j-k))
                str_temp = str(i) + ' + ' + str(j) + ' - ' + str(k)+' =    '
                # questions += str_temp
                questions.append((str_temp))
                count_temp+=1
        elif flag_add1==1 and flag_add2==1:
            if i-j-k>0:
                # print(' {} - {} - {} = {} '.format(i,j,k,i-j-k))
                str_temp = str(i) + ' - ' + str(j) + ' - ' + str(k)+' =   '
                # questions += str_temp
                questions.append((str_temp))
                count_temp+=1
                     
            # str_temp = str(i) + ' + ' + str(l) + '' + ' =    \n'
            # questions += str_temp
            # questions.append((i, l,k, j))
            # count_temp += 1
        if count_temp >= count:
            break

    return questions


# def resort(quiz):
#     rng_index = random.randint(0, 2)
#     flag_addsub = random.randint(0, 1)
#     if flag_addsub:
#         str_temp = (str(quiz[0]) if rng_index != 0 else '(  )') + ' + ' \
#                    + (str(quiz[1]) if rng_index != 1 else '(  )') \
#                    + ' = ' \
#                    + (str(quiz[2]) if rng_index != 2 else '(  )') + '\n'
#     else:
#         str_temp = (str(quiz[2]) if rng_index != 0 else '(  )') + ' - ' \
#                    + (str(quiz[1]) if rng_index != 1 else '(  )') \
#                    + ' = ' \
#                    + (str(quiz[0]) if rng_index != 2 else '(  )') + '\n'
#     return str_temp


def main():
    sum_value, count = 100, 100  # 随机出20题，10以内的加减法
    text = ''
    quizs = add_test(sum_value, count)
    # for quiz in quizs:
    #     text += resort(quiz)
    title = '%d以内加法算术题' % sum_value + datetime.now().strftime("_%Y%m%d") + '.txt'
    with open(title, "w") as f:
        for i in quizs:
            f.write(str(i)+'\n')
    f.close()


if __name__ == '__main__':
    main()

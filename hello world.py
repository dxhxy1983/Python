# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 14:47:23 2019

@author: D
"""
def main():
    s=(input())
    print(s)
    l=s.split()
    print(l)
#    print(m)
#    m,op,n=input()
#   
    m=eval(l[0])
    op=l[1]
    n=eval(l[2])
    print(m)
    print(op)
    print(n)
    if op=='+':
        print('M+N={:.2f}'.format(m+n))
    elif op=='-'  :
        print('M-N={:.2f}'.format(m-n))
    elif op=='*':
        print('M*N={:.2f}'.format(m*n))
    elif op=='/':
        print('M/N={:.2f}'.format(m/n))
    

main()

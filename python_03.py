#!/usr/bin/python3
'''打印斐波那契数列'''
import sys

fib = [0, 1]
def mk_fib(long=10):
    for i in range(long -2):
        k = fib.append(fib[-2] + fib[-1])
    return fib

if __name__ == '__main__':
    print(mk_fib(int(sys.argv[1])))
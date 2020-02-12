#!/usr/bin/python3
'''打印随机字符串'''
from random import choice
from string import ascii_letters, digits

zifuji = ascii_letters + digits
def suijizifu(n = 8):
    result = ''
    for i in range(n):
        zifu = choice(zifuji)
        result += zifu
    return result

if __name__ == '__main__':
    print(suijizifu())
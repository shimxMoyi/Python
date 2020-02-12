#!/usr/bin/python3

'''新建文本文件并写入内容'''

import os

def get_fname():
    '获取文件名,返回一个不存在的文件名'
    while 1:
        fname = input('文件名: ')
        if not os.path.exists(fname):
            break
        print('文件以存在, 请重试: ')
    return fname


def get_content():
    '获取输入内容,返回列表'
    content = []
    print('请输入文件内容, 输入 end 结束输入')
    while 1:
        line = input('(end to quit)> ')
        if line == 'end':
            break
        content.append(line + '\n')
    return content


def wfile(fname, content):
    '将内容写入到文件'
    with open(fname, 'w') as fobj:
        fobj.writelines(content)


if __name__ == '__main__':
    fname = get_fname()
    content = get_content()
    # content = ['%s\n' % line for line in content]
    wfile(fname, content)

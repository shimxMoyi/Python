#!/usr/bin/python3

'''创建用户，设置密码，用户信息写入到文件'''

import sys
import python_02
import subprocess

def adduser(user, passwd, fname):
    result = subprocess.run(
        'id %s &> /dev/null' % user, shell=True
    )
    if result.returncode == 0:
        print('用户已经存在')
        return

    subprocess.run(
        'useradd %s' % user, shell=True
    )

    subprocess.run(
        'echo %s | passwd --stdin %s' % (passwd, user), shell=True
    )

    info = '''用户信息
用户名: %s
密码: %s
''' % (user, passwd)
    with open(fname, 'a') as fobj:
        fobj.write(info)

if __name__ == '__main__':
    user = sys.argv[1]
    passwd = python_02.suijizifu()
    fname = sys.argv[2]
    adduser(user, passwd, fname)

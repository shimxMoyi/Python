import sys
import subprocess
from random import choice
from string import ascii_letters, digits

def adduser(username, password, fname):
    data = '''user information
%s: %s
'''
    subprocess.run('useradd %s' % username, shell=True)
    subprocess.run(
        'echo %s | passwd --stdin %s' % (password, username),
        shell=True
    )
    with open(fname, 'a') as fobj:
        fobj.write(data % (username, password))

def set_passwd(n=8):
    zifuji = ascii_letters + digits
    password = ''
    for i in range(8):
        password += choice(zifuji)
    return password

if __name__ == '__main__':
    username = sys.argv[1]
    password = set_passwd()
    adduser(username, password, '/tmp/user.list')

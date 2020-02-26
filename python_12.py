#!/usr/bin/python3

'''
Gitlab + Jenkins 部署 WEB 页面

1. 创建 git repo, 上传到 Gitlab
2. 使用 Jenkin 拉取 Gitlab 上的代码，开始构建
3. 使用 Jenkins 页面打包，计算 md5 值用于校验，通过 httpd 共享
4. 运行 Python 脚本，下载 Jenkin 服务器上的 tarball 并解压，自动上线最新页面
'''

import os
import requests
import wget
import hashlib
import tarfile

def has_new_ver(ver_fname, ver_url):
    '用于检查是否有新版本，有返回真，没有返回假'
    # 如果本地没有版本文件，则有新版本
    if not os.path.isfile(ver_fname):
        return True

    # 如果本地版本号与网上版本号不一样，则有新版本
    with open(ver_fname) as fobj:
        local_ver = fobj.read()   # 从本地文件中读取本地版本号

    r = requests.get(ver_url)     # 获取网上的版本号
    if local_ver != r.text:
        return True
    else:
        return False

def file_ok(md5_url, app_fname):
    '用于检查文件是否完好，完好为真，否则为假'
    # 计算本地文件的md5值
    m = hashlib.md5()
    with open(app_fname, 'rb') as fobj:
        while 1:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)

    # 比较本地文件的md5值和网上给出的md5值
    r = requests.get(md5_url)
    if m.hexdigest() == r.text.strip():  # 网上文件的md5值尾部可能有\n，去除它
        return True
    else:
        return False

def deploy(app_fname, deploy_dir, dest):
    # 解压缩
    tar = tarfile.open(app_fname)
    tar.extractall(path=deploy_dir)
    tar.close()

    # 拼接解压文件的绝对路径
    app_dir = os.path.basename(app_fname)
    app_dir = app_dir.replace('.tar.gz', '')
    app_dir = os.path.join(deploy_dir, app_dir)

    # 目标软链接文件如果存在，则删除
    if os.path.exists(dest):
        os.remove(dest)

    # 创建链接文件
    os.symlink(app_dir, dest)

if __name__ == '__main__':
    # 检查是否有新版本
    ver_fname = '/var/www/deploy/live_ver'
    ver_url = 'http://192.168.1.67:8008/deploy/live_ver'
    if not has_new_ver(ver_fname, ver_url):
        print('未发现新版本')
        exit(1)

    # 下载新版本压缩包
    down_dir = '/var/www/download'
    r = requests.get(ver_url)
    app_url = 'http://192.168.1.67:8008/deploy/pkgs/myweb-%s.tar.gz' % r.text
    wget.download(app_url, down_dir)

    # 校验下载的压缩包是否损坏，如果损坏则删除它
    md5_url = app_url + '.md5'   # 拼接md5的url
    app_fname = app_url.split('/')[-1]
    app_fname = os.path.join(down_dir, app_fname)  # 拼接本地文件的绝对路径
    if not file_ok(md5_url, app_fname):
        print('文件已损坏')
        os.remove(app_fname)
        exit(2)

    # 部署软件
    deploy_dir = '/var/www/deploy'
    dest = '/var/www/html/nsd1909'
    deploy(app_fname, deploy_dir, dest)

    # 更新本地版本文件
    if os.path.exists(ver_fname):
        os.remove(ver_fname)
    wget.download(ver_url, ver_fname)

    print('上线完成')

#!/usr/bin/env python
import sys
import os
import time

'''
手动编写一个daemon进程
'''


def daemonize(stdin="/dev/null", stdout="/dev/null", stderror="/dev/null"):
    try:
        pid = os.fork()
# 为什么创建子进程要把父进程退出？
        if pid > 0:
            sys.exit(0)
    except OSError as err:
        sys.stderr.write(f"_Fork #1 Failed: {0} \n")
        sys.exit(1)
    # decouple from parenet enviroment so it can be unmount
    os.chdir("/")
    # 调用umask(0) 拥有写任何程序的权限，避免导致继承自父进程的umask被修改而导致自身权限不足
    os.umask(0)
    # setsid 被调用成功后，进程会成为新的会话租组长，与原来的对话和进程组脱离
    os.setsid()

    # 重定向标准文件描述符
    sys.stdout.flush()
    sys.stderr.flush()

    si = open(stdin, "r")
    so = open(stdout, "a+")
    se = open(stderror, "w")

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def test():
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid())
    while True:
        now = time.strftime("%X", time.localtime())
        sys.stdout.write(f'{time.ctime()}\n')
        sys.stdout.flush()
        time.sleep(1)


if __name__ == "__main__":
    daemonize('/dev/null', '/Users/SW/Desktop/d1.log', '/dev/null')
    test()

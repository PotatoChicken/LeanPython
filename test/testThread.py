#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""learn threading"""

__author__ = "eric"

import threading
import time


# 新线程执行的代码
def loop():
    print("thread %s is running ...." % threading.current_thread().name)
    n = 0
    while n < 5:
        n += 1
        print('thread %s >> %d' % (threading.current_thread().name, n))
        time.sleep(2)
    print('thread %s is end' % threading.current_thread().name)


def test():
    print("thread %s is running ..." % threading.current_thread().name)
    t = threading.Thread(target=loop, name='LoopThread')
    t.start()
    t.join()
    print("thread %s ended" % threading.current_thread().name)


# 银行存款
balance = 0
lock = threading.Lock()


def change_it(n):
    global balance
    balance += n
    balance -= n


def run_thread(n):
    for i in range(1000000):
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()


def test1():
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("the balance %s" % balance)


if __name__ == '__main__':
    test1()

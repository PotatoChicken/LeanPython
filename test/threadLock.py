#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" test thread local
"""

import threading

local_school = threading.local()


def process_student():
    std = local_school.student
    print("hello, %s (in %s)" % (std, threading.current_thread().name))


def process_thread(name):
    local_school.student = name
    process_student()


def test():
    t1 = threading.Thread(target=process_thread, args=("Eric",), name="thread_a")
    t2 = threading.Thread(target=process_thread, args=("Grace",), name="thread_b")
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    test()
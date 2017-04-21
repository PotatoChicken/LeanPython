#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'a test module'

__author__ = 'eric'

import sys


def test():
    args = sys.argv
    argsLen = len(args)
    if argsLen == 1:
        print("the args is %s" % args[0])
    elif argsLen == 2:
        print("the args is %s and %s" % (args[0], args[1]))
    else:
        print("the args is to many")

if __name__ == '__main__':
    test()

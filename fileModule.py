#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'list all file in folder'

import os


def listAllFiles(key, path):
    for f in os.listdir(path):
        absPath = os.path.join(path, f)
        if os.path.isfile(absPath):
            print(f)
        elif os.path.isdir(absPath):
            listAllFiles(key, absPath)


if __name__ == '__main__':
    listAllFiles("py", '.')

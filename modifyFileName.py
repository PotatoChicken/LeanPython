#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'list all file in folder'

import os
from os import walk

def modifyFileName(needModifyFileName, toFileName):
    f = []
    for (dirpath, dirnames, filenames) in walk('.'):
        f.extend(filenames)
        break

    print(f)

    # 先判断需要修改名称的文件是否存在
    isExitNeedModifyFile = False
    for fileName in f:
        if needModifyFileName in fileName:
            isExitNeedModifyFile = True
            break

    # 如果需要修改名称的文件存在则删除命名后的文件
    if isExitNeedModifyFile:
        try:
            os.remove(toFileName)
        except FileNotFoundError:
            print("not found need remove file!!!!!")
        else:
            print("remove file success")
    else:
        print("The file whose name needs to be modified does not exist!!!!")

    # 修改文件名
    for fileName in f:
        if needModifyFileName in fileName:
            os.renames(fileName, toFileName)
            break

if __name__ == '__main__':
    modifyFileName("Signed_Aligned", 'SystemUI.apk')

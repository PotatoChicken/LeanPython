# !/bin/usr/env python3
# -*- coding: utf-8 -*-

"""
test socket client
"""

__author__ = "eric"

import socket, threading


def test():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 9997))
        print(s.recv(1024).decode('utf-8'))

        for data in [b'Eric', b'Grace', b'Grace and Eric']:
            s.send(data)
            print(s.recv(1024).decode('utf-8'))
        s.send(b'exit')


if __name__ == "__main__":
    test()
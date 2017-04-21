# !/bin/usr/env python3
# -*- coding: utf-8 -*-

"""
test socket server, bind '127.0.0.1', port 9997
"""

__author__ = "eric"

import socket, threading

def test():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 9997))
        s.listen(5)
        print("waiting for connect...")
        while True:
            sock, addr = s.accept()
            t = threading.Thread(target=handlerTcp, args=(sock, addr))
            t.start()


def handlerTcp(sock, addr):
    print("Accept new connection from %s:%s..." % addr)
    try:
        sock.send(b'Welcome!')
        while True:
            data = sock.recv(1024)
            if not data or data.decode('utf-8') == 'exit':
                break;
            sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
        sock.close()
    finally:
        sock.close()
    print("connection from %s:%s closed." % addr)


if __name__ == "__main__":
    test()

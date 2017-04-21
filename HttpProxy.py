#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import socket
import urllib
import select


class MyHandler(BaseHTTPRequestHandler):
    def connect_to(self, location, destination_socket):
        i = location.find(':')
        if i >= 0:
            host = location[:i]
            port = int(location[i + 1:])
        else:
            host = location
            port = 80
        print 'Connecting to {0}:{1}'.format(host, port)
        try:
            host_ip = socket.gethostbyname(host)
            self.socket.connect((host_ip, port))
        except socket.error, arg:
            try:
                msg = arg[1]
            except:
                msg = arg
            self.send_error(404, msg)
            return 0
        return 1

    def read_write(self, socket, max_idling=100):
        iw = [self.connection, socket]
        ow = []
        count = 0
        while count != max_idling:
            count += 1
            read_list, write_list, exception_list = select.select(iw, ow, iw, 3)
            if exception_list:
                break
            if read_list:
                for item in read_list:
                    out = self.connection if item is socket else socket
                    data = item.recv(8192)
                    if data:
                        out.send(data)
                        count = 0
            else:
                pass

    def do_CONNECT(self):
        uri = self.path
        print("connect uri: " + uri)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self.connect_to(uri, socket):
                print("Connected to %s" % (uri))
                self.log_request(200)
                self.wfile.write(self.protocol_version + " 200 Connection established\n")
                self.wfile.write("Proxy-agent: {0}\n".format(self.version_string()))
                self.wfile.write("\n")
                self.read_write(self.socket, 300)
        finally:
            print("Connection closed")
            self.socket.close()
            self.connection.close()

    def do_POST(self):
        uri = self.path
        print("post uri: " + uri)

    def do_GET(self):
        uri = self.path
        print("GET uri: " + uri)
        proto, rest = urllib.splittype(uri)
        host, rest = urllib.splithost(rest)
        # print("host: " + host)
        path = rest
        # print("path: " + path)
        host, port = urllib.splitnport(host)
        if port <= 0:
            port = 80
        # print("host %s, port %d" % (host, port))
        host_ip = socket.gethostbyname(host)
        # print("host_ip:" + host_ip)
        del self.headers["Proxy-Connection"]
        self.headers["Connection"] = "close"
        send_data = "GET " + path + " " + self.protocol_version + "\r\n"
        head = " "
        for key, val in self.headers.items():
            head += "%s: %s \r\n" % (key, val)
        send_data = send_data + head + "\r\n"
        # print(send_data)
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.connect((host_ip, port))
        so.sendall(send_data)
        data = " "
        while True:
            tmp = so.recv(4096)
            if not tmp:
                break
            data = data + tmp
        so.close()
        self.wfile.write(data)


def main():
    try:
        server = HTTPServer(('127.0.0.1', 8087), MyHandler)
        print("welcome to this machine....")
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C received, shutting down server")
        server.socket.close()


if __name__ == "__main__":
    main()

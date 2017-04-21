#!/usr/bin/env python

import eventlet

from eventlet.green.urllib import request

urls = [
    "http://www.baidu.com",
    "http://taobao.com",
    "http://jd.com",
    "http://www.csdn.net",
    "http://www.qq.com",
]


def fetch(url):
    print("opening", url)
    with request.urlopen(url) as f:
        print("Status: ", f.status, f.reason)
        for k, v in f.getheaders():
            print("%s : %s" % (k, v))
        # body = urllib.request.urlopen(request).read()
        body = f.read()
        print("done with", url)
        return url, body


pool = eventlet.GreenPool(200)


def test():
    for url, body in pool.imap(fetch, urls):
        print("got body from", url, "of length", len(body))


if __name__ == "__main__":
    test()


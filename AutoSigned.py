# -*- coding: utf-8 -*-
__author__ = 'wenbiao.xie'

import requests
import sys
import os

global auth_user
global auth_pass
global domain_uri #http://172.24.61.104/NB/

def create_session(auth):
    s = requests.session()
    if auth:
        s.auth = auth
    else:
        print("failed to create session, for no auth information to continue!!")
        exit(-1)
    return s

def got_cookie(s):
    global domain_uri
    url = domain_uri + "index.php"
    print(url)
    r = s.get(url)

    print(r)
    print(r.headers["Set-Cookie"])
    cookie_header = r.headers["Set-Cookie"]
    cookies = cookie_header.split(";")
    tag = "PHPSESSID="
    cookie = None
    for c in cookies:
        if tag in c:
            cookie = c
            break

    return cookie

def post_apk_with_cookie(s, cookie, apk_path):
    print("cookie: ", cookie)
    global domain_uri
    url = domain_uri + "index.php"
    kv = cookie.split("=")
    cookies = {}
    cookies[kv[0]] = kv[1]
    print("cookies: ", cookies)
    host = domain_uri
    dir, filename = os.path.split(apk_path)
    files = {"myfiles[]":(filename, open(apk_path, 'rb'), "application/octet-stream", {'Expires': '0'})}
    print("upload file ...")
    data = {
        "version":"V2_0",
        "key_type":"platform",
        "product":"TCL_Release",
        "sign_ap":"Sign APK"
    }

    r = s.post(url, data=data, files=files, cookies=cookies)
    print (r.headers)
    print(r.iter_content)
    print(r.text)
    signed_apk_suf ='window.open("'
    open_index = r.text.index(signed_apk_suf)
    if open_index >= 0:
        print "found the results apk"
        open_index += len(signed_apk_suf)
        end_index = r.text.find('")',open_index)
        if end_index < open_index:
            print "failed to parse apk url"
            exit(-1)

        signed_apk_url = r.text[open_index: end_index]
        signed_apk_url = host + signed_apk_url
        print "signed apk url: ", signed_apk_url
        return signed_apk_url
    else :
        print "not found the results apk"
        exit(-1)


def download_apk(s, apk_url, out_path, cookie):
    cookies = {}
    if cookie:
        kv = cookie.split("=")
        cookies[kv[0]] = kv[1]

    filename = apk_url.split('/')[-1]
    r = s.get(apk_url, stream=True, cookies=cookies)

    length = int(r.headers["content-length"])

    if out_path is None:
        out_path = os.getcwd() + os.sep

    if not out_path.endswith(os.sep):
        out_path += os.sep

    out_file_path = out_path + filename

    if not os.path.exists(out_path):
        os.makedirs(out_path)
    elif os.path.exists(out_file_path) and os.path.isfile(out_file_path):
        os.remove(out_file_path)

    print "start to download apk to ", out_file_path
    f = None
    try:
        with open(out_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
                f.flush()
    finally:
        if f:
            f.close()

    print "download success...."
    return out_file_path

def usage():
    print 'usage: python AutoSigned.py [-d dir] [-a user:pass] [apk1] [apk2] [apk3]...'

def read_conf():
    import ConfigParser
    conf_filename = "conf"
    if not os.path.exists(conf_filename):
        return None

    cf = ConfigParser.ConfigParser()
    confs = {}
    try:
        cf.read(conf_filename)
    except:
        return None

    s = cf.get("main", "dest")
    if s:
        s = s.strip()
        if len(s) > 0:
            confs["dest"] = s

    auth = cf.get("main", "auth")
    if auth:
        auth = auth.strip()
        if len(auth) > 0:
            confs["auth"] = auth

    domain = cf.get("main", "domain")
    if domain:
        domain = domain.strip()
        if len(domain) > 0:
            confs["domain"] = domain

    return confs


def main(argv):
    import getopt
    global auth_user
    global auth_pass
    global domain_uri

    try:
        opts, args = getopt.getopt(argv, "hd:a:", ["help", "dest=", "auth="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    destdir = None
    auth = None
    domain_uri = "http://172.24.61.104/NB/"

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(1)

        elif opt in ("-d", "--dest"):
            destdir = arg

        elif opt in ("-a", "--auth"):
            s = arg.split(":")
            auth_user=s[0]
            auth_pass=s[1]
            auth = (auth_user, auth_pass)

    confs = read_conf()
    if confs is not None and len(confs) > 0:
        if destdir is None and confs.has_key("dest"):
            destdir = confs["dest"]

        if auth is None and confs.has_key("auth"):
            sa = confs["auth"]
            s = sa.split(":")
            auth_user=s[0]
            auth_pass=s[1]
            auth = (auth_user, auth_pass)

        if confs.has_key("domain"):
            domain_uri = confs["domain"]


    unsigned_apks = []
    vlen = len(args)
    if vlen > 0:
        unsigned_apks = args[:]
    else :
        cur = os.getcwd() + os.sep
        filelist = os.listdir(cur)
        for f in filelist:
            fpathandname, fext = os.path.splitext(f)
            if len(fext) > 0 and fext == ".apk":
                unsigned_apks.append(cur + f)

    if len(unsigned_apks) == 0:
        print "not found any unsigned apks!"
        exit(-1)

    session = create_session(auth)
    c = got_cookie(session)
    print "cookie: ", c

    #apk_path="C:\\Users\\wenbiao.xie\\Desktop\\JDMall.apk"
    for apk_path in unsigned_apks:
        print "begin to signing apk ", apk_path
        url = post_apk_with_cookie(session, c, apk_path)
        apk = download_apk(session, url, destdir, c)
        dir, filename = os.path.split(apk_path)
        outdir, outfile = os.path.split(apk)
        if not outdir.endswith(os.sep):
            outdir += os.sep
        newfile = outdir + filename
        if os.path.exists(newfile):
            os.remove(newfile)

        os.rename(apk, newfile)
        print u"successfully to signed apk to ", newfile

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    main(sys.argv[1:])
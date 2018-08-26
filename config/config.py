#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser,io
import os.path
import sys

codetype = sys.getfilesystemencoding()
INI_FILE = """[Redis-Queue]
host = localhost
port = 6379
db = 0

[bloomfilter]
host = localhost
port = 6379
db = 1
blockNum = 1
key = bloomfilter

[sql]
host = localhost
port = 3306
user = root
passwd =
db =
charset = utf8mb4
"""

class config(object):
    """docstring for user"""
    def __init__(self):
        super(config, self).__init__()
        self.ok = True
        fname = ''
        if os.path.exists("utils"):
            fname = "config.ini"
        else:
            fname = "..\config.ini"
        if not os.path.isfile(fname):
            f = open(fname,"w")
            f.writelines(INI_FILE)
            f.close()
            self.ok = False
            #raise Exception("config file not exists, automatically created. Please fill the proper values")
        with open(fname) as f:
            myconfig = f.read().decode(codetype).encode("utf-8")
        configer = ConfigParser.RawConfigParser(allow_no_value=True)
        configer.readfp(io.BytesIO(myconfig))
        self.host = configer.get('Redis-Queue','host')
        self.port = configer.get('Redis-Queue','port')
        self.db = configer.get('Redis-Queue','db')
        self.bhost = configer.get('bloomfilter','host')
        self.bport = configer.get('bloomfilter','port')
        self.bdb = configer.get('bloomfilter','db')
        self.bblockNum = configer.get('bloomfilter','blockNum')
        self.bkey = configer.get('bloomfilter','key')
        self.shost = configer.get('sql','host')
        self.sport = configer.get('sql','port')
        self.suser = configer.get('sql','user')
        self.spass = configer.get('sql','passwd')
        self.sdb = configer.get('sql','db')
        self.charset = configer.get('sql','charset')

    def rq_config(self):
        return self.host, self.port, self.db, self.blockNum, self.key

    def bf_config(self):
        return self.bhost, self.bport, self.bdb, self.bblockNum, self.bkey

    def sql_conf(self):
        return self.shost,self.sport,self.suser,self.spass,self.sdb,self.charset

if __name__ == '__main__':
    my = config()
    if not my.ok:
        print "config file not exists, created automatically"
    print "[Redis-Queue]"
    print "host:",my.host,"\nport:",my.port,"\ndb:",my.db
    print "[bloomfilter]"
    print "host:",my.bhost,"\nport:",my.bport,"\ndb:",my.bdb
    print "blockNum:",my.bblockNum,"\nkey:",my.bkey
    print "[sql]"
    print "host:",my.shost,"\nport:",my.sport,"\ndb:",my.sdb
    print "user:",my.suser,"\npasswd:",my.spass,'\ncharset:',my.charset

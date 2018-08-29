#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import config
from database import sqlconn
from datebase import redisconn
from utils import whutparser, dupcheck
import os

class spider(object):
    """the industrious spider for whut internal webpages feeding the backend."""
    def __init__(self, arg):
        super(spider, self).__init__()
        self.arg = arg
        self.config = config()
        self.checker = dupcheck(self.config)
        self.lock = None
        self.resume = None
        self.parser = whutparser()
        self.parser.setProxy(self.config.proxy())
        self.mysql = sqlconn(self.config.sql_conf()
        if not os.path.isfile("spider.pid"):
            f.open("spider.pid","w")
            f.writelines("start")
            self.lock = f
            self.initialize()
        else:
            with open("spider.pid","r") as f:
                self.resume = f.readlines()
            f.open("spider.pid","a")
            self.lock = f
            self.resume()

    def __del__(self):
        self.lock.close()

    def initialize(self):
        self.parser.getCategory_and_facultyLink()
        self.mysql.createTab('article',False,True,
        ['id','title','link','content','keyword_id','category_id','datetime','source_id'],
         ['bigint','varchar(100)','varchar(120)','text','int','int','date','int'],
          ['auto_increment','not null','not null','not null','not null','not null','not null','not null'],
           ['id'], [], [], [], 'utf8mb4')
        self.lock.write('sql create table article')

        self.lock.write('getCategory_and_facultyLink\n')


    def resume(self):
        pass

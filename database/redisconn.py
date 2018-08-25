#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rq import Queue
from redis import Redis


class redisconn(object):
    """redis connection class"""
    def __init__(self):
        super(redisconn, self).__init__()
        self.q = Queue(connection = Redis())
    def enqueue(self, *args):
        self.q.enqueue(map(tuple,args))
    def enqPrint(self, arg):
        self.q.enqueue('print',arg)

if __name__ == '__main__':
    myconn = redisconn()
    #myconn.enqueue('print','http://i.whut.edu.cn')
    myconn.enqPrint('12345')

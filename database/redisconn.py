#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rq import Queue
from redis import Redis


class redisconn(object):
    """redis connection class"""
    def __init__(self, host='localhost', port=6379, db=0):
        """
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param blockNum: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        """
        super(redisconn, self).__init__()
        self.q = Queue(connection = Redis(host=host, port=port, db=db))
    def enqueue(self, func, *args, **kwargs):
        self.q.enqueue(func,args,kwargs)
    def enqPrint(self, arg):
        self.q.enqueue('print',arg)

if __name__ == '__main__':
    myconn = redisconn()
    #myconn.enqueue('print','http://i.whut.edu.cn')
    myconn.enqPrint('12345')

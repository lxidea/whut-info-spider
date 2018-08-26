#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql.cursors

class sqlconn(object):
    """sql connection class."""
    def __init__(self, host='localhost', port=3306, user='root', passwd='root', db='whut', charset='utf8mb4'):
        super(sqlconn, self).__init__()
        try:
            self.connection = pymysql.connect(host=host,
                             port=port,
                             user=user,
                             password=passwd,
                             db=db,
                             charset=charset,
                             cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            raise(e)

    def __del__(self):
        if self.connection.open:
            self.connection.close()

if __name__ == '__main__':
    conn = sqlconn('localhost',3307,'root','usbw')
    if conn.connection.open:
        print 'opened'

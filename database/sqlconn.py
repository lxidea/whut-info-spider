#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql.cursors
import warnings,pymysql.err
warnings.filterwarnings('error', category=pymysql.err.Warning)

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

    def createTab(self, table, temp=True, ifnotexists=False, fieldlist=[], typelist=[], attribs=[],
     primKeys=[], forgkeys=[], reftabs=[], refkeys=[], charset='utf8mb4'):
        lens = [len(fieldlist),len(typelist),len(attribs)]
        if max(lens)!=min(lens):
            return False, 'parameters not match'
        if len(primKeys)==0:
            return False, 'no primary key'
        lens = [len(forgkeys),len(reftabs),len(refkeys)]
        if max(lens)!=min(lens):
            return False, 'foreign keys not match'
        if temp:
            tempstr = "temporary"
        else:
            tempstr = ""
        if ifnotexists:
            ifnostr = "if not exists "
        else:
            ifnostr = ""
        sql = "create " + tempstr + " table " + ifnostr + table +' ('
        cdefs = ','.join([('`'+field+'` '+typelist[idx]+' '+attribs[idx]).strip() for idx,field in enumerate(fieldlist)])
        if len(primKeys)>0:
            primstr = 'primary key (' + ','.join(['`'+x+'`' for x in primKeys]) + ')'
        else:
            primstr = ''
        if len(forgkeys)>0:
            forkstrs = ','.join(['foreign key (%s) references %s(%s)'%(key,reftabs[idx],refkeys[idx]) for idx,key in enumerate(forgkeys)])
        else:
            forkstrs = ''
        tabopts = ') Engine=InnoDB default charset=' + charset + ' collate=' + charset + '_bin'
        sql += cdefs + ',' + primstr + forkstrs + tabopts
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
            self.connection.commit()
        except pymysql.err.Warning as e:
            return True, e
        except pymysql.err.Error as e:
            return False, e
        return True, None

    def insert(self, table, keylist, valuelist):
        if table is None or len(table)==0:
            return False
        if type(keylist) is not list or type(valuelist) is not list:
            return False
        if len(keylist)*len(valuelist)==0:
            return False
        keystr = ', '.join(['`'+x+'`' for x in keylist])
        values = tuple(valuelist)
        formats = ', '.join(['%s']*len(values))
        print keystr
        print values
        sql = "INSERT INTO ``" + table + "`` (" + keystr + ") VALUES (" + formats + ")"
        print sql
        with self.connection.cursor() as cursor:
            cursor.execute(sql, values)

        self.connection.commit()

if __name__ == '__main__':
    conn = sqlconn('localhost',3307,'root','usbw')
    if conn.connection.open:
        print 'opened'
        print conn.createTab('article',False,True,
        ['id','title','link','content','keyword_id','category_id','datetime','source_id','attachment_id'],
         ['bigint','varchar(100)','varchar(120)','text','int','int','date','int','int'],
          ['auto_increment','not null','not null','not null','not null','not null','not null','not null','not null'],
           ['id'], [], [], [], 'utf8mb4')
        #conn.insert('tab',['name','key','passwd'],['John',2,'123456'])

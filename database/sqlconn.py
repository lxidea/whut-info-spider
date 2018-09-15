#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql.cursors
import warnings,pymysql.err
warnings.filterwarnings('error', category=pymysql.err.Warning)

class sqlconn(object):
    """sql connection class."""
    def __init__(self, host='localhost', port=3306, user='root', passwd='root', db='whut', charset='utf8mb4', unix_socket=None):
        super(sqlconn, self).__init__()
        try:
            if unix_socket is None:
                self.connection = pymysql.connect(host=host,
                                 port=port,
                                 user=user,
                                 password=passwd,
                                 charset=charset,
                                 cursorclass=pymysql.cursors.DictCursor)
            else:
                self.connection = pymysql.connect(host=host,
                                 user=user,
                                 password=passwd,
                                 charset=charset,
                                 unix_socket=unix_socket,
                                 cursorclass=pymysql.cursors.DictCursor)
            sql = 'CREATE DATABASE IF NOT EXISTS' + db
            self.connection.cursor().execute(sql)
            self.connection.close()
        except:
            pass
        try:
            if unix_socket is None:
                self.connection = pymysql.connect(host=host,
                                 port=port,
                                 user=user,
                                 password=passwd,
                                 db=db,
                                 charset=charset,
                                 cursorclass=pymysql.cursors.DictCursor)
            else:
                self.connection = pymysql.connect(host=host,
                                 user=user,
                                 password=passwd,
                                 db=db,
                                 charset=charset,
                                 unix_socket=unix_socket,
                                 cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            raise(e)

    def __del__(self):
        if self.connection.open:
            self.connection.close()

    def createTab(self, table, fieldlist=[], typelist=[], attribs=[],
     primKeys=[], forgkeys=[], reftabs=[], refkeys=[], charset='utf8mb4',temp=False, ifnotexists=True):
        lens = [len(fieldlist),len(typelist),len(attribs)]
        if max(lens)!=min(lens):
            return False, 'parameters not match'
        if len(primKeys)==0:
            return False, 'no primary key'
        lens = [len(forgkeys),len(reftabs),len(refkeys)]
        if max(lens)!=min(lens):
            return False, 'foreign keys not match'
        if temp:
            tempstr = "temporary "
        else:
            tempstr = ""
        if ifnotexists:
            ifnostr = "if not exists "
        else:
            ifnostr = ""
        sql = "create " + tempstr + "table " + ifnostr + table +' ('
        cdefs = ','.join([('`'+field+'` '+typelist[idx]+' '+attribs[idx]).strip() for idx,field in enumerate(fieldlist)])
        if len(primKeys)>0:
            primstr = ', primary key (' + ','.join(['`'+x+'`' for x in primKeys]) + ')'
        else:
            primstr = ''
        if len(forgkeys)>0:
            forkstrs = ',' + ','.join(['foreign key (%s) references %s(%s)'%(key,reftabs[idx],refkeys[idx]) for idx,key in enumerate(forgkeys)])
        else:
            forkstrs = ''
        tabopts = ') Engine=InnoDB default charset=' + charset + ' collate=' + charset + '_bin'
        sql += cdefs + primstr + forkstrs + tabopts
        try:
            with self.connection.cursor() as cursor:
                self.result = cursor.execute(sql)
            self.connection.commit()
        except pymysql.err.Warning as e:
            return True, e
        except pymysql.err.Error as e:
            return False, e
        return True, self.result

    def insert(self, table, keylist, valuelist):
        """insert table, require tab_name, keylist, valuelist as argument,
        return True or False, affected rows or failure reason"""
        if table is None or len(table)==0:
            return False
        if type(keylist) is not list or type(valuelist) is not list:
            return False
        if len(keylist)*len(valuelist)==0:
            return False
        keystr = ', '.join(['`'+x+'`' for x in keylist])
        values = tuple(valuelist)
        formats = ', '.join(['%s']*len(values))
        sql = "INSERT INTO `" + table + "` (" + keystr + ") VALUES (" + formats + ")"
        #print sql
        try:
            with self.connection.cursor() as cursor:
                self.result = cursor.execute(sql, values)
            self.connection.commit()
        except pymysql.err.Warning as e:
            return True, e
        except pymysql.err.Error as e:
            return False, e
        return True, self.result

    def dropTab(self, table):
        if table is None or len(table)==0:
            return False, 'invalid table name'
        sql = 'drop table ' + table
        try:
            with self.connection.cursor() as cursor:
                self.result = cursor.execute(sql)
            self.connection.commit()
        except pymysql.err.Warning as e:
            return True, e
        except pymysql.err.Error as e:
            return False, e
        return True, self.result

    def dropTabs(self, tabs):
        for tab in tabs:
            self.dropTab(tab)

if __name__ == '__main__':
    conn = sqlconn('localhost',3307,'root','qlnEnae7', 'whut', 'utf8mb4', '/var/run/mysqld/mysqld.sock')
    if conn.connection.open:
        print 'opened'
        print conn.createTab('keyword',['id','value'],['bigint','varchar(100)'],['auto_increment','not null'],['id'])
        print conn.createTab('category',['id','parent_id','value'],['int','int','varchar(100)'],['auto_increment','',''],['id'])
        print conn.createTab('source',['id','category_id','value'],['int','int','varchar(100)'],['auto_increment','not null','not null'],
        ['id'],['category_id'],['category'],['id'])
        print conn.createTab('user',['id','name','email'],['bigint','varchar(100)','varchar(100)'],
        ['auto_increment','not null','not null'],['id'])
        print conn.createTab('attach',
        ['id','file_name','file_size','file_path','origin_addr'],
        ['bigint','varchar(120)','bigint','varchar(120)','varchar(120)'],
        ['auto_increment','not null','not null','not null','not null'],['id'])
        print conn.createTab('article',
        ['id','tid','title','link','content','keyword_id','category_id','datetime','source_id'],
         ['bigint','bigint','varchar(100)','varchar(120)','text','int','int','date','int'],
          ['auto_increment','not null','not null','not null','not null','not null','not null','not null','not null'],
           ['id'], [], [], [], 'utf8mb4')
        print conn.createTab('attrelate',['id','article_id','attach_id'],['bigint','bigint','bigint'],
        ['not null','not null','not null'],['id'],['article_id','attach_id'],['article','attach'],['id','id'])
        print conn.insert('article',['tid','title','link','content','keyword_id','category_id','datetime','source_id']
        ,[1,'test','http://i.whut.edu.cn','test text content',1,1,'2018-08-28',1])
        #conn.dropTabs(['keyword','source','category','attrelate','article','attach','user'])

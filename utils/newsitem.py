#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5
from webparser import webparser

class whutNewsItem(object):
    """News Item class for storing info of a single item."""
    def __init__(self, link, title):
        super(whutNewsItem, self).__init__()
        self.link = link
        self.title = title
        self.catlink = None
        self.catName = None
        self.content = None
        self.hash = None
        self.proxy = None
    def setCat(self, link, name):
        self.catlink = link
        self.catName = name
    def setContent(self, wc):
        self.content = wc
        #self.hash = hash_func.md5(self.content)
    def getContent(self, parser):
        self.content=whutNewsContent(self.title,title.link)
        #self.content.getContent(parser)

class whutNewsContent(object):
    """News Content class for storing main context of the news."""
    def __init__(self, title=None, url=None, content=None, date=None, publisher=None,attchs=[]):
        super(whutNewsContent, self).__init__()
        self.title = title
        self.url = url
        self.date = date
        self.publisher = publisher
        self.content = content
        self.attachs = attchs
        self.hash = hash_func.md5(self.content)
    def setDate(self, date):
        self.date = date
    def setPublisher(self, publisher):
        self.publisher = publisher
    def setAttachs(self, attachs):
        self.attachs = attachs
    def addAttachs(self, attachs):
        if type(attachs) is whutNewsAttachment:
            self.attachs.append(attachs)
        elif type(attachs) is list:
            self.attachs.extend(attachs)


class whutNewsAttachment(object):
    """News Attachment stores the link and name of the main content."""
    def __init__(self, name, link):
        super(whutNewsAttachment, self).__init__()
        self.name = name
        self.link = link
    def setName(self, name):
        self.name = name
    def setLink(self, link):
        self.link = link

class hash_func(object):
    """docstring for hash_func."""
    @classmethod
    def md5(self,content):
        hash_md5=md5()
        md5hash=hash_md5.copy()
        md5hash.update(content.encode('utf-8'))
        md5_res=md5hash.hexdigest()
        return md5_res

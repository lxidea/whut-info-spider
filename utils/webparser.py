#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fetcher import fetcher
import requests,datetime
from bs4 import BeautifulSoup

class webparser(object):
    """docstring for webparser"""
    def __init__(self, _url=None, proxy=None):
        super(webparser, self).__init__()
        self.url = _url
        self.proxy = proxy
        if _url is None:
            return
        response = fetcher.fetch(self.addSchema(_url),self.proxy)
        self.htmltext = response.text
        self.content = response.content
        self.status = response.status_code
        self.code_reason = response.reason
        self.time_cost = response.elapsed
        self.url = response.url
        #print self.url
        self.ok = response.ok
        self.encoding = response.encoding
        self.cookie = response.cookies
        self.header = response.headers
        self.is_redirect = response.is_redirect
        self.history = response.history
        #self.stew()
    def setProxy(self, _proxy):
        self.proxy = _proxy
    def addSchema(self, _url):
        if not _url.startswith('http'):
            return 'http://'+_url
        else:
            return _url
    def cleanMe(self, soup):
        [x.extract() for x in soup.find_all('script')]
        [x.extract() for x in soup.find_all('style')]
        [x.extract() for x in soup.find_all('meta')]
        [x.extract() for x in soup.find_all('noscript')]
        return soup
    def stew(self, _url):
        if _url!=None:
            response = fetcher.fetch(self.addSchema(_url),self.proxy)
            self.htmltext = response.text
            self.content = response.content
            self.status = response.status_code
            self.code_reason = response.reason
            self.time_cost = response.elapsed
            self.url = response.url
            self.ok = response.ok
            self.encoding = response.encoding
            self.cookie = response.cookies
            self.header = response.headers
            self.is_redirect = response.is_redirect
            self.history = response.history
        self.soup = BeautifulSoup(self.content, 'html.parser')
        return self.cleanMe(self.soup)
    def text(self):
        return self.htmltext
    def content(self):
        return self.content

if __name__ == '__main__':
    #page = fetcher.fetch("http://www.baidu.com")
    myparser = webparser("http://i.whut.edu.cn")
    soup = myparser.stew()
    grablist = [[addr.string.title(), addr.get("href")] for addr in soup.find("div","in_nav").find_all("a") if "i.whut.edu.cn/" in addr.get("href")]

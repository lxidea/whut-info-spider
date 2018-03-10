#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from fetcher import fetcher
import requests,datetime
from bs4 import BeautifulSoup

class webparser(object):
    """docstring for webparser"""
    def __init__(self, _url):
        super(webparser, self).__init__()
        response = fetcher.fetch(_url)
        self.htmltext = response.text
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
        #self.stew()
    def stew(self):
        self.soup = BeautifulSoup(self.htmltext, 'html.parser')
        return self.soup
    def text(self):
        return self.htmltext

if __name__ == '__main__':
    #page = fetcher.fetch("http://www.baidu.com")
    myparser = webparser("http://www.baidu.com")

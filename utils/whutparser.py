#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webparser import webparser
from bs4 import BeautifulSoup

class whutparser(object):
    """parser to fetch contents."""
    def __init__(self, arg):
        super(whutparser, self).__init__()
        self.arg = arg
        self.root = "i.whut.edu.cn"
        self.parser = webparser()
    def getCategory_and_facultyNews(self, arg):
        self.parser.stew(self.root)
        self.catlist = [[addr.string.title(), addr.get("href")] for addr in self.parser.soup.find("div","in_nav").find_all("a") if self.root in addr.get("href")]
        facultyName = [namespan.find("h2").string.split()[0] for namespan in self.parser.soup.find_all("div","tit_box6")]
        facultyLink = [c.find("a").get("href").replace('.',self.root) for c in soup.find_all("div","tit_box6")]
        self.faclist = [[name, facultyLink[idx]] for idx,name in enumerate(facultyName)]
    def getCatPage(self, arg):
        pass
    def getFacPage(self, arg):
        pass

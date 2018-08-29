#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webparser import webparser
from bs4 import BeautifulSoup
from newsitem import *
from markdownify import markdownify as md


class whutparser(object):
    """parser to fetch contents."""
    def __init__(self):
        super(whutparser, self).__init__()
        #self.arg = arg
        self.root = "i.whut.edu.cn"
        self.catlist = []
        self.faclist = []
        self.parser = webparser()
    def setProxy(self, proxy):
        self.parser.setProxy(proxy)
    def fullurl(self,_url,flag=None):
        """escape and recover the relative directory to full address"""
        if _url.startswith('.') and flag is not None:
            if self.parser.url.endswith('/') and _url.startswith('./'):
                return _url.replace('.',self.parser.url[:-1].replace('http://','',1),1)
            elif self.parser.url.find('index')>=0 and _url.startswith('./'):
                return _url.replace('.',self.parser.url[:self.parser.url.index('/index')].replace('http://','',1),1)
            elif self.parser.url.endswith('shtml') and _url.startswith('./'):
                return _url.replace('.',self.parser.url[:self.parser.url.index('/t')].replace('http://','',1),1)
            else:
                return _url.replace('.',self.parser.url.replace('http://','',1),1)
        elif _url.startswith('.'):
            return _url.replace('.',self.root,1)
        else:
            return _url
    def getCategory_and_facultyLink(self):
        """get faclist from homepage"""
        self.parser.stew(self.root)
        self.catlist = [[addr.string.title(), addr.get("href")] for addr in self.parser.soup.find("div","in_nav").find_all("a") if self.root in addr.get("href") and not addr.get("href").endswith(self.root)]
        facultyName = [namespan.find("h2").string.split()[0] for namespan in self.parser.soup.find_all("div","tit_box6")]
        facultyLink = [self.fullurl(c.find("a").get("href")) for c in self.parser.soup.find_all("div","tit_box6")]
        self.faclist = [[name, facultyLink[idx]] for idx,name in enumerate(facultyName)]

    def getNewsfromListPage(self, _url):
        """return a list of whutItems object"""
        #print _url
        self.parser.stew(_url)
        #return self.parser.soup
        lilist = self.parser.soup.find('ul','normal_list2').find_all('li')
        item1 = lilist[0]
        link_num = len(item1.find_all('a'))
        #when link number is equal to 2, then clist will make sense
        clist = [[self.fullurl(li.find_all('a')[0].get('href'),1),li.find_all('a')[0].string] for li in lilist]
        #the category name and link if they are available
        NewsList = [[self.fullurl(li.find_all('a')[-1].get('href'),1),li.find_all('a')[-1].get('title')] for li in lilist]
        #list contains all the news entries
        whutItems = []
        for idx, news in enumerate(NewsList):
            item = whutNewsItem(news[0],news[1])
            if (link_num==2):
                item.setCat(clist[idx][0],clist[idx][1])
            whutItems.append(item)
        return whutItems

    def getNewsListPages(self, name, root):
        """get page lists from category link"""
        url = root
        self.parser.stew(url)
        txt = self.parser.soup.find_all('script')[3].get_text()
        Keyword = 'createPageHTML'
        Keyword2 = Keyword + '('
        pageMaxStr = txt[txt.find(Keyword)+len(Keyword2):txt.find(',',txt.find(Keyword))]
        pageMax = int(pageMaxStr)
        pages = []
        for page in range(pageMax):
            if page!=0 and url.endswith('/'):
                url = url + 'index_' + str(page) + '.shtml'
            elif page!=0:
                url = url + '/index_' + str(page) + '.shtml'
            pages.append(url)
        return pages

    def getNewsListPage(self, para, page):
        """retrieve list page of news by category link and pageNum"""
        if len(self.catlist)==0 or len(self.faclist)==0:
            self.getCategory_andfacultyLink()
        if len(para) == 0:
            return None,None
        if 'index' in para:
            url = para[:para.find('index')-1]
        elif 'whut.edu.cn' in para:
            url = para
        else:
            idx = [li[0] for li in (self.catlist + self.faclist)].index(para)
            if idx<0:
                return -1,None
            url = [li[1] for li in (self.catlist + self.faclist)][idx]
        self.parser.stew(url)
        txt = self.parser.soup.find_all('script')[3].get_text()
        Keyword = 'createPageHTML'
        Keyword2 = Keyword + '('
        pageMaxStr = txt[txt.find(Keyword)+len(Keyword2):txt.find(',',txt.find(Keyword))]
        pageMax = int(pageMaxStr)
        if page>=pageMax or page<0:
            return pageMax,None
        if page!=0 and url.endswith('/'):
            url = url + 'index_' + str(page) + '.shtml'
        elif page!=0:
            url = url + '/index_' + str(page) + '.shtml'
        return pageMax,self.getNewsListPage(url)

    def getNewsPage(self, link):
        """return whutNewsContent Object by address"""
        self.parser.stew(link)
        content = md(self.parser.soup.find(id='art_content'))
        title = self.parser.soup.find('div','art_tit').h2.string
        info = self.parser.soup.find('div','art_info').find(text=True).strip(u'\xa0').split(u'\xa0')
        publisher = info[0][3:]
        date = info[-1][3:]
        url = self.parser.url
        return whutNewsContent(title,url,content,date,publisher)

    def getNewsContent(self, whutitem):
        """return whutNewsContent Object by whutitem object"""
        self.parser.stew(whutitem.link)
        content = md(self.parser.soup.find(id='art_content'))
        title = self.parser.soup.find('div','art_tit').h2.string
        info = self.parser.soup.find('div','art_info').find(text=True).strip(u'\xa0').split(u'\xa0')
        publisher = info[0][3:]
        date = info[-1][3:]
        url = self.parser.url
        attachments = self.parser.soup.find('div','file_box').find_all('a')
        attachs = None
        if len(attachments)>0:
            attachs = []
            for attach in attachments:
                attachs.append(whutNewsAttachment(attach.text,self.fullurl(attach.get('href'),1)))
        return whutNewsContent(title,url,content,date,publisher,attachs)

if __name__ == '__main__':
    proxy = {'http':'socks5://ftp.lxidea.org:26222'}
    myparser = whutparser()
    myparser.setProxy(proxy)
    myparser.getCategory_and_facultyLink()
    entries = myparser.getNewsfromListPage(myparser.catlist[0][1])
    for li in myparser.catlist:
        print li[0],li[1]
    soup, news = myparser.getNewsContent(entries[1])

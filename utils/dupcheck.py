#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bloomfilter

class dupcheck(object):
    """checking whether a url has been visited."""
    def __init__(self, config):
        super(dupcheck, self).__init__()
        self.config = config
        self.bf = bloomfilter(self.config.bf_config())

    def visited(self, url):
        return self.bf.isContains(url)

    def add(self, url):
        return url

    def pop(self, url):
        self.bf.remove(url)
        return url

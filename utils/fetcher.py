#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests,urllib
import requests_cache


requests_cache.install_cache('test_cache', backend='sqlite', expire_after=300)

class fetcher(object):
	"""class used to obtain context from the network"""
	def __init__(self, _proxy = None):
		super(fetcher, self).__init__()
		self._proxy = _proxy
	@staticmethod
	def fetch(_url, _proxy = None):
		if _proxy is None:
			return requests.get(_url)
		elif type(_proxy) is str and _proxy == "system":
			return requests.get(_url,proxies=urllib.getproxies(),
                                            timeout = 5)
		elif type(_proxy) is dict and _proxy.has_key("http"):
			proxy = dict()
			for protocal in ["http","https","ftp"]:
				if _proxy.has_key(protocal):
					proxy[protocal] = _proxy.get(protocal)
			if len(proxy)==0:
				proxy = None
			req = requests.get(_url,proxies=proxy,timeout=5)
			req.close()
			return req
	@staticmethod
	def clear_cache(self):
		requests_cache.clear()

if __name__ == '__main__':
	page = fetcher.fetch("http://i.whut.edu.cn")
	print page.status_code, page.reason
	print 'time used',page.elapsed

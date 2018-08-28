#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests,urllib
import requests_cache
import os


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
	def download_file(remote, local=None, _proxy=None):
		local_filename = local
		if local is None:
			local_filename = remote.split('/')[-1]
    	# NOTE the stream=True parameter
		if _proxy is None:
			r = requests.get(remote, stream=True)
		else:
			proxy = dict()
			for protocal in ["http","https","ftp"]:
				if _proxy.has_key(protocal):
					proxy[protocal] = _proxy.get(protocal)
			if len(proxy)==0:
				proxy = None
			r = requests.get(remote, stream=True, proxies=proxy)
		try:
			with open(local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024):
					if chunk: # filter out keep-alive new chunks
						f.write(chunk)
                		#f.flush() commented by recommendation from J.F.Sebastian
		except Error as e:
			return False, None, None
		return True,local_filename,os.path.realpath(local_filename)

	@staticmethod
	def clear_cache(self):
		requests_cache.clear()

if __name__ == '__main__':
	page = fetcher.fetch("http://i.whut.edu.cn")
	print page.status_code, page.reason
	print 'time used',page.elapsed
	print fetcher.download_file('http://i.whut.edu.cn/xytg/xyb/qcxy/201808/P020180828540288518086.pdf')

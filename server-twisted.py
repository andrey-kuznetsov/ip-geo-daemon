from twisted.web import server, resource
from twisted.internet import reactor

from datetime import datetime

import ipcache
import json

import random

ipcache = ipcache.IPCache()

def randIP():
	return '.'.join([str(random.randint(0, 255)) for _ in range(4)])

class HelloResource(resource.Resource):
	isLeaf = True
	numberRequests = 0

	def render_GET(self, request):
		self.numberRequests += 1
		request.setHeader('Content-Type', 'application/json')
		searchRes = ipcache.search(randIP())
		if not searchRes:
			searchRes = {'Error' : 'No IP range found'}
		return json.dumps(searchRes) + '\n'

reactor.listenTCP(8080, server.Site(HelloResource()))
reactor.run()

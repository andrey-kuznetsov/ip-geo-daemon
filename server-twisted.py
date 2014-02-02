from twisted.web import server, resource
from twisted.internet import reactor

from datetime import datetime

class HelloResource(resource.Resource):
	isLeaf = True
	numberRequests = 0
	
	def render_GET(self, request):
		self.numberRequests += 1
		request.setHeader('Content-Type', 'application/json')
		message = '{"City" : "Moscow", "Country" : "Russia", "Time" : "%s", "Index" : "%d"}' % (datetime.now(), self.numberRequests)
		return message + '\n'

reactor.listenTCP(8080, server.Site(HelloResource()))
reactor.run()
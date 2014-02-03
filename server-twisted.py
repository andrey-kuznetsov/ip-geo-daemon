from twisted.web import server, resource
from twisted.internet import reactor

from datetime import datetime

from sxgeo import SxGeo

class HelloResource(resource.Resource):
	isLeaf = True
	numberRequests = 0
	sxgeo = SxGeo('sxgeo/SxGeo_GeoIPCity.dat')

	def render_GET(self, request):
		self.numberRequests += 1
		request.setHeader('Content-Type', 'application/json')
		message = '{"City" : "Moscow", "Country" : "Russia", "Time" : "%s", "Index" : "%d", "db_items" : "%d"}' % (datetime.now(), self.numberRequests, self.sxgeo.db_items)
		return message + '\n'

reactor.listenTCP(8080, server.Site(HelloResource()))
reactor.run()
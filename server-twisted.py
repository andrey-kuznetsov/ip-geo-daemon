# -*- coding: utf-8 -*-

from twisted.web import server, resource
from twisted.internet import reactor

import json
import sys

import sxgeo

def loadConfigFromJsonFile(fileName):
	try:
		with open(fileName, 'r') as f:
			return json.load(f)
	except IOError:
		print >> sys.stderr, 'Unable to open configuration file '  + fileName
		sys.exit(1)
		
CONFIG = loadConfigFromJsonFile(sys.argv[1] if len(sys.argv) > 1 else 'server-config.json')

SXGEO_METHODS = ['getCityFull', 'getCity']

def makeErrorObj(message):
	return {'Error': message}

class SxGeoResource(resource.Resource):

	isLeaf = True

	sg = sxgeo.SxGeo(CONFIG['data_file'])

	def render_GET(self, request):
		request.setHeader('Content-Type', 'application/json; charset=utf-8')

		uriParts = [p for p in request.uri.split('?')[0].split('/') if p]
		if not uriParts or len(uriParts) > 1:
			result = makeErrorObj('Malformed URI')
		else:
			command = uriParts[0]
			if command == 'reload':
				# We're in the main loop thread, thus the following assignment is safe.
				self.sg = sxgeo.SxGeo(CONFIG['data_file'])
				result = True
			elif command in SXGEO_METHODS:
				ip = request.args.get('ip')
				if ip:
					result = getattr(self.sg, command)(ip[0]) # ip is a list, but we don't support multiple values
				else:
					result = makeErrorObj('No "ip" request argument provided')
			else:
				result = makeErrorObj('Unknown command: ' + command)

		return json.dumps(result, ensure_ascii = False) + '\n'


reactor.listenTCP(int(CONFIG['port']), server.Site(SxGeoResource()), interface = CONFIG['host'])
reactor.run()

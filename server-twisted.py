#!/usr/bin/python
# -*- coding: utf-8 -*-

from twisted.web import server, resource
from twisted.internet import reactor

import json

import sxgeo

import random

def randIP():
	return '.'.join([str(random.randint(0, 255)) for _ in range(4)])

def makeErrorObj(message):
	return {'Error': message}

class SxGeoResource(resource.Resource):

	sg = sxgeo.SxGeo('sxgeo/SxGeo_GeoIPCity.dat')

	isLeaf = True

	def render_GET(self, request):
		request.setHeader('Content-Type', 'application/json; charset=utf-8')

		uriParts = [p for p in request.uri.split('?')[0].split('/') if p]
		if not uriParts or len(uriParts) > 1:
			result = makeErrorObj('Malformed URI')
		else:
			command = uriParts[0]
			if command == 'reload':
				# TODO: RELOAD
				pass
			elif command in ['getCityFull', 'getCity', 'get_num']:
				ip = request.args.get('ip')
				if ip:
					result = getattr(self.sg, command)(ip[0]) # ip is a list, but we don't support multiple values
				else:
					result = makeErrorObj('No "ip" request argument provided')
			else:
				result = makeErrorObj('Unknown command: ' + command)

		#a = {'cn' : result['country_name']}
		return json.dumps(result, ensure_ascii = False) + '\n'

reactor.listenTCP(8081, server.Site(SxGeoResource()))
reactor.run()

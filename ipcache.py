#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
from collections import OrderedDict, namedtuple
import struct
import socket
import bisect

import countryMap

import time

RANGE_FIELDS = ['beginip', 'endip', 'cityid', 'regionid', 'country']
RangeRow = namedtuple('RangeRow', RANGE_FIELDS[1:])

REGION_FIELDS = ['id', 'name', 'country', 'parentid']
RegionRow = namedtuple('RegionRow', REGION_FIELDS[1:])

CITY_FIELDS = ['id', 'name', 'country', 'regionid']
CityRow = namedtuple('CityRow', CITY_FIELDS[1:])

COUNTRY_FIELDS = ['code', 'name']
CountryRow = namedtuple('CountryRow', COUNTRY_FIELDS[1:])

class IPCache:

	ranges = OrderedDict()
	rangeKeys = []
	
	regions = {}
	cities = {}
	countries = {}
	
	def __init__(self, mysqlHost, mysqlUser, mysqlPassword, mysqlDb):
		
		self.db = MySQLdb.connect(
			host = mysqlHost,
			user = mysqlUser,
			passwd = mysqlPassword,
			db = mysqlDb)

		self._fillDictFromDb('select %s from %s order by %s' % (', '.join(RANGE_FIELDS), 'geo_network', 'beginip'), self.ranges, 'RangeRow')
		self.rangeKeys = self.ranges.keys()
		
		self._fillDictFromDb('select %s from %s' % (', '.join(REGION_FIELDS), 'geo_regions'), self.regions, 'RegionRow')
		self._fillDictFromDb('select %s from %s' % (', '.join(CITY_FIELDS), 'geo_cities'), self.cities, 'CityRow')
		self._fillDictFromDb('select %s from %s' % (', '.join(COUNTRY_FIELDS), 'geo_countries'), self.countries, 'CountryRow')
		
		self.db.close()
		
	def _fillDictFromDb(self, queryString, rowsDict, rowType):
		cur = self.db.cursor() 
		cur.execute(queryString)
		for r in cur:
			rowsDict[r[0]] = globals()[rowType]._make(r[1:])

	def _findIPRange(self, ip):
		numIP = ip2int(ip)
		if numIP != None:
			i = bisect.bisect(self.rangeKeys, numIP)
			if i:
				row = self.ranges[self.rangeKeys[i-1]]
				if numIP <= row.endip:
					return row
		
	def _getRegionById(self, regionId):
		result = { 'region_name' : '', 'parent_region_id' : '', 'parent_region_name' : '' }
		region = self.regions.get(regionId)
		if region:
			result['region_name'] = region.name
			result['parent_region_id'] = region.parentid
			if region.parentid:
				result['parent_region_name'] = self.regions[region.parentid].name
		return result

	def _getCity(self, ip, addRegionInfo = False):
		ipRange = self._findIPRange(ip)
		if ipRange:
			result = { 'country_code' : ipRange.country, 'country_name' : countryMap.getCountryName(ipRange.country), 'region_id' : ipRange.regionid, 'city_id' : ipRange.cityid }
			city = self.cities.get(ipRange.cityid)
			if city:
				result['city'] = city.name
			if addRegionInfo:
				result.update(self._getRegionById(ipRange.regionid))
			return result

	def getCity(self, ip):
		return anyFalseToLiteralFalse(self._getCity(ip))
			
	def getCityFull(self, ip):
		return anyFalseToLiteralFalse(self._getCity(ip, addRegionInfo = True))

def ip2int(ip):
	try:
		packedIP = socket.inet_aton(ip)
	except socket.error:
		return None
		
	return struct.unpack("!I", packedIP)[0]

def anyFalseToLiteralFalse(value):
	return value if value else False
	
if __name__ == '__main__':
	"""
	Test
	"""
	ipcache = IPCache('localhost', '', '', 'test')
	ips = """221.193.237.73
		183.63.130.218
		222.124.143.9
		221.204.223.38
		220.162.237.125
		221.215.173.78
		203.161.24.62
		91.143.57.8
		85.26.164.199
		78.36.41.96
		2.60.0.77
		188.232.98.242
		188.232.98.242
		84.38.176.247
		116.228.55.217
		217.244.61.96""".split('\n')
	ips = [ip.strip() for ip in ips]
	t0 = time.time()
	for ip in ips:
		print ipcache.getCityFull(ip)
	print "Elapsed: %f" % (time.time() - t0)
	
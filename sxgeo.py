#!/usr/bin/python
# -*- coding: UTF-8 -*-
import struct
import socket

import countryMap

import time

# Translated from PHP-version, memory mode only.
class SxGeo:

	info = {}

	def __init__(self, db_file):

		with open(db_file, 'rb') as fh:

			header = fh.read(32)

			if header[0:3] != 'SxG':
				raise RuntimeError("Invalid file signature in %s" % db_file)

			info_labels = 'ver time type charset b_idx_len m_idx_len range db_items id_len max_region max_city region_size city_size'.split()
			info_values = struct.unpack('>BLBBBHHLBHHLL', header[3:])
			info = dict(zip(info_labels, info_values))

			if not info['b_idx_len'] or not info['m_idx_len'] or not info['range'] or not info['db_items'] or not info['time'] or not info['id_len']:
				raise RuntimeError('Invalid file header in %s' % db_file)

			self.b_idx_str = fh.read(info['b_idx_len'] * 4)
			self.m_idx_str = fh.read(info['m_idx_len'] * 4)
			self.range       = info['range']
			self.b_idx_len   = info['b_idx_len']
			self.m_idx_len   = info['m_idx_len']
			self.db_items    = info['db_items']
			self.id_len      = info['id_len']
			self.block_len   = 3 + self.id_len
			self.max_region  = info['max_region']
			self.max_city    = info['max_city']
			self.db_begin = fh.tell()

			self.db  = fh.read(self.db_items * self.block_len)
			self.regions_db = fh.read(info['region_size'])
			self.cities_db  = fh.read(info['city_size'])

			self.info['regions_begin'] = self.db_begin + self.db_items * self.block_len
			self.info['cities_begin']  = self.info['regions_begin'] + info['region_size']

			# 
			if self.id_len > 4:
				raise RuntimeError('Implementation assumption failed: id_len <= 4')


	def search_idx(self, ipn, min, max):
		while max - min > 8:
			offset = (min + max) >> 1
			index = offset * 4
			if ipn > self.m_idx_str[index:index+4]:
				min = offset
			else:
				max = offset
		while ipn > self.m_idx_str[min*4:min*4 + 4]:
			min_prev = min
			min += 1
			if min_prev >= max:
				break
		return min

	def search_db(self, base, ipn, min, max):
		if max - min > 1:
			ipn = ipn[1:]
			while max - min > 8:
				offset = (min + max) >> 1
				index = offset * self.block_len
				if ipn > base[index : index+3]:
					min = offset
				else:
					max = offset
			while ipn >= base[min*self.block_len:min*self.block_len + 3]:
				min_prev = min
				min += 1
				if min_prev >= max:
					break

			index = min * self.block_len - self.id_len
			# self.id_len <= 4 always. See __init__().
			return struct.unpack('>L', base[index : index + self.id_len].rjust(4, chr(0)))[0]
		else:
			index = min * self.block_len + 3
			return struct.unpack('>L', base[index : index + 3].rjust(4, chr(0)))[0]

	def get_num(self, ip):
		try:
			ip1n = int(ip.split('.')[0])
		except ValueError:
			return False
		# FIXME: refine unroutable IP ranges checks.
		if ip1n == 0 or ip1n == 10 or ip1n == 127 or ip1n >= self.b_idx_len:
			return False
		try:
			ipn = socket.inet_aton(ip)
		except socket.error:
			return False

		self.ip1c = chr(ip1n)
		# Находим блок данных индексе первых байт
		index = (ip1n - 1) * 4
		blocks = dict(zip(('min', 'max'), struct.unpack('>LL', self.b_idx_str[index : index + 8])))
		if blocks['max'] - blocks['min'] > self.range:
			# Ищем блок в основном индексе
			part = self.search_idx(ipn, blocks['min'] // self.range, blocks['max'] // self.range - 1)
			# Нашли номер блока в котором нужно искать IP, теперь находим нужный блок в БД
			min = part * self.range if part > 0 else 0
			max = self.db_items if part > self.m_idx_len else (part+1) * self.range
			# Нужно проверить чтобы блок не выходил за пределы блока первого байта
			if min < blocks['min']: min = blocks['min']
			if max > blocks['max']: max = blocks['max']
		else:
			min = blocks['min']
			max = blocks['max']
		len = max - min
		# Находим нужный диапазон в БД
		return self.search_db(self.db, ipn, min, max - 1)

	def parseCity(self, seek):
		raw = self.cities_db[seek : seek + self.max_city]
		self.city = dict(zip(('rpos', 'country_id', 'region_id', 'city_id'), struct.unpack('>LBHH', raw[0:9])))
		self.city['country_code']  = cc2iso[self.city['country_id']]
		self.city['country_name']  = countryMap.getCountryName(self.city['country_code'])
		self.city['city'] = raw[9:].split('\0')[0]
		return self.city

	def parseRegion(self, region_seek):
		if region_seek > 0:
			region = self.regions_db[region_seek : region_seek + self.max_region].split('\0')
			self.city['region_name'] = region[0]
			self.city['parent_region_id'] = region[1]
			self.city['parent_region_name'] = region[2]
		else:
			self.city['region_name'] = self.city['parent_region_id'] = self.city['parent_region_name'] = ''

	def get(self, ip):
		return self.getCity(ip) if self.max_city else self.getCountry(ip)

	def getCountry(self, ip):
		return self.cc2iso[self.get_num(ip)]

	def getCountryId(self, ip):
		return self.get_num(ip)

	def getCity(self, ip):
		seek = self.get_num(ip)
		if seek > 0:
			return self.parseCity(seek)
		else:
			return False

	def getCityFull(self, ip):
		seek = self.get_num(ip)
		if seek > 0:
			self.parseCity(seek)
			self.parseRegion(self.city['rpos'])
			return self.city
		else:
			return False

cc2iso = [
	'', 'AP', 'EU', 'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AN', 'AO', 'AQ',
	'AR', 'AS', 'AT', 'AU', 'AW', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH',
	'BI', 'BJ', 'BM', 'BN', 'BO', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA',
	'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU',
	'CV', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG',
	'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'FX', 'GA', 'GB',
	'GD', 'GE', 'GF', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT',
	'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN',
	'IO', 'IQ', 'IR', 'IS', 'IT', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM',
	'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS',
	'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN',
	'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA',
	'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ', 'OM', 'PA',
	'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY',
	'QA', 'RE', 'RO', 'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI',
	'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'ST', 'SV', 'SY', 'SZ', 'TC', 'TD',
	'TF', 'TG', 'TH', 'TJ', 'TK', 'TM', 'TN', 'TO', 'TL', 'TR', 'TT', 'TV', 'TW',
	'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN',
	'VU', 'WF', 'WS', 'YE', 'YT', 'RS', 'ZA', 'ZM', 'ME', 'ZW', 'A1', 'A2', 'O1',
	'AX', 'GG', 'IM', 'JE', 'BL', 'MF'
	]

if __name__ == '__main__':
	"""
	Test
	"""
	sg = SxGeo('sxgeo/SxGeo_GeoIPCity.dat')
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
		print sg.getCityFull(ip)
	print "Elapsed: %f" % (time.time() - t0)

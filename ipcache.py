import MySQLdb
from collections import OrderedDict, namedtuple
import struct
import socket
import bisect

MYSQL_HOST = 'localhost'
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DB = 'test'

NETWORK_FIELDS = ['beginip', 'endip', 'cityid', 'regionid', 'country']
NetworkRow = namedtuple('NetworkRow', NETWORK_FIELDS[1:] 
	+ ['avgtime']) # crutch!

class IPCache:

	cache = OrderedDict()
	cache_keys = []
	
	def __init__(self):
		"""
		TODO: add auth parameters.
		"""

		db = MySQLdb.connect(
			host=MYSQL_HOST,
			user=MYSQL_USER,
			passwd=MYSQL_PASSWORD,
			db=MYSQL_DB)

		cur = db.cursor() 

		cur.execute('select ' + ', '.join(NETWORK_FIELDS) + ' from geo_network order by beginip')

		while True:
			row = cur.fetchone()
			if not row:
				break
			
			beginip = row[0]
			self.cache[beginip] = NetworkRow._make(row[1:]
				+ (0,)) # crutch!

		self.cache_keys = self.cache.keys()

	def search(self, ip):
		numIP = ip2int(ip)
		i = bisect.bisect(self.cache_keys, numIP)
		if not i:
			return None
		row = self.cache[self.cache_keys[i-1]]
		if numIP > row.endip:
			return None
		return (i-1, row)

def ip2int(ip):
	return struct.unpack("!I", socket.inet_aton(ip))[0]

def int2ip(n):
	return socket.inet_ntoa(struct.pack("!I", n))
	
	
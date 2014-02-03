import struct

class SxGeo:

	info = {}

	def __init__(self, db_file = 'SxGeo.dat'):

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

			# Memory mode only.
			self.db  = fh.read(self.db_items * self.block_len);
			self.regions_db = fh.read(info['region_size']);
			self.cities_db  = fh.read(info['city_size']);

			self.info['regions_begin'] = self.db_begin + self.db_items * self.block_len
			self.info['cities_begin']  = self.info['regions_begin'] + info['region_size']
		
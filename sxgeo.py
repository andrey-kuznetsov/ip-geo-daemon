import struct
import socket

# Translated from PHP-version, menory mode only.
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

			self.db  = fh.read(self.db_items * self.block_len);
			self.regions_db = fh.read(info['region_size']);
			self.cities_db  = fh.read(info['city_size']);

			self.info['regions_begin'] = self.db_begin + self.db_items * self.block_len
			self.info['cities_begin']  = self.info['regions_begin'] + info['region_size']

			# 
			if self.id_len > 4:
				raise RuntimeError('Implementation assumption failed: id_len <= 4')


	def search_idx(self, ipn, min, max):
		while max - min > 8:
			offset = (min + max) >> 1
			index = offsed * 4
			if ipn > self.m_idx_str[index:index+4]:
				min = offset
			else:
				max = offset
		}
		while ipn > self.m_idx_str[min*4:min*4 + 4]:
			min_prev = min
			min += 1
			if min_prev >= max:
				break
		return min

	def search_db(self, str, ipn, min, max):
		if max - min > 1:
			ipn = ipn[1:];
			while max - min > 8:
				offset = (min + max) >> 1
				index = offset * self.block_len
				if ipn > str[index:index+3]:
					min = offset;
				else 
					max = offset;
			}
			while ipn > str[min*self.block_len:min*self.block_len + 3]:
				min_prev = min
				min += 1
				if min_prev >= max:
					break
			index = min * self.block_len - self.id_len
			# self.id_len <= 4 always. See __init__().
			return struct.unpack('>L', str[index:index + self.id_len].zfill(4))
		else:
			index = min * self.block_len + 3
			return struct.unpack('>L', bin2hex(str[index:index + 3].zfill(4)))

	@staticmethod 
	def bin2hex(bin_str):
		return ''.join([hex(c)[2:].zfill(2) for c in bin_str])

	def get_num(self, ip){
		ip1n = ip.split('.')[0];
		# FIXME: refine unroutable IP ranges checks.
		if ip1n == 0 or ip1n == 10 or ip1n == 127 or ip1n >= self.b_idx_len:
			return False
		try
			ipn = socket.inet_aton(ip)
		except socket.error:
			return False

		# TODO: Dig from here...

		$this->ip1c = chr($ip1n);
		// Находим блок данных индексе первых байт
		if ($this->batch_mode){
			$blocks = array('min' => $this->b_idx_arr[$ip1n-1], 'max' => $this->b_idx_arr[$ip1n]);
		}
		else {
			$blocks = unpack("Nmin/Nmax", substr($this->b_idx_str, ($ip1n - 1) * 4, 8));
		}
		if ($blocks['max'] - $blocks['min'] > $this->range){
			// Ищем блок в основном индексе
			$part = $this->search_idx($ipn, floor($blocks['min'] / $this->range), floor($blocks['max'] / $this->range)-1);
			// Нашли номер блока в котором нужно искать IP, теперь находим нужный блок в БД
			$min = $part > 0 ? $part * $this->range : 0;
			$max = $part > $this->m_idx_len ? $this->db_items : ($part+1) * $this->range;
			// Нужно проверить чтобы блок не выходил за пределы блока первого байта
			if($min < $blocks['min']) $min = $blocks['min'];
			if($max > $blocks['max']) $max = $blocks['max'];
		}
		else {
			$min = $blocks['min'];
			$max = $blocks['max'];
		}
		$len = $max - $min;
		// Находим нужный диапазон в БД
		if ($this->memory_mode) {
			return $this->search_db($this->db, $ipn, $min, $max);
		}
		else {
			fseek($this->fh, $this->db_begin + $min * $this->block_len);
			return $this->search_db(fread($this->fh, $len * $this->block_len), $ipn, 0, $len-1);
		}

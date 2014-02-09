<?php
/***************************************************************************\
| Sypex Geo                  version 2.2.0                                  |
| (c)2006-2013 zapimir       zapimir@zapimir.net       http://sypex.net/    |
| (c)2006-2013 BINOVATOR     info@sypex.net                                 |
|---------------------------------------------------------------------------|
|     created: 2006.10.17 18:33              modified: 2014.01.30 12:46     |
|---------------------------------------------------------------------------|
| Sypex Geo is released under the terms of the BSD license                  |
|   http://sypex.net/bsd_license.txt                                        |
\***************************************************************************/

define ('SXGEO_FILE', 0);
define ('SXGEO_MEMORY', 1);
define ('SXGEO_BATCH',  2);
class SxGeo {
	protected $fh;
	protected $ip1c;
	protected $info;
	protected $range;
	protected $db_begin;
	protected $b_idx_str;
	protected $m_idx_str;
	protected $b_idx_arr;
	protected $m_idx_arr;
	protected $m_idx_len;
	protected $db_items;
	protected $db;
	protected $regions_db;
	protected $cities_db;
	public $cc2iso = array(
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
	);

	public $batch_mode  = false;
	public $memory_mode = false;

	public function __construct($db_file = 'SxGeo.dat', $type = SXGEO_FILE){
		$this->fh = fopen($db_file, 'rb');
		// Сначала убеждаемся, что есть файл базы данных
		$header = fread($this->fh, 32);
		if(substr($header, 0, 3) != 'SxG') die("Can't open {$db_file}\n");
		$info = unpack('Cver/Ntime/Ctype/Ccharset/Cb_idx_len/nm_idx_len/nrange/Ndb_items/Cid_len/nmax_region/nmax_city/Nregion_size/Ncity_size', substr($header, 3));
		if($info['b_idx_len'] * $info['m_idx_len'] * $info['range'] * $info['db_items'] * $info['time'] * $info['id_len'] == 0) die("Wrong file format {$db_file}\n");
		$this->b_idx_str = fread($this->fh, $info['b_idx_len'] * 4);
		$this->m_idx_str = fread($this->fh, $info['m_idx_len'] * 4);
		$this->range       = $info['range'];
		$this->b_idx_len   = $info['b_idx_len'];
		$this->m_idx_len   = $info['m_idx_len'];
		$this->db_items    = $info['db_items'];
		$this->id_len      = $info['id_len'];
		$this->block_len   = 3 + $this->id_len;
		$this->max_region  = $info['max_region'];
		$this->max_city    = $info['max_city'];
		$this->batch_mode  = $type & SXGEO_BATCH;
		$this->memory_mode = $type & SXGEO_MEMORY;
		$this->db_begin = ftell($this->fh);
		if ($this->batch_mode) { // Значительное ускорение блока
			$this->b_idx_arr = array_values(unpack("N*", $this->b_idx_str)); // Быстрее в 5 раз, чем с циклом
			unset ($this->b_idx_str);
			$this->m_idx_arr = str_split($this->m_idx_str, 4); // Быстрее в 5 раз чем с циклом
			unset ($this->m_idx_str);
		}
		if ($this->memory_mode) {
			$this->db  = fread($this->fh, $this->db_items * $this->block_len);
			$this->regions_db = fread($this->fh, $info['region_size']);
			$this->cities_db  = fread($this->fh, $info['city_size']);
		}
		$this->info['regions_begin'] = $this->db_begin + $this->db_items * $this->block_len;
		$this->info['cities_begin']  = $this->info['regions_begin'] + $info['region_size'];
	}

	protected function search_idx($ipn, $min, $max){
		if($this->batch_mode){
			while($max - $min > 8){
				$offset = ($min + $max) >> 1;
				if ($ipn > $this->m_idx_arr[$offset]) $min = $offset;
				else $max = $offset;
			}
			while ($ipn > $this->m_idx_arr[$min] && $min++ < $max){};
		}
		else {
			while($max - $min > 8){
				$offset = ($min + $max) >> 1;
				if ($ipn > substr($this->m_idx_str, $offset*4, 4)) $min = $offset;
				else $max = $offset;
			}
			while ($ipn > substr($this->m_idx_str, $min*4, 4) && $min++ < $max){};
		}
		return  $min;
	}

	protected function search_db($str, $ipn, $min, $max){
		if($max - $min > 1) {
			$ipn = substr($ipn, 1);
			while($max - $min > 8){
				$offset = ($min + $max) >> 1;
				if ($ipn > substr($str, $offset * $this->block_len, 3)) $min = $offset;
				else $max = $offset;
			}
			while ($ipn >= substr($str, $min * $this->block_len, 3) && $min++ < $max){};
		}
		else {
			return hexdec(bin2hex(substr($str, $min * $this->block_len + 3 , 3)));
		}
		return hexdec(bin2hex(substr($str, $min * $this->block_len - $this->id_len, $this->id_len)));
	}

	public function get_num($ip){
		$ip1n = (int)$ip; // Первый байт
		if($ip1n == 0 || $ip1n == 10 || $ip1n == 127 || $ip1n >= $this->b_idx_len || false === ($ipn = ip2long($ip))) return false;
		$ipn = pack('N', $ipn);
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
	}
	protected function parseCity($seek){

		if($this->memory_mode){
			$raw = substr($this->cities_db, $seek, $this->max_city);
		}
		else{
			fseek($this->fh, $this->info['cities_begin'] + $seek);
			$raw = fread($this->fh, $this->max_city);
		}
		$this->city = unpack('Nrpos/Ccountry_id/nregion_id/ncity_id', $raw);
		$this->city['country_code']  = $this->cc2iso[$this->city['country_id']];
		$this->city['country_name']  = $this->getCountryName($this->city['country_code']);

		$c = explode("\0", substr($raw, 9),2);
		$this->city['city'] = $c[0];
		return $this->city;
	}

	protected function parseRegion($region_seek){

		if($region_seek > 0){
			if($this->memory_mode){
				$region = explode("\0",substr($this->regions_db, $region_seek, $this->max_region));
			}
			else{
				fseek($this->fh, $this->info['regions_begin'] + $region_seek);
				$region = explode("\0", fread($this->fh, $this->max_region));
			}
			$this->city['region_name'] = $region[0];
			$this->city['parent_region_id'] = $region[1];
			$this->city['parent_region_name'] = $region[2];
		}
		else{
			$this->city['region_name'] = $this->city['parent_region_id'] = $this->city['parent_region_name'] = '';
		}
	}

	public function get($ip){
		return $this->max_city ? $this->getCity($ip) : $this->getCountry($ip);
	}
	public function getCountry($ip){
		return $this->cc2iso[$this->get_num($ip)];
	}
	public function getCountryId($ip){
		return $this->get_num($ip);
	}
	public function getCity($ip){
		$seek = $this->get_num($ip);
		if($seek > 0) return $this->parseCity($seek);
		else return false;
	}
	public function getCityFull($ip){
		$t0 = gettimeofday(true);
		$seek = $this->get_num($ip);
		if($seek > 0) {
			$this->parseCity($seek);
			$this->parseRegion($this->city['rpos']);
			return $this->city;
		} else {
			return false;
		}
	}
	public function getCountryName($cc){
		$a = array('AU' => 'Австралия',
			'MY' => 'Малайзия',
			'KR' => 'Южная Корея',
			'CN' => 'Китай',
			'JP' => 'Япония',
			'IN' => 'Индия',
			'TW' => 'Тайвань',
			'HK' => 'Гонконг',
			'TH' => 'Таиланд',
			'VN' => 'Вьетнам',
			'FR' => 'Франция',
			'IT' => 'Италия',
			'AE' => 'ОАЭ',
			'SE' => 'Швеция',
			'KZ' => 'Казахстан',
			'PT' => 'Португалия',
			'GR' => 'Греция',
			'SA' => 'Саудовская Аравия',
			'RU' => 'Российская Федерация',
			'GB' => 'Великобритания',
			'DK' => 'Дания',
			'US' => 'США',
			'CA' => 'Канада',
			'MX' => 'Мексика',
			'BM' => 'Бермуды',
			'PR' => 'Пуэрто Рико',
			'VI' => 'Виргинские Острова США',
			'DE' => 'Германия',
			'IR' => 'Иран',
			'BO' => 'Боливия',
			'MS' => 'Монтсеррат',
			'NL' => 'Нидерланды',
			'IL' => 'Израиль',
			'ES' => 'Испания',
			'BS' => 'Багамские острова',
			'VC' => 'Сент-Винсент и Гренадины',
			'CL' => 'Чили',
			'NC' => 'Новая Каледония',
			'AR' => 'Аргентина',
			'DM' => 'Доминика',
			'SG' => 'Сингапур',
			'NP' => 'Непал',
			'PH' => 'Филиппины',
			'ID' => 'Индонезия',
			'PK' => 'Пакистан',
			'TK' => 'Токелау',
			'NZ' => 'Новая Зеландия',
			'KH' => 'Камбоджа',
			'MO' => 'Макау',
			'PG' => 'Папуа Новая Гвинея',
			'MV' => 'Мальдивские острова',
			'AF' => 'Афганистан',
			'BD' => 'Бангладеш',
			'IE' => 'Ирландия',
			'BE' => 'Бельгия',
			'BZ' => 'Белиз',
			'BR' => 'Бразилия',
			'CH' => 'Швейцария',
			'ZA' => 'ЮАР',
			'EG' => 'Египет',
			'NG' => 'Нигерия',
			'TZ' => 'Танзания',
			'ZM' => 'Замбия',
			'SN' => 'Сенегал',
			'GH' => 'Гана',
			'SD' => 'Судан',
			'CM' => 'Камерун',
			'MW' => 'Малави',
			'AO' => 'Ангола',
			'KE' => 'Кения',
			'GA' => 'Габон',
			'ML' => 'Мали',
			'BJ' => 'Бенин',
			'MG' => 'Мадагаскар',
			'TD' => 'Чад',
			'BW' => 'Ботсвана',
			'LY' => 'Ливия',
			'CV' => 'Кабо-Верде',
			'RW' => 'Руанда',
			'MZ' => 'Мозамбик',
			'GM' => 'Гамбия',
			'LS' => 'Лесото',
			'MU' => 'Маврикий',
			'CG' => 'Конго',
			'UG' => 'Уганда',
			'BF' => 'Буркина Фасо',
			'SL' => 'Сьерра-Леоне',
			'SO' => 'Сомали',
			'ZW' => 'Зимбабве',
			'CD' => 'Демократическая Республика Конго',
			'NE' => 'Нигер',
			'CF' => 'Центрально-Африканская Республика',
			'SZ' => 'Свазиленд',
			'TG' => 'Того',
			'GN' => 'Гвинея',
			'LR' => 'Либерия',
			'SC' => 'Сейшеллы',
			'MA' => 'Марокко',
			'DZ' => 'Алжир',
			'MR' => 'Мавритания',
			'NA' => 'Намибия',
			'DJ' => 'Джибути',
			'KM' => 'Коморские острова',
			'RE' => 'Реюньон',
			'GQ' => 'Экваториальная Гвинея',
			'TN' => 'Тунис',
			'TR' => 'Турция',
			'PL' => 'Польша',
			'LV' => 'Латвия',
			'UA' => 'Украина',
			'BY' => 'Беларусь',
			'CZ' => 'Чехия',
			'PS' => 'Палестина',
			'IS' => 'Исландия',
			'CY' => 'Кипр',
			'HU' => 'Венгрия',
			'SK' => 'Словакия',
			'RS' => 'Сербия',
			'BG' => 'Болгария',
			'OM' => 'Оман',
			'RO' => 'Румыния',
			'GE' => 'Грузия',
			'NO' => 'Норвегия',
			'AM' => 'Армения',
			'AT' => 'Австрия',
			'AL' => 'Албания',
			'SI' => 'Словения',
			'PA' => 'Панама',
			'BN' => 'Бруней',
			'LK' => 'Шри-Ланка',
			'ME' => 'Черногория',
			'EU' => 'Европейский Союз',
			'TJ' => 'Таджикистан',
			'IQ' => 'Ирак',
			'LB' => 'Ливан',
			'MD' => 'Молдова',
			'FI' => 'Финляндия',
			'EE' => 'Эстония',
			'BA' => 'Босния и Герцеговина',
			'KW' => 'Кувейт',
			'AX' => 'Аландские острова',
			'LT' => 'Литва',
			'LU' => 'Люксембург',
			'AG' => 'Антигуа и Барбуда',
			'MK' => 'Македония',
			'SM' => 'Сан-Марино',
			'MT' => 'Мальта',
			'FK' => 'Фолклендские острова',
			'BH' => 'Бахрейн',
			'UZ' => 'Узбекистан',
			'AZ' => 'Азербайджан',
			'MC' => 'Монако',
			'HT' => 'Гаити',
			'GU' => 'Гуам',
			'JM' => 'Ямайка',
			'UM' => 'Внешние малые острова США',
			'FM' => 'Микронезия',
			'EC' => 'Эквадор',
			'PE' => 'Перу',
			'KY' => 'Каймановы острова',
			'CO' => 'Колумбия',
			'HN' => 'Гондурас',
			'AN' => 'Антильские острова',
			'YE' => 'Йемен',
			'VG' => 'Британские Виргинские острова',
			'SY' => 'Сирия',
			'NI' => 'Никарагуа',
			'DO' => 'Доминиканская республика',
			'GD' => 'Гренада',
			'GT' => 'Гватемала',
			'CR' => 'Коста-Рика',
			'SV' => 'Сальвадор',
			'VE' => 'Венесуэла',
			'BB' => 'Барбадос',
			'TT' => 'Тринидад и Тобаго',
			'BV' => 'Буве',
			'MH' => 'Маршалловы острова',
			'CK' => 'Острова Кука',
			'GI' => 'Гибралтар',
			'PY' => 'Парагвай',
			'WS' => 'Самоа',
			'KN' => 'Сент Китс и Невис',
			'FJ' => 'Фиджи',
			'UY' => 'Уругвай',
			'MP' => 'Северные Марианские острова',
			'PW' => 'Палау',
			'QA' => 'Катар',
			'JO' => 'Иордания',
			'AS' => 'Американское Самоа',
			'TC' => 'Туркс и Кейкос',
			'LC' => 'Святая Люсия',
			'MN' => 'Монголия',
			'VA' => 'Ватикан',
			'AW' => 'Арулько',
			'GY' => 'Гайана',
			'SR' => 'Суринам',
			'IM' => 'Остров Мэн',
			'VU' => 'Вануату',
			'HR' => 'Хорватия',
			'AI' => 'Ангуилья',
			'PM' => 'Сен-Пьер и Микелон',
			'GP' => 'Гваделупа',
			'MF' => 'Сен-Мартен',
			'GG' => 'Гернси',
			'BI' => 'Бурунди',
			'TM' => 'Туркменистан',
			'KG' => 'Кыргызстан',
			'MM' => 'Мьянма',
			'BT' => 'Бутан',
			'LI' => 'Лихтенштейн',
			'FO' => 'Фарерские острова',
			'ET' => 'Эфиопия',
			'MQ' => 'Мартиника',
			'JE' => 'Джерси',
			'AD' => 'Андорра',
			'AQ' => 'Антарктида',
			'IO' => 'Британская территория в Индийском океане',
			'GL' => 'Гренландия',
			'GW' => 'Гвинея-Бисау',
			'ER' => 'Эритрея',
			'WF' => 'Уоллис и Футуна',
			'PF' => 'Французская Полинезия',
			'CU' => 'Куба',
			'TO' => 'Тонга',
			'TL' => 'Восточный Тимор',
			'ST' => 'Сан-Томе и Принсипи',
			'GF' => 'Французская Гвинея',
			'SB' => 'Соломоновы острова',
			'TV' => 'Тувалу',
			'KI' => 'Кирибати',
			'NU' => 'Ниуэ',
			'NF' => 'Норфолк',
			'NR' => 'Науру',
			'YT' => 'Майотта',
			'PN' => 'Питкэрн',
			'CI' => 'Кот-д\'Ивуар',
			'LA' => 'Лаос',
			'KP' => 'Корейская Народно-Демократическая Республика',
			'SJ' => 'Свальбард и Ян-Майен',
			'SH' => 'Остров Святой Елены',
			'CC' => 'Кокосовые острова',
			'EH' => 'Западная Сахара');
		return isset($a[$cc]) ? $a[$cc] : '';
	}
}
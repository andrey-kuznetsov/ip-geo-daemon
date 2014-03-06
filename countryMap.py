# -*- coding: UTF-8 -*-
def getCountryName(countryCode):
	try:
		result = iso2country[countryCode]
	except KeyError:
		result = ''
	return result if result else ''

iso2country = {'AU' : 'Австралия',
	'MY' : 'Малайзия',
	'KR' : 'Южная Корея',
	'CN' : 'Китай',
	'JP' : 'Япония',
	'IN' : 'Индия',
	'TW' : 'Тайвань',
	'HK' : 'Гонконг',
	'TH' : 'Таиланд',
	'VN' : 'Вьетнам',
	'FR' : 'Франция',
	'IT' : 'Италия',
	'AE' : 'ОАЭ',
	'SE' : 'Швеция',
	'KZ' : 'Казахстан',
	'PT' : 'Португалия',
	'GR' : 'Греция',
	'SA' : 'Саудовская Аравия',
	'RU' : 'Российская Федерация',
	'GB' : 'Великобритания',
	'DK' : 'Дания',
	'US' : 'США',
	'CA' : 'Канада',
	'MX' : 'Мексика',
	'BM' : 'Бермуды',
	'PR' : 'Пуэрто Рико',
	'VI' : 'Виргинские Острова США',
	'DE' : 'Германия',
	'IR' : 'Иран',
	'BO' : 'Боливия',
	'MS' : 'Монтсеррат',
	'NL' : 'Нидерланды',
	'IL' : 'Израиль',
	'ES' : 'Испания',
	'BS' : 'Багамские острова',
	'VC' : 'Сент-Винсент и Гренадины',
	'CL' : 'Чили',
	'NC' : 'Новая Каледония',
	'AR' : 'Аргентина',
	'DM' : 'Доминика',
	'SG' : 'Сингапур',
	'NP' : 'Непал',
	'PH' : 'Филиппины',
	'ID' : 'Индонезия',
	'PK' : 'Пакистан',
	'TK' : 'Токелау',
	'NZ' : 'Новая Зеландия',
	'KH' : 'Камбоджа',
	'MO' : 'Макау',
	'PG' : 'Папуа Новая Гвинея',
	'MV' : 'Мальдивские острова',
	'AF' : 'Афганистан',
	'BD' : 'Бангладеш',
	'IE' : 'Ирландия',
	'BE' : 'Бельгия',
	'BZ' : 'Белиз',
	'BR' : 'Бразилия',
	'CH' : 'Швейцария',
	'ZA' : 'ЮАР',
	'EG' : 'Египет',
	'NG' : 'Нигерия',
	'TZ' : 'Танзания',
	'ZM' : 'Замбия',
	'SN' : 'Сенегал',
	'GH' : 'Гана',
	'SD' : 'Судан',
	'CM' : 'Камерун',
	'MW' : 'Малави',
	'AO' : 'Ангола',
	'KE' : 'Кения',
	'GA' : 'Габон',
	'ML' : 'Мали',
	'BJ' : 'Бенин',
	'MG' : 'Мадагаскар',
	'TD' : 'Чад',
	'BW' : 'Ботсвана',
	'LY' : 'Ливия',
	'CV' : 'Кабо-Верде',
	'RW' : 'Руанда',
	'MZ' : 'Мозамбик',
	'GM' : 'Гамбия',
	'LS' : 'Лесото',
	'MU' : 'Маврикий',
	'CG' : 'Конго',
	'UG' : 'Уганда',
	'BF' : 'Буркина Фасо',
	'SL' : 'Сьерра-Леоне',
	'SO' : 'Сомали',
	'ZW' : 'Зимбабве',
	'CD' : 'Демократическая Республика Конго',
	'NE' : 'Нигер',
	'CF' : 'Центрально-Африканская Республика',
	'SZ' : 'Свазиленд',
	'TG' : 'Того',
	'GN' : 'Гвинея',
	'LR' : 'Либерия',
	'SC' : 'Сейшеллы',
	'MA' : 'Марокко',
	'DZ' : 'Алжир',
	'MR' : 'Мавритания',
	'NA' : 'Намибия',
	'DJ' : 'Джибути',
	'KM' : 'Коморские острова',
	'RE' : 'Реюньон',
	'GQ' : 'Экваториальная Гвинея',
	'TN' : 'Тунис',
	'TR' : 'Турция',
	'PL' : 'Польша',
	'LV' : 'Латвия',
	'UA' : 'Украина',
	'BY' : 'Беларусь',
	'CZ' : 'Чехия',
	'PS' : 'Палестина',
	'IS' : 'Исландия',
	'CY' : 'Кипр',
	'HU' : 'Венгрия',
	'SK' : 'Словакия',
	'RS' : 'Сербия',
	'BG' : 'Болгария',
	'OM' : 'Оман',
	'RO' : 'Румыния',
	'GE' : 'Грузия',
	'NO' : 'Норвегия',
	'AM' : 'Армения',
	'AT' : 'Австрия',
	'AL' : 'Албания',
	'SI' : 'Словения',
	'PA' : 'Панама',
	'BN' : 'Бруней',
	'LK' : 'Шри-Ланка',
	'ME' : 'Черногория',
	'EU' : 'Европейский Союз',
	'TJ' : 'Таджикистан',
	'IQ' : 'Ирак',
	'LB' : 'Ливан',
	'MD' : 'Молдова',
	'FI' : 'Финляндия',
	'EE' : 'Эстония',
	'BA' : 'Босния и Герцеговина',
	'KW' : 'Кувейт',
	'AX' : 'Аландские острова',
	'LT' : 'Литва',
	'LU' : 'Люксембург',
	'AG' : 'Антигуа и Барбуда',
	'MK' : 'Македония',
	'SM' : 'Сан-Марино',
	'MT' : 'Мальта',
	'FK' : 'Фолклендские острова',
	'BH' : 'Бахрейн',
	'UZ' : 'Узбекистан',
	'AZ' : 'Азербайджан',
	'MC' : 'Монако',
	'HT' : 'Гаити',
	'GU' : 'Гуам',
	'JM' : 'Ямайка',
	'UM' : 'Внешние малые острова США',
	'FM' : 'Микронезия',
	'EC' : 'Эквадор',
	'PE' : 'Перу',
	'KY' : 'Каймановы острова',
	'CO' : 'Колумбия',
	'HN' : 'Гондурас',
	'AN' : 'Антильские острова',
	'YE' : 'Йемен',
	'VG' : 'Британские Виргинские острова',
	'SY' : 'Сирия',
	'NI' : 'Никарагуа',
	'DO' : 'Доминиканская республика',
	'GD' : 'Гренада',
	'GT' : 'Гватемала',
	'CR' : 'Коста-Рика',
	'SV' : 'Сальвадор',
	'VE' : 'Венесуэла',
	'BB' : 'Барбадос',
	'TT' : 'Тринидад и Тобаго',
	'BV' : 'Буве',
	'MH' : 'Маршалловы острова',
	'CK' : 'Острова Кука',
	'GI' : 'Гибралтар',
	'PY' : 'Парагвай',
	'WS' : 'Самоа',
	'KN' : 'Сент Китс и Невис',
	'FJ' : 'Фиджи',
	'UY' : 'Уругвай',
	'MP' : 'Северные Марианские острова',
	'PW' : 'Палау',
	'QA' : 'Катар',
	'JO' : 'Иордания',
	'AS' : 'Американское Самоа',
	'TC' : 'Туркс и Кейкос',
	'LC' : 'Святая Люсия',
	'MN' : 'Монголия',
	'VA' : 'Ватикан',
	'AW' : 'Арулько',
	'GY' : 'Гайана',
	'SR' : 'Суринам',
	'IM' : 'Остров Мэн',
	'VU' : 'Вануату',
	'HR' : 'Хорватия',
	'AI' : 'Ангуилья',
	'PM' : 'Сен-Пьер и Микелон',
	'GP' : 'Гваделупа',
	'MF' : 'Сен-Мартен',
	'GG' : 'Гернси',
	'BI' : 'Бурунди',
	'TM' : 'Туркменистан',
	'KG' : 'Кыргызстан',
	'MM' : 'Мьянма',
	'BT' : 'Бутан',
	'LI' : 'Лихтенштейн',
	'FO' : 'Фарерские острова',
	'ET' : 'Эфиопия',
	'MQ' : 'Мартиника',
	'JE' : 'Джерси',
	'AD' : 'Андорра',
	'AQ' : 'Антарктида',
	'IO' : 'Британская территория в Индийском океане',
	'GL' : 'Гренландия',
	'GW' : 'Гвинея-Бисау',
	'ER' : 'Эритрея',
	'WF' : 'Уоллис и Футуна',
	'PF' : 'Французская Полинезия',
	'CU' : 'Куба',
	'TO' : 'Тонга',
	'TL' : 'Восточный Тимор',
	'ST' : 'Сан-Томе и Принсипи',
	'GF' : 'Французская Гвинея',
	'SB' : 'Соломоновы острова',
	'TV' : 'Тувалу',
	'KI' : 'Кирибати',
	'NU' : 'Ниуэ',
	'NF' : 'Норфолк',
	'NR' : 'Науру',
	'YT' : 'Майотта',
	'PN' : 'Питкэрн',
	'CI' : 'Кот-д\'Ивуар',
	'LA' : 'Лаос',
	'KP' : 'Корейская Народно-Демократическая Республика',
	'SJ' : 'Свальбард и Ян-Майен',
	'SH' : 'Остров Святой Елены',
	'CC' : 'Кокосовые острова',
	'EH' : 'Западная Сахара'}

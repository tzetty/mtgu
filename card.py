import json
import zmisc

class Card:
	# scryfell to arena
	SET_REMAPPER = {
		'm20': 'M20',
		'war': 'WAR',
		'rna': 'RNA',
		'grn': 'GRN',
		'm19': 'M19',
		'dom': 'DAR',
		'rix': 'RIX',
		'xln': 'XLN',
	}

	RARITY_REMAPPER = {
		'common': 'Com',
		'uncommon': 'Unc',
		'rare': 'Rare',
		'mythic': 'Myth'
	}

	CARD_COLOR_REMAPPER = {
		'' : '',
		'U' : 'Blue',
		'W' : 'White',
		'G' : 'Green',
		'R' : 'Red',
		'B' : 'Black',
		'B W' : 'Black/White',
		'B U' : 'Black/Blue',
		'G U' : 'Green/Blue',
		'B G' : 'Black/Green',
		'G R' : 'Green/Red',
		'R U' : 'Red/Blue',
		'R W' : 'Red/White',
		'G W' : 'Green/White',
		'U W' : 'Blue/White',
		'B R' : 'Black/Red',
		'B R U' : 'Gold',
		'B G R' : 'Gold',
		'G R W' : 'Gold',
		'B U W' : 'Gold',
		'G U W' : 'Gold',
		'B G U' : 'Gold',
		'B G R U W' : 'Gold',
	}

	SUBST_TABLE = {
		'{T}' : 'Tap',
		'{W}' : 'w',
		'{R}' : 'r',
		'{B}' : 'b',
		'{U}' : 'u',
		'{G}' : 'g',
		'{C}' : 'c',
		'{X}' : 'x',
		'{0}' : '0', '{1}' : '1', '{2}' : '2', '{3}' : '3',
		'{4}' : '4', '{5}' : '5', '{6}' : '6', '{7}' : '7',
		'{8}' : '8', '{9}' : '9', '{10}' : '11', '{11}' : '11',
		'{12}' : '12', '{13}' : '13', '{14}' : '14', '{15}' : '15',
		'{16}' : '16', '{17}' : '17', '{18}' : '18', '{19}' : '19',
		'{20}' : '20', '{21}' : '21', '{22}' : '22', '{23}' : '23',
	}

	SETS = [
        'war', 'rna', 'grn', 'm19', 'dom', 'rix', 'xln',
    ]

	TYPE_DASH = chr(8212)

	def __init__(self, dd):
		#print(type(dd))
		#print(dd)
		assert dd['object'] == 'card'
		self.dict = dd

	def to_json(self):
		return json.dumps(self.dict,  indent=2)

	def is_match(self, match_set, match_num):
		return (self.dict['set'] == match_set) and (self.dict['collector_number'] == match_num)

	def has_valid_number(self):
		return self.is_all_digits(self.dict['collector_number'])

	@staticmethod
	def is_valid(card):
		if Card.get_set_abbv(card) in Card.SETS:
			if card.has_valid_number():
				return True
		return False

	@staticmethod
	def is_all_digits(ss):
		if len(ss) == 0:
			return False

		for ch in ss:
			if ch not in '0123456789':
				return False
		return True

	@staticmethod
	def get_set_abbv(card):
		return card.dict['set']

	@staticmethod
	def get_card_color(card):
		return ' '.join(card.dict['color_identity'])

	@staticmethod
	def get_reprint_message(card):
		if card.dict['reprint'] == False:
			return ''
		return 'Reprint'

	@staticmethod
	def get_mana_cost(card):
		# detect and exclude lands
		if 'cmc' in card.dict:
			return str(int(card.dict['cmc']))
		return ''

	@staticmethod
	def get_power(card):
		if 'loyalty' in card.dict:
			return ''
		# special case lands and planeswalkers
		if 'power' in card.dict:
			return card.dict['power']
		return ''

	@staticmethod
	def get_toughness(card):
		# special case lands and planeswalkers
		if 'loyalty' in card.dict:
			return card.dict['loyalty']
		if 'toughness' in card.dict:
			return card.dict['toughness']
		return ''

	@staticmethod
	def get_split_types(card):
		# special case lands and planeswalkers
		if 'type_line' in card.dict:
			tl = card.dict['type_line']
			return [x.strip() for x in tl.split(Card.TYPE_DASH)]
		return []

	@staticmethod
	def get_type(card):
		types = Card.get_split_types(card)
		if len(types) >= 1:
			return types[0]
		return ''

	@staticmethod
	def get_subtypes(card):
		types = Card.get_split_types(card)
		if len(types) == 2:
			return types[1]
		return ''

RowDef = zmisc.RowDef(
	zmisc.DictColDef.mode_str('set_name', 'set', remapper=Card.SET_REMAPPER),
	zmisc.DictColDef.mode_int('number', 'collector_number'),
	zmisc.GetterColDef('card_color', Card.get_card_color, remapper=Card.CARD_COLOR_REMAPPER),
	zmisc.DictColDef.mode_str('rarity', 'rarity', remapper=Card.RARITY_REMAPPER),
	zmisc.DictColDef.mode_str('card_name', 'name'),
	zmisc.GetterColDef('card_type', Card.get_type),
	zmisc.GetterColDef('card_type', Card.get_subtypes),
	zmisc.GetterColDef('power', Card.get_power),
	zmisc.GetterColDef('toughness', Card.get_toughness),
	zmisc.DictColDef.mode_str('mana_mix', 'mana_cost', subst_table=Card.SUBST_TABLE),
	zmisc.DictColDef.mode_str('card_text', 'oracle_text', encoding='ascii', encoding_mode='ignore', subst_table=Card.SUBST_TABLE),
)

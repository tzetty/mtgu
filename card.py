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
		'common': 'C',
		'uncommon': 'U',
		'rare': 'R',
		'mythic': 'M'
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

	def __init__(self, dd):
		assert dd['object'] == 'card'
		self.dict = dd

	def to_json(self):
		return json.dumps(self.dict,  indent=2)

	def is_match(self, match_set, match_num):
		return (self.dict['set'] == match_set) and (self.dict['collector_number'] == match_num)

	def has_valid_number(self):
		return self.is_all_digits(self.dict['collector_number'])

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


RowDef = zmisc.RowDef(
	zmisc.DictColDef.mode_str('set_name', 'set', remapper=Card.SET_REMAPPER),
	zmisc.DictColDef.mode_str('long_set_name', 'set_name'),
	zmisc.DictColDef.mode_int('number', 'collector_number'),
	zmisc.DictColDef.mode_str('rarity', 'rarity', remapper=Card.RARITY_REMAPPER),
	zmisc.DictColDef.mode_str('card_name', 'name'),
	zmisc.DictColDef.mode_str('card_type', 'type_line'),
	zmisc.GetterColDef('power', Card.get_power),
	zmisc.GetterColDef('toughness', Card.get_toughness),
	zmisc.GetterColDef('mana', Card.get_mana_cost),
	zmisc.DictColDef.mode_str('mana_mix', 'mana_cost', subst_table=Card.SUBST_TABLE),
	zmisc.GetterColDef('card_color', Card.get_card_color),
	zmisc.GetterColDef('reprint_message', Card.get_reprint_message),
	zmisc.DictColDef.mode_str('card_text', 'oracle_text', encoding='utf-8', subst_table=Card.SUBST_TABLE),
)


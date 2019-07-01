#!/usr/bin/env python3

import sys
import zmisc
import card

class DeckLine:
	def __init__(self, txt):
		parts = txt.split(' ')
		self.inv = int(parts[0])
		self.num = int(parts[-1])
		self.set_name = parts[-2][1:-1]
		self.card_name = ' '.join(parts[1:-2])
		self.rarity = 'Unknown'
		self.card_type = 'Unknown'

	def __str__(self):
		return '%d %s (%s) %d %s %s' % (self.inv,
			self.card_name, self.set_name, self.num,
			self.rarity, self.card_type)

	@staticmethod
	def match_card_row(card_row):
		return card_row.is_match(card_row.set_name, card_row.num)


class Decker:
	def __init__(self, args):
		self.args = zmisc.Args(args)

		self.card_db = zmisc.RowDb(zmisc.read_json_file('cards.json'), card.Card)
		self.card_db.print_rows(card.RowDef.to_csv_row)

		self.deck_db = zmisc.RowDb(zmisc.read_text_lines('rna_inv.txt'), DeckLine)
		self.deck_db.sort(key=lambda x:x.card_name)
		self.card_map = {}
		self.card_db.each(self.add_to_card_map)

		#self.deck_db.each(self.complete_deck_row)
		self.deck_db.print_rows(str)

	def add_to_card_map(self, row):
		print(row)

	def complete_deck_row(self, row):
		result = self.card_db.find(DeckLine.match_card_row)
		if result != None:
			print(result)
		else:
			print('no match for %s' % (row))

def main(args):
	Decker(args)

if __name__ == '__main__':
    main(sys.argv[1:])

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

	def __str__(self):
		return '%d %s (%s) %d' % (self.inv, self.card_name, self.set_name, self.num)

	@staticmethod
	def is_valid(deck_item):
		return True

class Decker:
	def __init__(self, args):
		self.args = zmisc.Args(args)

		self.card_db = zmisc.RowDb(zmisc.read_json_file('cards.json'), card.Card)
		self.card_db.print_rows(card.RowDef.to_csv_row)

		self.deck_db = zmisc.RowDb(zmisc.read_text_lines('rna_inv.txt'), DeckLine)
		self.deck_db.print_rows(str)


def main(args):
	decker = Decker(args)

if __name__ == '__main__':
    main(sys.argv[1:])

import sys
import random
import zmisc
import card


# https://docs.python.org/3.3/tutorial/inputoutput.html#reading-and-writing-files

SETS = [
'war', 'rna', 'grn', 'm19', 'dom', 'rix', 'xln', 
]


def main(args):
	jj = zmisc.read_json_file('cards.json')

	for ndx in range(len(jj)):
		cc = card.Card(jj[ndx])
		if card.Card.get_set_abbv(cc) in SETS:
			if cc.has_valid_number():
				print('%s' % (card.RowDef.to_csv_row(cc)))

	for set_ndx in range(len(jj)):
		cc = card.Card(jj[set_ndx])
		for arg_ndx in range(0, len(args), 2):
			match_set = args[arg_ndx]
			match_num = args[arg_ndx+1]

			if cc.is_match(match_set, match_num):
				print('ndx %d Found %s %s oracle len %d' % (set_ndx, match_set, match_num, len(cc.dict['oracle_text'])))
				print(cc.to_json())
				print('')

if __name__ == '__main__':
    main(sys.argv[1:])

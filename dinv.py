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

def main(args):
	txt = zmisc.read_file(args[0])
	lines = [x.strip() for x in txt.split('\n') if len(x) > 0]
	print(lines)

	deck = [DeckLine(line)for line in lines]
	deck.sort(key=lambda x: x.num)
	for dline in deck:
		print(dline)

if __name__ == '__main__':
    main(sys.argv[1:])

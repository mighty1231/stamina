
class Data:
	def __init__(self, fname):
		pos = []
		neg = []

		alphabet_size = -1 # 0 to alphabet_size-1

		with open(fname, 'rt') as f:
			for line in f.readlines():
				tokens = line.split(' ')

				# evaluate maximum alphabet
				string = bytes(map(int, tokens[1:]))
				for s in string:
					if s >= alphabet_size:
						alphabet_size = s+1

				if tokens[0] == '+':
					if string not in pos: # remove redundancy. Does multiple value prove its importance?
						pos.append(string)
				elif tokens[0] == '-':
					if string not in neg: # remove redundancy. Does multiple value prove its importance?
						neg.append(string)
				else:
					raise RuntimeError('Error on parsing %s:%s' % (fname, line))

		self.pos = pos
		self.neg = neg
		self.alphabet_size = alphabet_size

if __name__ == "__main__":
	d = Data("../grid/1_training.txt")
	for t in sorted(d.pos, key=len)[:30]:
		print(t)

	for t in sorted(d.neg, key=len)[:30]:
		print(t)
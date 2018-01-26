
class Data:
	def __init__(self, fname):
		pos = []
		neg = []

		alphabet_size = -1 # 0 to alphabet_size-1

		with open(fname, 'rt') as f:
			for line in f.readlines():
				tokens = line.split(' ')
				if tokens[-1] == '\n':
					tokens = tokens[:-1]

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

class PTA:
	# prefix
	def __init__(self, isPositive = None):
		self.dict = dict()
		self.acceptance = isPositive

	def register(self, string, isPositive):
		if string == []:
			if self.acceptance == None:
				self.acceptance = isPositive
			else:
				assert self.acceptance == isPositive
			return

		c = string.pop(0)
		if c in self.dict:
			self.dict[c].register(string, isPositive)
		else:
			pta = PTA()
			pta.register(string, isPositive)
			self.dict[c] = pta

	@staticmethod
	def fromTXT(fname):
		data = Data(fname)
		pta = PTA()
		for string in data.pos:
			pta.register(list(string), True)
		for string in data.neg:
			pta.register(list(string), False)
		return pta

	# return the number of nodes
	def __len__(self):
		# BFS
		todo = [self]
		cnt = 0
		while todo:
			node = todo.pop(0)
			cnt += 1

			for c in node.dict:
				todo.append(node.dict[c])

		return cnt


	def makeViz(self):
		edges = [] # fromState, toState, alphabet
		positiveStates = []
		negativeStates = []

		# BFS
		todo = [(self, 0)]
		node_cnt = 1
		while todo:
			node, idx = todo.pop(0)

			if node.acceptance == True:
				positiveStates.append(idx)
			elif node.acceptance == False:
				negativeStates.append(idx)

			for char in node.dict:
				edges.append((idx, node_cnt, char))
				todo.append((node.dict[char], node_cnt))
				node_cnt += 1


		posColor = "0.408 0.498 1.000"
		negColor = "0.000 1.000 1.000"
		string = 'digraph fsm {\n\tnode [style=filled];\n'

		for fromState, toState, alphabet in edges:
			string += '\t%d -> %d [ label = "%s" ];\n' % (fromState, toState, alphabet)

		for state in positiveStates:
			string += '\t%d [ color="%s" ];\n' % (state, posColor)

		for state in negativeStates:
			string += '\t%d [ color="%s" ];\n' % (state, negColor)

		string += '}\n'

		return string

	def makeSimpleViz(self):
		edges = [] # fromState, toState, alphabet
		positiveStates = []
		negativeStates = []

		# BFS
		todo = [(self, 0)]
		node_cnt = 1
		while todo:
			node, idx = todo.pop(0)

			if node.acceptance == True:
				positiveStates.append(idx)
			elif node.acceptance == False:
				negativeStates.append(idx)

			for char in node.dict:
				edges.append((idx, node_cnt, char))
				todo.append((node.dict[char], node_cnt))
				node_cnt += 1

		# check nodes to simplify
		prevState = [None for _ in range(node_cnt)]
		nextState = [None for _ in range(node_cnt)]
		for fromState, toState, alphabet in edges:
			if nextState[fromState] == None:
				nextState[fromState] = (toState, alphabet)
			else:
				nextState[fromState] = -1 # more than one item

			if prevState[toState] == None:
				prevState[toState] = (fromState, alphabet)
			else:
				prevState[toState] = -1 # more than one item

		def isSimplifiable(node):
			return node not in positiveStates and node not in negativeStates and \
				isinstance(prevState[node], tuple) and isinstance(nextState[node], tuple)

		for curNode in range(node_cnt):
			if isSimplifiable(curNode): 
				_prev, a1 = prevState[curNode]
				_next, a2 = nextState[curNode]

				string = [a1, a2]
				edges.remove((_prev, curNode, a1))
				edges.remove((curNode, _next, a2))
				
				while isSimplifiable(_next):
					_nextofnext, aa = nextState[_next]
					string.append(aa)
					prevState[_next] = None # prevent duplicate search

					edges.remove((_next, _nextofnext, aa))
					_next = _nextofnext
				edges.append((_prev, _next, string))

		# render
		posColor = "0.408 0.498 1.000"
		negColor = "0.000 1.000 1.000"
		string = 'digraph fsm {\n\tnode [style=filled];\n'

		for fromState, toState, alphabet in edges:
			string += '\t%d -> %d [ label = "%s" ];\n' % (fromState, toState, alphabet)

		for state in positiveStates:
			string += '\t%d [ color="%s" ];\n' % (state, posColor)

		for state in negativeStates:
			string += '\t%d [ color="%s" ];\n' % (state, negColor)

		string += '}\n'

		return string



if __name__ == "__main__":
	# pta = PTA.fromTXT("../grid/28_training.txt")
	# print(pta.makeSimpleViz())

	def getLengthOfPTA():
		for i in range(1, 101):
			pta = PTA.fromTXT("../grid/%d_training.txt" % i)
			print(len(pta))

	getLengthOfPTA()
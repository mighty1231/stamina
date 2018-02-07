# represent merging between states

from data import PTA
from disjoint_set import DisjointSet
from copy import copy
import os

class PTADisjointSetTree:
	def __init__(self, value):
		# DisjointSetTree
		self.parent = self
		self.rank = 0
		self.value = value # index of PTADisjointSet

	def copy(self):
		dst = DisjointSetTree(value)
		dst.rank = self.rank


class PTADisjointSet:
	def __init__(self, pta_nodes = None):
		max_alphabet = -1
		for node in pta_nodes:
			for c in node.dict:
				if c > max_alphabet:
					max_alphabet = c

		# dst_dict: dictionary, int -> PTADisjointSetTree
		# trans: make transition diagram, index to index
		# trans[idx_of_from_node][transition_int] = idx_of_to_node
		dst_dict = dict()
		trans = [[-1 for i in range(max_alphabet+1)] for t in range(len(pta_nodes))]
		for i, node in enumerate(pta_nodes):
			dst_dict[i] = PTADisjointSetTree(i)
			for c in node.dict:
				trans[i][c] = pta_nodes.index(node.dict[c])

		self.dst_dict = dst_dict
		self.trans = trans

	def __len__(self):
		return len(self.dst_dict)

	def _find_node(self, node):
		if node.parent != node:
			node.parent = self._find_node(node.parent)
		return node.parent

	def find(self, x):
		return self._find_node(self.dst_dict[x])

	def union(self, x, y):
		# make union diagram
		xRoot = self.find(x)
		yRoot = self.find(y)
		print(x, y, xRoot.value, yRoot.value)
		if xRoot == yRoot:
			return

		# get unions of nodes
		l = len(self.dst_dict)
		max_alphabet = len(self.trans[0])
		bfsq = [(xRoot.value, yRoot.value)]
		ds = DisjointSet([])

		while bfsq:
			v1, v2 = bfsq.pop(0)
			if v1 not in ds:
				ds.add(v1)
			if v2 not in ds:
				ds.add(v2)

			if ds.find(v1) == ds.find(v2):
				continue

			print('\nmerging', v1, v2)
			# if v1 in [16, 25, 26, 64, 56] or v2 in [16, 25, 26, 64, 56]:
			print(ds.get(v1), self.trans[v1][0], self.trans[v1][1])
			print(ds.get(v2), self.trans[v2][0], self.trans[v2][1])

			assert v1 == self.find(v1).value
			assert v2 == self.find(v2).value
			ds.union(v1, v2)
			# v1 = ds.find(v1).value
			# v2 = ds.find(v2).value
			for i in range(max_alphabet):
				newv1 = self.trans[v1][i]
				newv2 = self.trans[v2][i]

				if newv1 != -1 and newv2 != -1:
					r1 = self.find(newv1)
					r2 = self.find(newv2)

					bfsq.append((r1.value, r2.value))
				elif newv1 != -1:
					self.trans[v2][i] = newv1
				elif newv2 != -1:
					self.trans[v1][i] = newv2

		# clean up unions
		# Should I have to use the method with union and cleanup?
		unionlist = ds.get()
		print(unionlist)
		topmostnodes = []
		for nodes in unionlist:
			if len(nodes) == 1:
				continue

			# get max rank
			max_rank = -1
			max_rank_nodeid = -1
			max_rank_double = 0
			for node in nodes:
				rank = self.dst_dict[node].rank
				if max_rank < rank:
					max_rank = rank
					max_rank_nodeid = node
					max_rank_double = 0
				elif max_rank == rank:
					max_rank_double = 1

			# move transition to the topmost node
			topmostnode = self.dst_dict[max_rank_nodeid]
			topmostnodes.append(topmostnode)
			for node in nodes:
				self.dst_dict[node].parent = topmostnode
			topmostnode.rank = max_rank + max_rank_double

		# rearrange transitions
		# new_unions = self.get()
		# max_alphabet = len(self.trans[0])
		# for union in new_unions:
		# 	transitions = [-1 for _ in range(max_alphabet)]
		# 	for i, node in enumerate(union):
		# 		for self.trans[node]

		for nodes in unionlist:
			root = None
			for node in nodes:
				if root == None:
					root = self.find(node)
				else:
					assert root == self.find(node)

				for alphabet, c in enumerate(self.trans[root.value]):
					to = self.trans[node][alphabet]
					# if to != -1 and c != -1:
					# 	assert self.find(self.trans[root.value][alphabet]) == self.find(to).value
					if to != -1:
						self.trans[root.value][alphabet] = self.find(to).value

		# for i, node in enumerate(unionlist):
		# 	topmostnode = topmostnodes[i]

		# 	for alphabet, c in enumerate(self.trans[node]):
		# 		if c != -1:
		# 			if self.trans[topmostnode.value][alphabet] == -1:
		# 				self.trans[topmostnode.value][alphabet] = c
		# 			else:
						# assert self.find(self.trans[topmostnode.value][alphabet]) == self.find(c), (self.find(self.trans[topmostnode.value][i]).value, topmostnode.value, self.find(c).value, self.trans[topmostnode.value][alphabet], node, alphabet, c, )

		# self.verify()


	# return union set
	def get(self):
		p2nodes = dict()
		for i in self.dst_dict:
			node = self.dst_dict[i]
			parent = self._find_node(node).value

			try:
				p2nodes[parent].append(i)
			except KeyError:
				p2nodes[parent] = [i]
		return p2nodes.values()

	def copy(self):
		new_dict = dict()
		for i in self.dst_dict:
			new_dict[i] = self.dst_dict[i].copy()

		# linking
		for i in new_dict:
			new_dict[i].parent = new_dict[self.dst_dict[i].parent.value]

		ptads = PTADisjointSet()
		ptads.dst_dict = new_dict
		ptads.trans = copy(self.trans)

		return ptads

	def generateViz(self):
		# make graphviz code
		p2nodes = dict() # parent to node
		for i in self.dst_dict:
			node = self.dst_dict[i]
			parent = self._find_node(node).value

			try:
				p2nodes[parent].append(i)
			except KeyError:
				p2nodes[parent] = [i]
		vizcode = ''
		# vizcode += repr(p2nodes) + '\n'
		vizcode += 'digraph fsm {\n\tnode [style=filled];\n'

		for parent in p2nodes:
			for alphabet, to in enumerate(self.trans[parent]):
				if to == -1:
					continue
				# assert self.find(to).value == to

				vizcode += '\t"%s" -> "%s" [label = "%s" ];\n' % (
					'_'.join(map(str, p2nodes[parent])),
					'_'.join(map(str, p2nodes[self.find(to).value])),
					alphabet
				)

		vizcode += '}\n'
		return vizcode

	def draw(self, fname):
		with open(fname, 'wt') as f:
			f.write(self.generateViz())		
		os.system('dot -Tjpg %s -O' % fname)

	def verify(self):
		for i in self.dst_dict:
			assert i == self.dst_dict[i].value

		for i in self.dst_dict:
			root = self.find(i).value
			for alphabet, to in enumerate(self.trans[i]):
				if to != -1:
					assert self.find(to) == self.find(self.trans[root][alphabet]), (i, to, alphabet, self.trans)


if __name__ == "__main__":
	pta = PTA.fromTXT('test_training.txt')
	pta_nodes = []
	bfsq = [pta]
	while bfsq:
		node = bfsq.pop(0)
		pta_nodes.append(node)

		for c in node.dict:
			bfsq.append(node.dict[c])


	ds = PTADisjointSet(pta_nodes)


	# [[1, 45], [0, 28], [4, 6], [6, 45], [23, 56], [2, 13], [53, 10], [1, 60]]
	# digraph fsm {
	# 	node [style=filled];
	# 	1 -> 1 [label = "0" ];
	# 	1 -> 1 [label = "1" ];
	# 	25 -> 43 [label = "0" ];
	# 	25 -> 44 [label = "1" ];
	# 	26 -> 1 [label = "0" ];
	# 	26 -> 46 [label = "1" ];
	# }

	ds.draw('debugging_00.gv')
	merging = [
		[1, 45],
		[0, 28],
		[4, 6],
		[6, 45],
		[23, 56],
		[2, 13],
		[53, 10],
		[1, 60]
	]

	'''
	merging 3 17
	merging 1 66
	merging 7 27
	merging 12 0
	merging 3 29
	merging 1 30
	merging 11 47
	merging 64 48 <- 64
	merging 17 1
	merging 66 2
	merging 7 51
	merging 12 52
	merging 3 1
	merging 1 54
	merging 27 3
	merging 0 1
	merging 29 5
	merging 30 1
	merging 47 7
	merging 48 12
	merging 51 31
	merging 52 32
	merging 15 11
	merging 16 64 <- 16
	merging 11 55
	merging 64 56 <- 
	merging 17 2
	merging 66 58
	merging 56 15
	merging 24 16
	merging 25 39
	merging 26 40
	merging 41 25
	merging 42 26
	'''
	for i, (s, t) in enumerate(merging):
		ds.union(s, t)
		ds.verify()
		ds.draw('debugging_%02d.gv' % (i+1))

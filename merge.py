# represent merging between states

from data import PTA
from disjoint_set import DisjointSet
from copy import copy

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

			ds.union(v1, v2)
			for i in range(max_alphabet):
				newv1 = self.trans[v1][i]
				newv2 = self.trans[v2][i]

				if newv1 != -1 and newv2 != -1:
					r1 = self.find(newv1)
					r2 = self.find(newv2)

					bfsq.append((r1.value, r2.value))

		# clean up unions
		# Should I have to use the method with union and cleanup?
		unionlist = ds.get()
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

		# clean up transition of topmost nodes
		for node in topmostnodes:
			for i, v in enumerate(self.trans[node.value]):
				if v != -1:
					self.trans[node.value][i] = self.find(v).value

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
		

if __name__ == "__main__":
	ds = PTADisjointSet(4)
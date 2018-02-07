#!/usr/bin/python
# -*- coding: utf-8 -*-
# https://en.wikipedia.org/wiki/Disjoint-set_data_structure

from copy import copy

class DisjointSetTree:
	def __init__(self, value):
		self.parent = self
		self.rank = 0
		self.value = value # Is it necessary?

	def copy(self):
		dst = DisjointSetTree(value)
		# dst.parent = dst  <- imaginary value
		dst.rank = self.rank

	def __repr__(self):
		return 'DST(%d)' % self.value

class DisjointSet:
	def __init__(self, arr):
		if isinstance(arr, dict):
			self.dict = arr
		else:
			self.dict = dict()

			for i in arr:
				if i not in self.dict:
					self.dict[i] = DisjointSetTree(i)

	# add new node, different with conventional disjoint set
	def add(self, value):
		if value in self.dict:
			raise RuntimeError("DisjointSet.add(v) the key already exists")
		self.dict[value] = DisjointSetTree(value)

	# check if the node is in or not, different with conventional disjoint set
	def __contains__(self, value):
		return value in self.dict

	# return union set
	def get(self, x = None):
		p2nodes = dict() # parent to nodes
		for i in self.dict:
			node = self.dict[i]
			try:
				parent = self._find_node(node).value
			except:
				print(self.dict)
				raise RuntimeError("sdfgawr")

			try:
				p2nodes[parent].append(i)
			except KeyError:
				p2nodes[parent] = [i]

		return p2nodes.values() if x == None else p2nodes[self.find(x).value]

	def _find_node(self, node):
		if node.parent != node:
			node.parent = self._find_node(node.parent)
		return node.parent

	# get value and return node
	def find(self, x):
		return self._find_node(self.dict[x])

	def _union_node(self, nodex, nodey):
		xRoot = self._find_node(nodex)
		yRoot = self._find_node(nodey)

		if xRoot == yRoot:
			return

		if xRoot.rank < yRoot.rank:
			xRoot.parent = yRoot
		elif xRoot.rank > yRoot.rank:
			yRoot.parent = xRoot
		else:
			yRoot.parent = xRoot
			xRoot.rank += 1

	# get value and union
	def union(self, x, y):
		self._union_node(self.dict[x], self.dict[y])
	
	def copy(self):
		new_dict = dict()

		for i in self.dict:
			new_dict[i] = self.dict[i].copy()

		# linking
		for i in new_dict:
			new_dict[i].parent = new_dict[self.dict[i].parent.value]

		return DisjointSet(new_dict)


if __name__=='__main__':
	test_set = DisjointSet([1,2,3,3,3,4,5,6,7,7,7,7])
	
	print(test_set.get())

	test_set.union(2,3)
	print(test_set.get())
	test_set.union(6,7)
	print(test_set.get())
	
	test_set.union(2,6)
	print(test_set.get())
	print(test_set.find(2))
	print(test_set.get())

	no = DisjointSet([8, 10, 100, 10000, 1000])

	
	print(test_set.get())
	
	test_set.union(2,3)
	print(test_set.get())
	test_set.union(6,7)
	print(test_set.get())
	
	test_set.union(2,6)
	print(test_set.get())
	
	print(no.get())
	
	no.union(8,10)
	print(no.get())
	no.union(10000,100)
	print(no.get())
	
	no.union(100,10)
	print(no.get())
	
	no.union(8,1000)
	print(no.get())
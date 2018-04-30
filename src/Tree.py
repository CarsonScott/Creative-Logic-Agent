from data.dict import Dict
from lib.util import intersection, union, rr, print_graph

class Pointer(str):
	def __init__(self, data):
		self = str(data)

class Tree(Dict):

	def __init__(self, label=None, size=None):
		self.size = size
		self.label = label

	def append(self, value):
		i = len(self.keys())
		if self.size != None and i < self.size:
			self.set(i, value)
			return True
		return False

	def nodes(self, keys=[]):
		for i in self.keys():
			if i not in keys:
				keys.append(i)
			if isinstance(self[i], Tree):
				keys = self[i].nodes(keys)
		return keys

	def __call__(self):
		op = self.label
		last = None
		for i in self.keys():
			node = self[i]
			if isinstance(node, Tree):
				node = self[i]()
			if op in ['conjunction', 'disjunction']:
				if isinstance(node, bool) or node in [0, 1]:
					if op == 'conjunction':
						if bool(node) == False:
							return False
						if i == len(self.keys())-1:
							return True
					if op == 'disjunction':
						if bool(node) == True:
							return True
						if i == len(self.keys())-1:
							return False
				else:raise Exception()
			elif op in ['intersection', 'union']:
				if isinstance(node, list) or isinstance(node, str):
					if last == None:
						last = node
					else:
						if op == 'intersection':
							return intersection(list(node), list(last))
						if op == 'union':
							return union(list(node), list(last))
				else:raise Exception()
			elif op in ['occurance']:
				return True

def contains(tree, final):
	if isinstance(tree, Tree):
		if len(tree.keys()) == 0:
			return False
		elif final in tree.keys():
			return True
		else:
			for i in tree.keys():
				if isinstance(tree[i], Tree):
					if contains(tree[i], final):
						return True
			return False
	elif tree == final:
		return True
	return False

def overlap(t1, t2):
	if isinstance(t1, Tree) and isinstance(t2, Tree):
		n1 = t1.nodes()
		n2 = t2.nodes()
		return intersection(n1, n2)

def occurance(a, b):
	return a == -1 and b == 1


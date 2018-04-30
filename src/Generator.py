from Tree import *
from data.dict import *
from lib.util import intersection, union

optypes = Dict()
optypes = {
	'conjunction':(bool, bool),
	'disjunction':(bool, bool),
	'intersection':(list, list),
	'union':(list, list),
	'test1':(bool, list),
	'test2':(list, bool)}

def get_valid_interfaces(function, candidates):
	xtype, ytype = optypes[function]
	xoptions = []
	yoptions = []
	for i in candidates:
		xt, yt = optypes[i]
		if xtype == yt:
			xoptions.append(i)
		if ytype == xt:
			yoptions.append(i)
	return xoptions, yoptions

class Generator:
	def __init__(self, features):
		self.features = Dict().create(features, None)
		self.states = Dict().create(features, False)
		for i in self.features.keys():
			self.features[i] = i

	def __call__(self, inputs):
		deltas = self.update(inputs)
		pairs = self.extract(deltas)
		structs = self.construct(pairs)
		self.store(structs)

	def update(self, inputs):
		deltas = Dict()
		previous = self.states
		for i in self.features.keys():
			prev = self.states[i]
			if i in inputs:
				self.states[i] = True
			else:			
				feature = self.features[i]
				state = False
				if isinstance(feature, Tree):
					for j in feature.keys():
						if isinstance(feature[j], Pointer):
							feature[j] = self.features[feature[j]]
					state = feature()
				self.states[i] = state
			deltas[i] = int(self.states[i])-int(prev)
		return deltas

	def extract(self, deltas):
		pairs = []
		for i in deltas.keys():
			for j in deltas.keys():
				if i != j:
					di = deltas[i]
					dj = deltas[j]
					if occurance(di, dj):
						pairs.append((i, j))
		return pairs

	def construct(self, pairs):
		structures = Dict()
		for pair in pairs:
			i, j = pair
			if not contains(self.features[i], j):
				key = str(i) + '_' + str(j)
				if key not in self.features.keys():
					structure = Tree('occurance', 2)
					structure[i] = Pointer(i)
					structure[j] = Pointer(j)
					structures[key] = structure
		return structures

	def store(self, structures):
		for i in structures.keys():
			self.features[i] = structures[i]
			self.states[i] = False

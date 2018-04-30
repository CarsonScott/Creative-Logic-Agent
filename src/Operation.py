from data.dict import *

DEFAULT=0
CONJUNCT=1
DISJUNCT=2
PRODUCT=3
TOTAL=4
DATA=5
INITIAL=6
FINAL=7

class Operation(Dict):
	def __init__(self, functions=[], optype=0):
		super().__init__()
		self['type'] = optype
		self['functions'] = []
		for f in functions:
			self['functions'].append(f)

	def __call__(self, x):
		Y = []
		for f in self['functions']:
			Y.append(f(x))
		t = self['type']
		return self.compute(Y, t)
	
	def compute(self, Y, t):
			if t == CONJUNCT:
				return all(Y)
			if t == DISJUNCT:
				return any(Y)
			if t == PRODUCT:
				return mult(Y)
			if t == TOTAL:
				return sum(Y)
			if t == INITIAL:
				return Y[0]
			if t == FINAL:
				return Y[len(Y)-1]
			return Y
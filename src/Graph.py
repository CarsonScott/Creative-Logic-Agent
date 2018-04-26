from lib.util import *

class Graph(Dict):
	
	def create(self, keys):
		for i in keys:
			self.set(i, Dict())

	def sources(self, key):
		y = []
		for i in self.keys():
			if key in self[i].keys():
				y.append(i)
		return y

	def rel(self, source, terminal, function):
		if self.has(source) == False:
			self.set(source, Dict())
		if self.has(terminal) == False:
			self.set(terminal, Dict())

		if self[source].has(terminal) == False:
			self[source].set(terminal, Dict())
		if self[terminal].has(function) == False:
			self[terminal].set(function, Dict())

		if self.has(terminal) == False:
			self.set(terminal, function)
		self[source][terminal][function] = None
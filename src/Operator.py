from data.graph import *
from lib.util import compliment
from Operation import *

class Operator(Graph):
	
	def __call__(self, data, index=None, graph=None):
		if graph == None:
			graph = Graph()
		if index == None:
			index = data.keys()[0]

		if index not in graph.keys():
			graph[index] = Dict()
		if index not in self.keys():
			return graph

		unvisited = compliment(self[index].keys(), graph[index].keys()) 
		if len(unvisited) > 0:
			for j in unvisited:
				x = data[index], data[j]
				f = self[index][j]
				graph[index][j] = f(x)
				self(data, j, graph)
		return graph

	def rel(self, i, j, f):
		if i not in self.keys():
			self[i] = Dict()
		self[i][j] = f
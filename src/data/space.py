from .dict import *

class Space(Dict):
	def __init__(self, size):
		self.size = size
	def contains(self, point):
		x, y = point
		w, h = self.size
		return in_range(x, [0, w]) and in_range(y, [0, h])
	def has(self, key):
		return super().has(key) and self.contains(self[key])
	def set(self, key, point):
		super().set(key, point)

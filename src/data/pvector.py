class PVector(list):
	def __setitem__(self, i, v):
		if i in (0, 1):
			if i == 0:
				self.x = v
			if i == 1:
				self.y = v
			super().__setitem__(i, v)
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		super().__init__([x, y])
def in_range(value, limits=[None, None]):
	if limits[0] != None:
		if value < limits[0]:
			return False
	if limits[1] != None:
		if value >= limits[1]:
			return False
	return True
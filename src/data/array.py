def generate(dimensions, value=0):
	Y = Array()
	if dimensions == 1:
		Y = value
	else:
		for i in range(dimensions):
			Y.append(generate(dimensions-1))
	return Y

class Array(list):
	def get(self, *all):
		Y = None
		for i in all:
			if Y == None:
				Y = self[i]
			else:Y = Y[i]
		return Y
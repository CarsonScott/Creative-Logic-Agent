def TRUE(X):	
	if len(X) < 1: raise Exception()
	return X[0] == True
def FALSE(X):
	if len(X) < 1: raise Exception()
	return X[0] == False
def NOT(X):
	if len(X) < 1:raise Exception()
	return not X[0]
def AND(X):
	if len(X) < 2: raise Exception()
	return X[0] and X[1]	
def OR(X):
	if len(X) < 2: raise Exception()
	return X[0] or X[1]
def EQ(X):
	if len(X) < 2: raise Exception()
	return X[0] == X[1]
def MT(X):
	if len(X) < 2: raise Exception()
	return X[0] > X[1]
def LT(X):
	if len(X) < 2: raise Exception()
	return X[0] < X[1]
def ADD(X):
	if len(X) < 2: raise Exception()
	return X[0] + X[1]
def SUB(X):
	if len(X) < 2: raise Exception()
	return X[0] - X[1]
def MULT(X):
	if len(X) < 2: raise Exception()
	return X[0] * X[1]
def DIV(X):
	if len(X) < 2: raise Exception()
	return X[0] / X[1]
def LEN(X):
	if len(X) < 1: raise Exception()
	return len(X[0])
def ID(X):
	if len(X) < 1: raise Exception()
	return X[0]
def GET(X):
	if len(X) < 2: raise Exception()
	return X[0][X[1]]
def SET(X):
	if len(X) < 3: raise Exception()
	X[0][X[1]] = X[2]
def CALL(X):
	if len(X) < 2: raise Exception()
	return X[0](X[1])
def NEG(X):
	if len(X) < 1: raise Exception()
	return X[0] < 0
def POS(X):
	if len(X) < 1: raise Exception()
	return X[0] > 0
def ZERO(X):
	if len(X) < 1: raise Exception()
	return X[0] == 0
def LEFTOF(X):
	if len(X) < 2: raise Exception()
	return X[0]['x'] < X[1]['x']
def RIGHTOF(X):
	if len(X) < 2: raise Exception()
	return X[0]['x'] > X[1]['x']
def ABOVE(X):
	if len(X) < 2: raise Exception()
	return X[0]['y'] < X[1]['y']
def BELOW(X):
	if len(X) < 2: raise Exception()
	return X[0]['y'] > X[1]['y']
def NEG(X):
	for i in range(len(X)):
		if X[i] >= 0: return False
	return True
def POS(X):
	for i in range(len(X)):
		if X[i] < 0: return False
	return True
def ALL(X):
	for i in range(len(X)):
		if X[i] != True:return False
	return True
def SOME(X):
	for i in range(len(X)):
		if X[i] == True:return True
	return False
def MEAN(X):
	if len(X) == 0: return 0
	return TOTAL(X) / len(X)
def TOTAL(X):
	y = 0
	for i in range(len(X)):
		if X[i]: y += 1
	return y
def OFFX(X):
	return X[1]['x'] - X[0]['x']
def OFFY(X):
	return X[1]['y'] - X[0]['y']
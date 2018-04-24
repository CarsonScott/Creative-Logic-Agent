from Graph import *
from Variable import *

class Buffer(list):
    def __init__(self, size=0):
        self.size = size
        for i in range(size):
            self.append(None)

    def __call__(self, value):
        self.insert(0, value)
        if len(self) > self.size:
            del self[self.size:len(self)]


class Correlator:
    def __init__(self, buffer_size=1, max_weight=1, learning_rate=1, decay_rate=1):
        self.lrate = learning_rate
        self.drate = decay_rate
        self.boundary = max_weight
        self.inputs = Buffer(buffer_size)
        self.weights = WeightGraph()

    def init(self, keys, command='fully_connected'):
        self.weights = WeightGraph()
        self.weights.init(keys, command)

    def set(self, a, b, w=0):
        self.weights.set(a, b, w)

    def get(self, a, b):
        y = self.weights.get(a, b)

    def children(self, key):
        return list(self.weights[key].keys())

    def parents(self, key):
        Y = []
        for i in self.weights.keylist():
            if key in self.weights[i].keylist():
                Y.append(i)
        return Y

    def revise(self, a, b, dw=0):
        w = self.get(a, b)
        if w == None:w = 0
        w += dw
        if abs(w) > self.boundary:
            y = self.boundary * w / abs(w)
        else: y = w
        self.set(a, b, y)

    def update(self):
        keys = []
        for i in range(len(self.inputs)):
            f = self.inputs[i]
            if f != None:keys.append(f)

        delta = 0
        count = 0
        for i in range(len(keys)):
            a = keys[i]
            for j in range(i, len(keys)):
                b = keys[j]
                if a != b:
                    e =  abs(i-j) / len(self.inputs)
                    d = self.lrate / pow(1+e, 2)
                    self.revise(b, a, d)
                    delta += d
                    count += 1
 
            k = self.weights[a].keylist()
            for j in range(len(k)):
                b = k[j]
                if b not in keys:
                    self.revise(b, a, -self.drate)

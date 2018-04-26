from Graph import *
from Variable import *


class Correlator:

    def __init__(self, keys):
        self.weights = Graph()

    def get(self, a, b):
        return self.weights.get(a, b)

    def set(self, a, b, w):
        self.weights.set(a, b, w)

    def revise(self, a, b, dw=0):
        w = self.weights[a][b]
        
        if w == None:
            w = 0
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

            k = self.weights.keys()
            for j in range(len(k)):
                b = k[j]
                if b not in keys:
                    self.revise(b, a, -self.drate)

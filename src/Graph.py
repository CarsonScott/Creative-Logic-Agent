from lib.util import rr
from Variable import *

class Dict(dict):

    def __init__(self, K=list(), v=None):
        self.create(K)
    
    def create(self, k, v=None):
        for i in k:
            self.set(i, v)
    
    def keylist(self):
        return list(self.keys())

    def has(self, k):
        return k in self.keylist()

    def set(self, k, x):
        self[k] = x

class Graph(Dict):

    def init(self, keys, command=None):
        for i in range(len(keys)):
            key = keys[i]
            self[key] = Dict()

        if command == 'fully_connected':
            for i in range(len(keys)):
                for j in range(len(keys)):
                    if i != j:
                        self.set(keys[i], keys[j])

        elif command == 'chain':
            for i in range(len(keys)-1):
                self.set(keys[i], keys[i+1])
    
    def get(self, a, b, k):
        if b in self.paths(a):
            return self[a][b][k]
        return None

    def set(self, a, b, k=None, x=0):
        if a not in self.keylist():
            self[a] = Dict()
        if b not in self[a].keylist():
            self[a][b] = Dict()
        if b not in self.keylist():
            self[b] = Dict()
        if k != None:
            self[a][b][k] = x
        
    def links(self, key):
        return list(self[key].keys())

class WeightGraph(Graph):

    def get(self, a, b):
        if a in self.keylist():
            if b in self[a].keylist():
                y = self[a][b]
                if isinstance(y, Variable):
                    y = y.get()
                return y
   
    def set(self, a, b, w=0):
        if a not in self.keylist():
            self[a] = Dict()
        if b not in self.keylist():
            self[b] = Dict()
        if b not in self[a].keylist():
            self[a][b] = Variable(None, w)

        if not isinstance(self[a][b], Variable):
            self[a][b] = Variable(None, self[a][b])

        self[a][b].set(w)
            

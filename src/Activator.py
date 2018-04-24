from Correlator import *
from Variable import *
from lib.util import sort

class Activator:
    def __init__(self, pool_size):
        self.links = Correlator()
        self.nodes = Dict()
        self.threshs = Dict()
        self.psize = pool_size


    def set(self, a, b, w=0):
        self.links.set(a, b, w)

    def get(self, a, b):
        y = self.links.weights.get(a, b)
        if isinstance(y, Variable):
            y = y.get()
        return y

    def rem(self, a, b):
        del self.link.weights[a][b]

    def init(self, keys, buffer_size, learning_rate, decay_rate):
        self.links = Correlator(buffer_size=buffer_size, learning_rate=learning_rate, decay_rate=decay_rate)
        self.links.init(keys, Variable(Domain(-2, 2), 0))
        self.nodes = Dict()
        self.nodes.create(keys, 0)
        self.threshs = Dict()
        self.threshs.create(keys, Variable(Domain(0, 1), rr(10)/10))

        K = self.links.weights.keylist()
        for i in K:
            self.threshs[i].set(rr(0, 1))
            Ki = self.links.weights[i].keylist()
            for j in Ki:
                self.set(i, j, rr(-10, 10)/10)
            if i in Ki:
                self.rem(i, i)

    def update(self, x=None):
        self.links.update()
        if x != None:
            self.links.inputs(x)
        self.links.weights.update()

        inputs = Dict()
        for i in self.nodes.keylist():
            parents = self.links.parents(i)
            for j in parents:
                Wij = self.get(i, j)
                if Wij == None: Wij = 0

                if Wij != 0:
                    Wij -= self.links.drate * Wij / abs(Wij)
                self.set(i, j, Wij)

            X = Dict()
            for j in parents:
                X[j] = self.nodes[j]
            inputs[i] = X
        
        outputs = Dict()
        self.nodes = Dict()
        for i in inputs.keylist():
            y = 0
            for j in inputs[i].keylist():
                x = inputs[i][j]
                w = self.get(i, j)
                if w == None:
                    w = 0
                self.set(i, j, w)
                y += x * w

            outputs[i] = y
            self.nodes[i] = int(y >= self.threshs[i].get())

        active = sort(outputs)
        stored = []
        for i in range(len(active)-1, -1, -1):
            if self.nodes[active[i]]:
                self.links.inputs(active[i])
                stored.append(active[i])
                bias = self.threshs[active[i]].get()
                offset = y - bias
                self.threshs[active[i]].set(bias + offset * self.links.drate)
            if len(stored) >= self.psize:
                break
        return stored
        
    def weights(self):
        return self.links.weights
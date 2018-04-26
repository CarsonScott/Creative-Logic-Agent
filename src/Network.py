from Graph import *
from Variable import *
from lib.util import *

def variable_dict(D, d):
    y = D
    for i in y.keys():
        y[i] = Variable(d, y[i])
    return y

def variable_graph(G, d):
    y = G
    for i in y.keys():
        y[i] = variable_dict(y[i], d)
    return y

class Network:
    def __init__(self, bsize, lrate, drate):
        self.lrate = lrate
        self.drate = drate
        self.bsize = bsize
        self.inputs = Dict()
        self.values = Dict()
        self.thresh = Dict()
        self.links = Graph()

    def get_value(self, i):
        return self.value[i]

    def set_value(self, i, x):
        self.value[i] = x

    def get_link(self, i, j):
        return self.links[i][j].value

    def set_link(self, i, j, x):
        self.links[i][j].value = x

    def get_thresh(self, i):
        return self.thresh[i].value

    def set_thresh(self, i, x):
        self.thresh[i] = x

    def children(self, key):
        return list(self.weights[key].keys())

    def parents(self, key):
        Y = []
        for i in self.weights.keys():
            if key in self.weights[i].keys():
                Y.append(i)
        return Y

    def create(self, keys):
        self.values.create(keys)
        self.thresh.create(keys)
        self.links.create(keys)

        values = self.values
        values = constant_dict(values, 0)
        self.values = values

        links = self.links
        links = complete_graph(links)
        links = constant_graph(links, 0.1)
        links = variable_graph(links, Domain(-2, 2))
        self.links = links

        thresh = self.thresh
        thresh = constant_dict(thresh, 0.5)
        thresh = variable_dict(thresh, Domain(0, 1))
        self.thresh = thresh

    def add_inputs(self, keys):
        for i in range(len(keys)):
            key = keys[i]
            self.inputs[key] = 1-i/len(keys)
            self.values[key] = 1

    def update(self, active=[]):
        self.add_inputs(active)

        inputs = sort(self.inputs)
        current = len(self.inputs)
        target = self.bsize
                 
        old = inputs[target:current]
        
        visited = []
        for i in self.inputs.keys():
            if i not in old:
                self.inputs[i] += 1
                for j in self.inputs.keys():
                    if j not in old and j not in visited and i != j:
                        offset = self.inputs[j] - self.inputs[i]

                        if offset > 0:
                            initial, final = j, i
                        elif offset < 0:
                            initial, final = i, j
                        else: continue

                        error = 1 - abs(offset) / self.bsize
                        delta = pow(1 + error, 2) * self.lrate
                        self.links[initial][final].iterate(delta)
            visited.append(i)

        active = []
        values = self.values
        for i in self.values.keys():
            parents = self.links.sources(i)
            thresh = self.get_thresh(i)

            total = 0
            for j in parents:
                x = values[j]
                w = self.get_link(i, j)
                total += x * w

            offset = thresh - total
            output = int(offset >= 0)
            delta = offset * self.lrate
            
            self.values[i] = output
            self.thresh[i].iterate(delta)
            if output:active.append(i)

            for j in self.links[i].keys():
                self.links[i][j].decay(self.drate)
        return active

    def weights(self):
        y = Graph()
        for i in self.links.keys():
            y[i] = Dict()
            for j in self.links[i].keys():
                y[i][j] = self.links[i][j].value
        return y
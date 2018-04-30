from data.graph import *
from data.variable import *
from lib.util import *

def variable_dict(D, d, r):
    y = D
    for i in y.keys():
        y[i] = Variable(d, y[i], r)
    return y

def variable_graph(G, d, r):
    y = G
    for i in y.keys():
        y[i] = variable_dict(y[i], d, r)
    return y

class Network:
    def __init__(self, lrate, drate):
        self.lrate = lrate
        self.drate = drate
        self.inputs = Dict()
        self.limits = Dict()
        self.values = Dict()
        self.thresh = Dict()
        self.links = Graph()

    def add_buffer(self, name, size, keys):
        self.inputs[name] = Dict()
        self.limits[name] = size

    def create(self, keys):
        self.values.create(keys)
        self.thresh.create(keys)
        self.links.create(keys)

        values = self.values
        values = constant_dict(values, 0)
        self.values = values

        links = self.links
        links = complete_graph(links)
        links = constant_graph(links, 0)
        links = variable_graph(links, Domain(-2, 2), self.lrate)
        self.links = links

        thresh = self.thresh
        thresh = custom_dict(thresh, random_thresh)
        thresh = variable_dict(thresh, Domain(0, 4), self.lrate)
        self.thresh = thresh

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

    def children(self, k):
        return list(self.weights[k].keys())

    def parents(self, k):
        Y = []
        for i in self.weights.keys():
            if k in self.weights[i].keys():
                Y.append(i)
        return Y

    def add_inputs(self, b, X):
        for i in range(len(X)):
            k = X[i]
            if k != None:
                self.inputs[b][k] = 1-i/len(X)
            self.values[k] = 1

    def update(self, b, X):
        self.add_inputs(b, X)

        inputs = sort(self.inputs[b])
        current = len(self.inputs[b])
        target = self.limits[b]
        values = self.values

        old = inputs[target-1:current]
        
        visited = []
        for i in self.inputs[b].keys():
            if i not in old:
                self.inputs[b][i] += 1

                for j in self.inputs[b].keys():
                    if j not in old and j not in visited and i != j:
                        offset = self.inputs[b][j] - self.inputs[b][i]

                        if offset > 0:
                            initial, final = j, i
                        elif offset < 0:
                            initial, final = i, j
                        else: continue

                        error = 1 - abs(offset) / self.limits[b]
                        delta = pow(1 + error, 2) * self.lrate
                        self.links[initial][final].iterate(delta)

                visited.append(i)
            else:
                del self.inputs[b][i]
                self.values[i] = 0
    
        active = Dict()
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
            if output == 1:
                active[i] = offset

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
from math import sqrt
from random import randrange as rr

def random_weight():
    return rr(-10, 10)/20

def random_thresh():
    return rr(10)/10

def complete_graph(G, x=None):
    y = G
    for i in y.keys():
        for j in y.keys():
            y[i][j] = x
    return y

def custom_graph(G, f):
    y = G
    for i in y.keys():
        for j in y[i].keys():
            y[i][j] = f()
    return y

def custom_dict(D, f):
    y = D
    for i in y.keys():
       y[i] = f()
    return y

def constant_dict(D, x):
    y = D
    for i in y.keys():
       y[i] = x
    return y

def constant_graph(G, x):
    y = G
    for i in y.keys():
       y[i] = constant_dict(y[i], x)
    return y

def save_weights(W, i, f):
    string = ''
    Wi = W[i]
    Ki = Wi.keys()
    
    for j in Ki:
        value = W[i][j]
        string += str(value) + '\t'
    string = str(c) + '\t' + string + '\n'
    f.write(string)

def print_weights(W, i):
    Ki = W[i].keys()
    s = i + ':\n'
    for j in Ki:
        v = W[i][j].get()
        s += '\t' + j + ': ' + str(v) + '\n' 
    print(s)

def spaces(string):
    indices = []
    for i in range(len(string)):
        c = string[i]             
        if c == ' ':
            indices.append(i)
        elif i == len(string)-1:
            indices.append(i+1)
    return indices

def tabs(string):
    s = spaces(string)
    r = [None, None]
    ranges = []
    for i in range(1, len(s)):
        xi = s[i-1]
        xj = s[i]
        print(xi, xj)
        if xj-xi > 1:
            r[1] = xi-1
            if None not in r:
                ranges.append(r)
            r = [None, None]
        elif r[0] == None:
            r[0] = xi
    ranges.append(r)
    return ranges

def spaces_to_tabs(string):
    T = tabs(string)
    S = list(string)

    for t in T:
        if None not in t:
            i, f = t
            del S[i:f]
            S.insert(i, '\t')
    y = ''
    for c in S:
        if c != ' ':
            y += c
    return y

class Fitness:
    def __init__(self):
        self.a = Gaussian(f= 0.5)
        self.b = Gaussian(b= 0.1)
        self.c = Gaussian(f= -0.5, d= 0.1)

    def __call__(self, x):
        return self.a(x) + self.b(x) + self.c(x)

def print_graph(G):
    string = ''
    for i in G.keys():
        string += i + '\n'
        for j in G[i].keys():
            string += '  ' + j + ':  ' + str(G[i][j]) + '\n'
    print(string)

def compute_delta(graph, last):
    delta = Graph()
    for i in graph.keys():
        delta[i] = Dict()
        for j in graph[i].keys():
            delta[i][j] = last[i][j] - graph[i][j]
    return delta

class Dict(dict):
    def set(self, key, value):
        self[key] = value
    def get(self, key):
        return self[key]
    def create(self, keys):
        for i in range(len(keys)):
            k = keys[i]
            self[k] = None
    def has(self, key):
        return key in self.keys()
    def keys(self):
         return list(super().keys())

class Buffer(list):
    def __init__(self, size=0):
        self.size = size
        for i in range(size):
            self.append(None)
    def __call__(self, value):
        self.insert(0, value)
        if len(self) > self.size:
            del self[self.size:len(self)]

class Link(dict):
    def __init__(self, a, b, x):
        self['a'] = a
        self['b'] = b
        self['x'] = x

class PVector(dict):
    def __init__(self, x, y):
        self['x'] = x
        self['y'] = y

class Logistic:
    def __init__(self, a=0, k=1, b=3, v=0.5, q=0.5, c=1):
        self.a = a
        self.k = k
        self.b = b
        self.v = v
        self.q = q
        self.c = c
        self.e = 2.71828182
    def __call__(self, x):
        return self.a + (self.k - self.a) / pow((self.c + pow(self.q * self.e, -self.b*x)), 1/self.v)

class Gaussian:
    def __init__(self, a=1, b=0, c=1, d=2, f=1):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.f = f
        self.e = 2.71828182
    def __call__(self, x):
        return self.f * self.a * pow(self.e, pow(x-self.b, 2)/(self.d * pow(self.c, 2)))

class Grid(list):
    def __init__(self, w, h, v=None):
        for i in range(h):
            self.append([])
            for j in range(w):
                self[i].append(v)
    def print(self):
        for i in range(len(self)):
            string = ''
            for j in range(len(self[i])):
                string += str(self[i][j]) + ' '
            print(string)

def intersection(A, B):
    Y = []
    for i in range(len(A)):
        a = A[i]
        if a in B:
            Y.append(a)
    return Y

def sort(d):
    keys = list(d.keys())
    vals = []
    for i in range(len(keys)):
        k = keys[i]
        vals.append(d[k])

    if len(keys) <= 1:
        return keys

    done = False
    while not done:
        done = True
        for i in range(len(keys)-1):
            k1 = keys[i]
            k2 = keys[i+1]

            v1 = vals[i]
            v2 = vals[i+1]

            if v2 < v1:
                done = False
                keys[i] = k2
                vals[i] = v2
                keys[i+1] = k1
                vals[i+1] = v1
    return keys

def distance(p1, p2):
    x1, y1 = p1['x'], p1['y']
    x2, y2 = p2['x'], p2['y']
    return sqrt(pow(x2-x1, 2) + pow(y2-y1, 2))

def parse(string, char=[' ']):
    char.append(None)
    data = []
    s = ''
    for i in range(len(string)+1):
        if i < len(string):
            c = string[i]
        else:c = None

        if c in char:
            if s != '':
                data.append(s)
                s = ''
        else:s += c
    return data

def Keys(data):
    return list(data.keys())

def gather(data, variables=[]):
    if len(variables) == 0:
        variables = Keys(data)
    values = []
    for i in variables:
        values.append(data.get(i))
    return values

def has(data, variable):
    return variable in Keys(data)

def compute(inputs, functions):
    outputs = []
    for i in range(len(functions)):
        outputs.append(functions[i](inputs))
    return outputs

def select(options, functions, selection):
    scores = []
    for i in range(len(functions)):
        scores.append(functions[i](options))
    return selection(scores)

def istrue(X):
    Y = []
    for i in range(len(X)):
        if X[i] == True:
            Y.append(i)
    return Y

def direct(links):
    sizes = dict()
    for i in range(len(links)):
        a, b = links[i]
        if a not in sizes:
            sizes[a] = 0
        if b not in sizes:
            sizes[b] = 0
        sizes[a] += 1
        sizes[b] += 1

    for i in range(len(links)):
        a, b = links[i]
        if sizes[a] < sizes[b]:
            links[i] = [b, a]
    return links

def merge(string1, string2, char=''):
    return string1 + char + string2
    
def loop(size, index):
    x = index
    if x not in range(0, size):
        if x >= size:
            x = x - size 
        else:
            x = size + x
        x = loop(size, x)
    return x

def randomize(graph, size):
    for i in graph.keys():
        keys = graph[i].keys()
        done = False
        
        while not done:
            if len(keys) > size:
                j = rr(len(keys))
                del graph[i][j]
            else:
                done = True
    return graph

def in_range(domain, value):
    low, high = domain.bounds
    return value >= low and value < high

from math import sqrt
from random import randrange as rr

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
        
class Link(dict):
    def __init__(self, a, b, x):
        self['a'] = a
        self['b'] = b
        self['x'] = x

class PVector(dict):
    def __init__(self, x, y):
        self['x'] = x
        self['y'] = y

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
    for i in graph.keylist():
        keys = graph[i].keylist()
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

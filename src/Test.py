from Variable import *
from Activator import *
from lib.util import loop, randomize, Logistic, Gaussian, sort

def save_weights(W, i, f):
    string = ''
    Ki = W[i].keylist()
    for j in Ki:
        value = W[i][j].get()
        string += str(value) + '\t'
    string = str(c) + '\t' + string + '\n'
    f.write(string)

def print_weights(W, i):
    Ki = W[i].keylist()
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
    for i in G.keylist():
        string += i + '\n'
        for j in G[i].keylist():
            string += '  ' + j + ':  ' + str(G.get(i, j)) + '\n'
    print(string)

def compute_delta(graph, last):
    delta = Graph()
    for i in graph.keylist():
        delta[i] = Dict()
        for j in graph[i].keylist():
            delta[i][j] = last[i][j] - graph[i][j]
    return delta

keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
activator = Activator(5)
activator.init(keys, 20, 0.001, 0.0001)

W = None
L = None
i = 0
x = None
p = None
y = None

string = ''
log1 = open('log1.txt', 'w')
log2 = open('log2.txt', 'w')
total = 0
count = 0
for c in range(10000):
    x = keys[i]

    activator.update(x)
    W = activator.weights()  
    
    count += 1
    total += int(p==x)
    if i % 10 == 0:
        total /= count
        total = 0
        count = 0

    if x == p:print('p')
    else:print('-p')
    print_graph(W)


    if x != None:
        vals = Dict()
        for j in W[x].keylist():
            vals[j] = W[x][j].get()
        if len(vals) > 0:
            vals = sort(vals)
            p = vals[len(vals)-1]

    save_weights(W, 'a', log1)
    save_weights(W, 'b', log2)
    i = loop(len(keys), i+1)

log1.close()
log2.close()

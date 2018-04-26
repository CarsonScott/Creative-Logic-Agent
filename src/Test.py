from Variable import *
from Network import *
from lib.util import *

keys1 = ['a', 'b', 'c', 'd', 'e']
keys2 = ['f', 'g', 'h', 'i', 'j']
keys = keys1 + keys2

W = None
L = None
x = None
p = None
y = None

string = ''
log1 = open('log1.txt', 'w')
log2 = open('log2.txt', 'w')
total = 0
count = 0

rnn = Network(5, 0.0001, 0.0001)
rnn.create(keys)

index = 0
for c in range(10000):
    index = loop(len(keys1), index+1)

    x1 = keys1[index]
    x2 = keys2[index]

    y = rnn.update([x1, x2])
    print_graph(rnn.weights())

log1.close()
log2.close()

from Variable import *
from Network import *
from lib.util import *

keys = ['a', 'b', 'c', 'd', 'e']

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

rnn = Network(2, 0.0001, 0.0001)
rnn.create(keys)

index = 0
for c in range(10000):
    index = loop(len(keys), index+1)

    x1 = keys[index]
    y = rnn.update([x1])

    # print(rnn.inputs, y)

    count += 1
    total += int(p==x)
    # if index % 10 == 0:
    #     total /= count
    #     total = 0
    #     count = 0

    W = rnn.weights()
    print_graph(W)

    # # V = Dict()
    # # for i in W.keys():
    # #     for j in W[i].keys():
    # #         V[j] = W[x][j]

    # if len(V) > 0:
    #     V = sort(V)
    #     p = V[len(V)-1]

    # # save_weights(W, 'a', log1)
    # save_weights(W, 'b', log2)
 

log1.close()
log2.close()

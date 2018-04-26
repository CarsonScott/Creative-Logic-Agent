from Graph import *
G = Graph()
G.set('and', AND)
G.set('or', OR)
G.set('not', NOT)
G.rel('a', 'b', 'c')


print(G)
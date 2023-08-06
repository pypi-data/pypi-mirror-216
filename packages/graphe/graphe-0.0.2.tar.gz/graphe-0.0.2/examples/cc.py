#!/usr/local/bin/python3

import sys
from graphe.graph import graph
from graphe.graph import cc

infile = "../data/rosalind_tree.txt"

G = graph.Graph(infile)

mycc = cc.CC(G)

res = mycc.ccomps()

print(f'Conneted components: {len(res)}')
print(f'{res}')

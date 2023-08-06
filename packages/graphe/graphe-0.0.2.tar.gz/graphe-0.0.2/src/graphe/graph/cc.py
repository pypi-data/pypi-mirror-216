#!/usr/local/bin/python3

import sys
from graphe.graph import graph

class CC:
   def __init__(self, Graph):
      self.G = Graph
      self.cc = []

   #todo should use dfs.py instead
   def DFS(self, temp, v, visited):
      visited[v] = True
      temp.append(v)

      for i in self.G.adj(v):
         if visited[i] == False:
            temp = self.DFS(temp, i, visited)
      return temp


   def ccomps(self):
      visited = []
      self.cc = []
      for i in range(self.G.V):
         visited.append(False)
      for v in range(self.G.V):
         if visited[v] == False:
            temp = []
            self.cc.append(self.DFS(temp, v, visited))
      return self.cc

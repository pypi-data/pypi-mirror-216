Usage
=====


Creating a Graph object
-----------------------

.. code-block:: python

  from graphe.graph import graph
  from graphe import draw

  G = graph.Graph('mediumG.txt')

  fig = draw.Draw()
  fig.node_attr(label='')
  fig.draw(G)

.. image:: images/graph.png
  :width: 500


Breadth-first search
--------------------

.. code-block:: python

  from graphe.graph import graph
  from graphe.graph import bfs
  from graphe import draw

  G = graph.Graph('mediumG.txt')

  bfs = bfs.BFSearch(G, 0)  # make tree with root on vertex 0
  bfpath = bfs.path_to(200) # find path to vertex 200 from 0

  fig = draw.Draw()
  fig.node_attr(label='')
  fig.draw(G, bfpath)

.. image:: images/short.png
  :width: 500


Depth-first search
--------------------

.. code-block:: python

  from graphe.graph import graph
  from graphe.graph import dfs
  from graphe import draw

  G = graph.Graph('mediumG.txt')

  dfs = dfs.DFSearch(G, 0)
  dfpath = dfs.path_to(200)

  fig = draw.Draw()
  fig.node_attr(label='')
  fig.draw(G, dfpath)

.. image:: images/long.png
  :width: 500


Directed Depth-first search
---------------------------

.. code-block:: python

  from graphe.digraph import digraph
  from graphe.digraph import digraphdfs
  from graphe import draw

  DG = digraph.Digraph('mediumG.txt')

  dfs = digraphdfs.DirectedDFSearch(DG, 0)
  dfpath = dfs.path_to(197)

  fig = draw.Draw(digraph=True)
  fig.node_attr(label='')
  fig.edge_attr(color='gray', arrowsize='0.2', penwidth='0.75')
  fig.draw(DG, dfpath)

.. image:: images/digraph_dfs.png
  :width: 600


SymbolGraph
-----------

.. code-block:: python

  from graphe.digraph import symboldigraph
  from graphe import draw

  SG = symbolgraph.SymbolGraph('routes.txt')

  fig = draw.Draw()
  fig.set_names(SG.node_names())
  fig.node_attr(width='0.3', height='0.3', shape='circle', style='filled',
                color='gray', fontcolor='black', fontsize='8')
  fig.draw(SG.graph())

.. image:: images/symbolg.png
  :width: 500



When plotting you can manually add node name

.. code-block:: python

  node_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

  G = graph.Graph('tinyG.txt')

  fig = draw.Draw()
  fig.set_names(node_names)
  fig.node_attr(style='', fontcolor='black', fontsize='10')
  fig.draw(G)

.. image:: images/node_names.png
  :width: 500


And you can do breadth first search on SymbolGraph

.. code-block:: python

  SG = symbolgraph.SymbolGraph('routes.txt')

  b = bfs.BFSearch(SG.graph(), SG.ST['LAX'])
  path = b.path_to(SG.ST['HOU'])

  fig = draw.Draw()
  fig.set_names(SG.node_names())
  fig.node_attr(width='0.3', height='0.3', shape='circle', style='filled',
                color='gray', fontcolor='black', fontsize='8')
  fig.draw(SG.graph(), path)

.. image:: images/symbol_graph_bfs.png
  :width: 500


Digraph
-------

.. code-block:: python

  from graphe.digraph import digraph
  from graphe import draw

  DG = digraph.Digraph('tinyDG.txt')

  fig = draw.Draw(digraph=True)
  fig.node_attr(fontsize='8')
  fig.draw(DG, [11, 12, 9, 11])

.. image:: images/digraph_loop.png
  :width: 500

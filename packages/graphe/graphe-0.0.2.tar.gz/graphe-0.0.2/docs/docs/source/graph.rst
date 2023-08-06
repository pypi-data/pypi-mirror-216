Graph
=======


.. py:class:: Graph(init)

  Creates a Graph object

  :param init: if integer (V) initialize empty Graph with V vertices. If string (filename) load and populate from file.


  .. py:method:: add_edge(v, w)

    Connects vertices v and w, both must be smaller than V

    :param v: vertice id
    :param w: vertice id


  .. py:method:: adj(v)

     Return a list of vertices adjacent to v

     :param v: vertice id
     :rtype: array of vertice ids


  .. py:method:: to_string()

    Create a string representation of the Graph

    :rtype: string



BFSearch
--------

.. py:class:: BFSearch(G, s)

  Does a breadth first search of *G* from *s*.

  :param G: Graph object
  :param s: Vertex id of the starting point for search


  .. py:method:: bfs(G, s)

    Performs the breadth first search - called from constructor, should *not* be called directly

    :param G: Graph object created by Graph or SymbolGraph
    :param s: Vertex id of the starting point for search


  .. py:method:: has_path_to(v)

    Does (G,s) have a path to vertex v?

    :param v: Vertex id
    :rtype: Boolean


  .. py:method:: path_to(v)

    Make one path to v from s

    :param v: Vertex id
    :rtype: array of vertex ids connecting v to s


  .. py:method:: count()

    Number of visited nodes when exploring (G, s)

    :rtype: number of visited nodes


DFSearch
--------

.. py:class:: DFSearch(G, s)

  Does a depth first search of *G* from *s*.

  :param G: Graph object
  :param s: Vertex id of the starting point for search


  .. py:method:: dfs(G, v)

    Performs the depth first search - called from constructor, should *not* be called directly

    :param G: Graph object created by Graph or SymbolGraph
    :param v: Vertex id of the starting point for search

  .. py:method:: has_path_to(v)

    Does (G,s) have a path to vertex v?

    :param v: Vertex id
    :rtype: Boolean


  .. py:method:: path_to(v)

    Make one path to v from s

    :param v: Vertex id
    :rtype: array of vertex ids connecting v to s

  .. py:method:: count()

    Number of visited nodes when exploring (G, s)

    :rtype: number of visited nodes

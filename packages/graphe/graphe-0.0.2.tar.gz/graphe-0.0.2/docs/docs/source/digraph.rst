Digraph classes
===============


Digraph
-------

.. py:class:: Digraph(init)

  Creates a Digraph object

  :param init: if integer (V) initialize empty Digraph with V vertices. If string (filename) load and populate from file.


  .. py:method:: add_edge(v, w)

    Connects vertices v and w, both must be smaller than V

    :param v: vertice id
    :param w: vertice id


  .. py:method:: adj(v)

    Return a list of vertices adjacent to v

    :param v: vertice id
    :rtype: array of vertice ids


  .. py:method:: reverse()

    Return the reversed Digraph

    :rtype: Digraph


  .. py:method:: to_string()

    Create a string representation of the Digraph

    :rtype: string


|
Directed Cycle
--------------

Detects cycles in Digraphs

.. py:class:: DirectedCycle(DG)

    :param DG: Digraph object


    .. py:method:: has_cycle()

      :rtype: boolean

    .. py:method:: get_cycle()

      :rtype: list of vertices in the cycle


|
DepthFirstOrder
---------------

Performs a depth first search with support for returning visited nodes in
pre-order, post-order and reverse post-order.

.. py:class:: DepthFirstOrder(DG)

    :param DG: Digraph object


    .. py:method:: get_pre()

      :rtype: vertice list in pre-order

    .. py:method:: get_post()

      :rtype: vertice list in post-order

    .. py:method:: get_reverse_post()

      :rtype: vertice list in reverse post-order



|
DirectedDFSearch
----------------

.. py:class:: DirectedDFSearch(DG, s)

  Does a depth first search of *Digraph* from *s*.

  :param DG: Digraph object
  :param s: Vertex id of the starting point for search


  .. py:method:: dfs(DG, v)

    Performs the depth first search - called from constructor, should *not* be called directly

    :param DG: Digraph object
    :param v: Vertex id of the starting point for search

  .. py:method:: has_path_to(v)

    Does (DG, s) have a path to vertex v?

    :param v: Vertex id
    :rtype: Boolean


  .. py:method:: path_to(v)

    Make one path to v from s

    :param v: Vertex id
    :rtype: array of vertex ids connecting v to s

  .. py:method:: count()

    Number of visited nodes when exploring (Digraph, s)

    :rtype: number of visited nodes


|
Regex
-----

An implementation of regular expressions. Constructs a NFA Digraph of the
regular expression, then simulates the NFA using repeated depth first searches.

.. py:class:: Regex(expression)

    :param expression: regular expression


    .. py:method:: match(text)

      :param text: text string to be matched against the regex
      :rtype: boolean


|
SymbolDigraph
-------------

Support Digraph objects with named edges.

.. py:class:: SymbolDigraph(filename)

    :param filename: file to read


    .. py:method:: graph()

      :rtype: Digraph object


    .. py:method:: node_names()

      List of node names corresponding to vertice ids

      :rtype: array of node names


|
Topological Sort
----------------

Performs topological sort. Since this can only work on DAGs this code
raises an exception of a cycle is found.

.. py:class:: Topological(DG)

    :param DG: Digraph


    .. py:method:: get_order()

      :rtype: vertices in topological order

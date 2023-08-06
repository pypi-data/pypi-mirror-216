Utilities
=========


Draw
----

.. py:class:: Draw(digraph=False)

  Prepares for drawing a graph/digraph. Creates a graphviz object and sets the initial graph attributes


  .. py:method:: set_names(names)

    Provide figure with names (from SymbolGraph) instead of ids

    :param names: array [] of names for each vertex id


  .. py:method:: get_name(v)

    Use when drawing the figure, should not normally be called direcctly.

    :param v: vertex id
    :rtype: string


  .. py:method:: node_attr(**kwargs)

    Set graphviz attributes for nodes

    :param \*\*kwargs: List of graphviz keywords (e.g. color='black')


  .. py:method:: edge_attr(**kwargs)

    Set graphviz attributes for edges

    :param \*\*kwargs: List of graphviz keywords (e.g. penwidth='0.75')


  .. py:method:: draw(G, path=[])

    Draws the graph using the configured attributes and, optionally, showing the provided path

    :param G: Graph object
    :param path: list of vertices on the path

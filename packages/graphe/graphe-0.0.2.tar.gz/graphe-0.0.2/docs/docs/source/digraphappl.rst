Digraph applications
====================

These are examples of applications that uses Digraph algorithms for their
implementation.


Regex
-----

Use non deterministic finite state automaton (NFA) simulation to implement
minimalistic regular expressions. The supported regex commands are

.. code-block:: none

  contatenation    AB
  grouping         (ABC)
  or               A|B
  closure          A*B
  wildcard         A.B

Regex does not support common regex features such as ranges [], repeats {}, '?' or '+'
as these are not fundamental

.. code-block:: none

  [A-E]*  -> (A|B|C|D|E)*
  (AB){3} -> ABABAB
  (AB)+   -> AB(AB)*
  (CD)?   -> (|(CD))

Examples

.. code-block:: none

  CGC(CCG|CAG)*AGT        Genomic repeats
  .*ion                   'ending' in ion (crossword)
  .*Needle.*              search for Needle (grep)
  (0|(1(01*(00)*0)*1)*)*  binary numbers which are a multiple of 3


.. py:class:: Regex(regex)

  Construct the NFA Digraph of epsilon transitions for the regular expression.

  .. py:method:: match(text)

    matches text against the given regexp by repeatedapplication of
    DirectedDFSearch to explore the reachable states.

    :param text: text string to match with regex
    :rtype: boolean


Topological Search
------------------

Finds one solution (of potentially several) to the 'scheduling' problem where
some tasks must be preceded by others.

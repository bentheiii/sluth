Introduction
===============
Sluth is a library that can find the definition of a function or class in a file, without importing it.
It is useful for tools that need to find the definition of a function, for example, to generate documentation or to
perform static analysis.

.. code-block::

    from sluth import NodeWalk

    source = """
    raise ValueError('This file cannot be run')
    
    class Foo:
        def bar(self):
            pass
    """

    node_walk = NodeWalk.from_source(source)
    assert node_walk["Foo"]["bar"].lineno == 5


API Reference
================

.. module:: walker

.. class:: NodeWalk(node: ast.AST)

    A class for exploring definitions in an AST.

    :param node: The root AST node.

    .. method:: from_source(source: str)->NodeWalk
        :classmethod:

        Create a :class:`NodeWalk` object from python source code. The code is parsed using the built-in :mod:`ast` module.
    
    .. method:: from_file(filename: str)->NodeWalk
        :classmethod:

        Create a :class:`NodeWalk` object from a python file. The file is read as text and parsed using the built-in :mod:`ast` module.

    .. method:: children()->collections.abc.Mapping[str, collections.abc.Sequence[NodeWalk]]

        Returns a mapping of the names of the named declared in the node to a
        sequence of :class:`NodeWalk` objects for each declaration.
    
    .. method:: __getitem__(name: str)->NodeWalk

        Returns a :class:`NodeWalk` object for the declaration of the given name.

        :param name: The name of the declared object. Can also be a dotted name.

        :raises KeyError: If the name is not declared in the node.
        :raises ValueError: If the node declares multiple names with the given name.

    .. method:: get_last(name: str)->NodeWalk

        Returns a :class:`NodeWalk` object for the last declaration of the given name.

        :param name: The name of the declared object. Can also be a dotted name.

        :raises KeyError: If the name is not declared in the node.

    .. method:: get_many(name: str)->collections.abc.Sequence[NodeWalk]

        Returns a sequence of :class:`NodeWalk` objects for each declaration of
        the given name. If the name is not declared in the node, an empty
        sequence is returned.

    .. property:: lineno
                  col_offset
        :type: int

        The line numer and column offset of the node. Note that this may differ from the column offset of the root node
    
    .. property:: end_lineno
                  end_col_offset
        :type: int | None

        The line number and column offset of the end of the node. Note that this may differ from the column offset of the end of the root node
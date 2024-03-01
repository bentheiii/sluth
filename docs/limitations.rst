Limitations
=================

The AST traversal can cover many edge cases, but it is not exhaustive. It is possible that some edge 
cases are not covered. The tool is not able to handle the following cases:

* Named Expressions, A.K.A. Assignment Expressions, or the Walrus Operator (PEP 572) are not handled.
* Star imports are not handled.
* dynamically-defined attributes (e.g. `__getattr__` or `__getattribute__` methods) are not handled.
* instance attributes (such as those set in `__init__` or `__new__` methods) are not handled.
* definitions made in `exec` calls are not handled.
# Sluth- a python library to find python definitions in code without running it

Sluth is a simple utility to find definitions in python code without running it. It is useful for building documentation, finding dependencies, and other tasks that require knowing what a python file does without running it.

```python
from sluth import NodeWalk

source = """
raise ValueError('This file cannot be run')

class Foo:
    def bar(self):
        pass
"""

node_walk = NodeWalk.from_source(source)
assert node_walk["Foo"]["bar"].lineno == 5
```
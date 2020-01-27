# Object Graph in place of Lists    {#graph}

It is strange that Lisp variants still alive these 60 years. Lisp uses
single-linked lists as its core data structure. They are so unusable and low
level, but still in use. This project is a try to replace lists with object
graphs that are tightly linked with attribute grammar processing, and
reimplement some part of a glory SICP book with this core data model.

The whole data model is built atop of base @ref SICPy.Frame "Frame" class:

```
class Frame:
    def __init__(self,V):

        ## type/class tag /required for PLY parser/
        self.type = self.__class__.__name__.lower()

        ## frame name or scalar value (string,number)
        self.val  = V

        ## named slot{}s
        self.slot = {}

        ## nest[]ed ordered elements
        self.nest = []
```

* Every node of an object graph must be inherited from this class including @ref SICPy.Primitive "Primitive" ones.
* Edges of a graph are formed by named and ordered references stored in `slot{}` and `nest[]` respectively.

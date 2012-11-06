consoll
=======

Command-line wrapper for Python modules
---------------------------------------

Consoll provides a command-line interface to your own Python modules. This may not sound like a big deal, since you can already import modules into Python's interactive console using the `-i` switch. The aim of consoll, however, is to wrap your module in a command-line interface in such a way that your module becomes _indistinguishable_ from a full-blown terminal client with command history and tab completion.

Thus, consoll enables you to trivially write your own console clients and pseudo-shells. Here is an example:


```python
from consoll import Consoll

class Cat():

    def say_meow():
        print "meow"

    def add(a, b):
        print int(a) + int(b)

if __name__ == '__main__':

    c = Consoll(Cat)
    c.start()
```

Having been initialized with class `Cat`, consoll itself instantiates a `Cat` object and then exposes `Cat`'s methods through a command-line interface once `start()` is called:

    $ python cat.py
    >> say_meow
    meow
    >> add 2 3
    5
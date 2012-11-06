consoll
=======

Command-line wrapper for Python modules
---------------------------------------

Consoll provides a command-line interface to your own Python modules. This may not sound like a big deal, since you can already import modules into Python's interactive console using the `-i` switch. The aim of consoll, however, is to wrap your module in a command-line interface in such a way that your module becomes _indistinguishable_ from a full-blown terminal client with command history and tab completion.

Thus, consoll enables you to trivially write your own interactive shells, complete with command history and tab completion.

Here is an example:


```python
from consoll import Consoll

class Cat():

    def say_meow():
        print "meow"

    def add(a, b):
        print int(a) + int(b)

if __name__ == '__main__':

    my_cat = Cat()
    c = Consoll({'say_meow': my_cat.say_meow,
                      'add': my_cat.add })
    c.start()
```

Having initialized our Consoll instance with the `say_meow` and `add` methods, they are now exposed through a minimal command-line interface:

    $ python cat.py
    >> say_meow
    meow
    >> add 2 3
    5
consoll
=======

Command-line wrapper for Python modules
---------------------------------------

Consoll enables you to write your own interactive shells trivially. Arrow-key-navigable command history and tab completion come baked in.

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

Running the script starts a minimal command-line interface, with `say_meow` and `add` exposed to it:

    $ python cat.py
    >> say_meow
    meow
    >> add 2 3
    5
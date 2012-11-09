clamshell
=======

Command-line layer for Python modules
---------------------------------------

### Introduction

Clamshell enables you to write your own interactive shells trivially. Bash-style command history and tab completion come baked in.

### Example


```python
from clamshell import Clamshell

class Cat():

    def say_meow():
        print "meow"

    def add(a, b):
        print int(a) + int(b)

if __name__ == '__main__':

    my_cat = Cat()
    cs = Clamshell({ 'say_meow': my_cat.say_meow,
                          'add': my_cat.add       })
    cs.start()
```

Executing the script starts a minimal command-line interface that exposes the methods we passed to the `Clamshell` constructor:

    $ python cat.py
    >> say_meow
    meow
    >> add 2 3
    5

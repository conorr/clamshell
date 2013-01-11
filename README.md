clamshell
=======

Command-line layer for Python modules
---------------------------------------

### Introduction

Clamshell enables you to write your own interactive shells trivially. Bash-style command history comes baked in.

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
    shell = Clamshell({'say_meow': my_cat.say_meow,
                       'add': my_cat.add})
    shell.start()
```

Executing the script starts a minimal command-line interface that exposes the methods we passed to the `Clamshell` constructor:

    $ python cat.py
    >> say_meow
    meow
    >> add 2 3
    5

Clamshell can also parse hash arguments. Supposed we registered the following method to the Clamshell instance:

    def show_hash(self, h):
        for key, val in h.items():
            print key, val

We can then call it thus:

    >> show_hash {'fruit': 'banana', 'veggie': 'celery'}
    fruit banana
    veggie celery

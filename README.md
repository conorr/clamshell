clamshell
=======

Command-line interface for Python modules
---------------------------------------

### Introduction

Clamshell faciliates writing interactive shells by wrapping the GNU Readline library. Tab completion and command history come baked in; all you have to do is bind commands to your Python methods.

### Example

```python
class Cat():

    def say_meow():
        print "meow"

    def add(a, b):
        print int(a) + int(b)

if __name__ == '__main__':
    my_cat = Cat()

    from clamshell import Clamshell
    shell = Clamshell({'say_meow': my_cat.say_meow,
                       'add': my_cat.add})
    shell.start()
```

Executing the above script starts a command-line interface that exposes the methods we passed to the `Clamshell` constructor:

    $ python cat.py
    >> say_meow
    meow
    >> add 2 3
    5

Clamshell parses an input string into a command followed by an argument vector, which it uses to call the function bound to that command. That is, if there is a bound function:

    >> do_this_undefined_thing
    Error: unknown command 'do_this_undefined_thing'

### Passing Python objects as arguments

Clamshell can parse hashes, lists, and tuples as arguments in the command line. Suppose the following was a method of the Cat class:

```python
def show_hash(self, h):
    for key, val in h.items():
        print key, val
```
```
>> show_hash {'fruit': 'banana', 'veggie': 'celery'}
fruit banana
veggie celery
```

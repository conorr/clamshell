clamshell
=======

Command-line interface for Python modules
---------------------------------------

### Introduction

Clamshell helps you write interactive shells by wrapping the GNU Readline library. All you have to do is bind commands to your Python methods.

### Example

```python
class Cat():

    def say_meow():
        print "meow"

    def add(a, b):
        print int(a) + int(b)

if __name__ == '__main__':
    from clamshell import Clamshell
    my_cat = Cat()
    shell = Clamshell({'say_meow': my_cat.say_meow,
                       'add': my_cat.add})
    shell.start()
```

Executing the above script starts a command-line interface that exposes the methods passed to the `Clamshell` constructor:

```
$ python cat.py
>> say_meow
meow
```

Clamshell parses an input string into a command followed by arguments, which are passed to the function bound to the command:

```
>> add 2 3
5
```

If a command has no bound function, it prints an error:

```
>> do_this_undefined_thing
Error: unknown command 'do_this_undefined_thing'
>>
```

### Passing Python objects as arguments

Clamshell can parse hashes, lists, and tuples as arguments in the command line.

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

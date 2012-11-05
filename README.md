consoll
=======

Command-line wrapper for Python modules
---------------------------------------

Consoll provides a command-line interface to your own Python modules. This may not sound like a big deal, since you can already import modules into Python's interactive console using the -i switch. The aim of Consoll, however, is to wrap your module in a command-line interface that is _indistinguishable_ from a full-blown terminal client, complete with command history and tab completion.

Here is an example:

    from consoll import Consoll

    class Cat():

        def say_meow():
            print "meow"

        def add(a, b):
            print int(a) + int(b)

    if __name__ == '__main__':

        c = Consoll(Cat)
        c.start()

Then this module can be invoked:

    $ python cat.py
    >> say_meow
    meow
    >> add 2 3
    5

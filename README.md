consoll
=======

Console framework for Python

Consoll provides a command-line interface to your own Python objects. This may not sound like a big deal, since you can already import modules into Python's interactive console using the -i switch. The aim of Consoll, however, is to wrap your classes in a command-line interface that is _indistiguisable_ from a full-blown console client, complete with tab completion and command history.

Here is an example:

    from consoll import Consoll

    class Cat():

        def meow():
            print "meow"

        def add(a, b):
            print int(a) + int(b)

    if __name__ == '__main__':

        c = Consoll(Cat)
        c.start()

Then this module can be invoked:

    $ python cat.py
    >> meow
    meow
    >> add 2 3
    5

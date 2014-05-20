#!/usr/bin/python
import clamshellrl
import parser
import sys

class Clamshell():

    def __init__(self):
        clamshellrl.set_dispatch_callback(self.dispatch)

    def dispatch(self, expr):
        if expr == 'exit':
            sys.exit()
        tokens = parser.parse(expr)
        print tokens
        print [type(t) for t in tokens]

    def start(self):
        clamshellrl.start()

if __name__ == '__main__':
    shell = Clamshell()
    shell.start()

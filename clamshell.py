#!/usr/bin/python
import clamshellrl
import parser
import sys

class Clamshell():

    def __init__(self):
        clamshellrl.set_dispatch_callback(self.dispatch)

    def dispatch(self, expr):
        if expr == '':
            return
        if expr == 'exit':
            sys.exit()
        cmd, argv = parser.parse(expr)
        print cmd, argv

    def start(self):
        clamshellrl.start()

if __name__ == '__main__':
    shell = Clamshell()
    shell.start()

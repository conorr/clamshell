#!/usr/bin/python
import clamshellrl
import parser
import sys

class Clamshell():

    bindings = {}

    def __init__(self, bindings):
        self.bindings = bindings
        clamshellrl.set_dispatch_callback(self.dispatch)

    def dispatch(self, expr):
        if expr == '':
            return
        cmd, argv = parser.parse(expr)
        if cmd in self.bindings.keys():
            fn = self.bindings[cmd]
            try:
                fn.__call__(*argv)
            except TypeError:
                arg_count = fn.func_code.co_argcount
                if len(argv) != arg_count:
                    msg = "Error: '{}' takes {} argument{}, not {}"
                    plural = ''
                    if arg_count > 1: plural = 's'
                    print msg.format(cmd, arg_count, plural, len(argv))
                    return
                else:
                    print "Error: bad arguments"
                    return
        else:
            print "Error: unknown command: '{}'".format(cmd)

    def bind(self, cmd, fn):
        self.bindings[cmd] = fn

    def start(self):
        clamshellrl.start()

if __name__ == '__main__':

    def say_hello(name):
        print "Hello {}!".format(name)

    shell = Clamshell({
        'exit': sys.exit,
        'say_hello': say_hello
    })

    shell.start()

#!/usr/bin/python
import clamshellrl
import sys

class Clamshel():

    def __init__(self):
        clamshellrl.set_dispatch_callback(self.dispatch)

    def dispatch(self, message):
        if message == 'exit':
            sys.exit()
        print "would dispatch " + message

    def start(self):
        clamshellrl.start()

if __name__ == '__main__':
    shell = Clamshel()
    shell.start()

#!/usr/bin/python
import clamshellrl
import sys

def main():
    clamshellrl.set_dispatch_callback(dispatch)
    clamshellrl.start()

def dispatch(message):
    print "would dispatch " + message

if __name__ == '__main__':
    main()

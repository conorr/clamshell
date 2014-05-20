#!/usr/bin/python
import clamshellrl

def dispatch(message):
    print "would dispatch " + message

clamshellrl.set_dispatch_callback(dispatch)

clamshellrl.helloworld()

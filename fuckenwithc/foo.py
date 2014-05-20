#!/usr/bin/python
import clamshellrl

def dispatch(message):
    print "would dispatch " + message

clamshellrl.my_set_callback(dispatch)

clamshellrl.helloworld()

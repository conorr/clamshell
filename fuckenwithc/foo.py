#!/usr/bin/python
import helloworld

def dispatch(message):
    print "would dispatch " + message

helloworld.my_set_callback(dispatch)

helloworld.helloworld()

#! /usr/bin/python

import Pump from models

p = Pump()

def check():
    if p.is_on():
        print "Pump is on"
    else:
        print "Pump is off"

def on():
    print "Switching on"
    p.turn_on()
    check()

def off():
    print "Switching off"
    p.turn_off()
    check()


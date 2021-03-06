#! /usr/bin/python
import time
import RPi.GPIO as GPIO

from wsp_control.config import PIN, logger

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN.PUMP, GPIO.OUT)
GPIO.setup(PIN.FLOW, GPIO.IN)

def check():
    state = GPIO.input(PIN.PUMP)
    if state:
        print 'Pump is on'
    else:
        print 'Pump is off'
    return state

def on():
    print 'Switching on'
    GPIO.output(PIN.PUMP, GPIO.HIGH)
    state = check()
    logger.info('Override - Pump {0}'.format(('OFF', 'ON')[state]))

def off():
    print 'Switching off'
    GPIO.output(PIN.PUMP, GPIO.LOW)
    state = check()
    logger.info('Override - Pump {0}'.format(('OFF', 'ON')[state]))



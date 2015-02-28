#! /usr/bin/python
import time
import RPi.GPIO as GPIO
from wsp_control.config import PIN

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN.PUMP, GPIO.OUT)
GPIO.setup(PIN.FLOW, GPIO.IN)

def check():
    if GPIO.input(PIN.PUMP):
        print 'Pump is on'
    else:
        print 'Pump is off'

def toggle():
    while True:
        print 'Switching', GPIO.input(PIN.PUMP)
        GPIO.output(PIN.PUMP, not GPIO.input(PIN.PUMP))
        time.sleep(2)

def override():
    print 'Switching on'
    GPIO.output(PIN.PUMP, GPIO.HIGH)

    if GPIO.input(PIN.PUMP):
        print 'Pump is on'
    else:
        print 'Pump is off'


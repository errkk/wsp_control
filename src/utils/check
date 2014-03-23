#! /usr/bin/python
import RPi.GPIO as GPIO
from config import PIN

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN.PUMP, GPIO.OUT)
GPIO.setup(PIN.FLOW, GPIO.IN)

if GPIO.input(PIN.PUMP):
    print 'Pump is on'
else:
    print 'Pump is off'

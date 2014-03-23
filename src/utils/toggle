#! /usr/bin/python
import time
import RPi.GPIO as GPIO
from config import PIN

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN.PUMP, GPIO.OUT)

while True:
    print 'Switching', GPIO.input(PIN.PUMP)
    GPIO.output(PIN.PUMP, not GPIO.input(PIN.PUMP))
    time.sleep(2)

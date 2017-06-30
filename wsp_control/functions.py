#! /usr/bin/python
import time
import RPi.GPIO as GPIO

from wsp_control.config import PIN, logger

from .mqtt_client import log_to_iot


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

def on():
    print 'Switching on'
    GPIO.output(PIN.PUMP, GPIO.HIGH)
    state = GPIO.input(PIN.PUMP)

    logger.info('Override - Pump {0}'.format(('OFF', 'ON')[state]))
    log_to_iot({'pump': state})

    if state:
        print 'Pump is on'
    else:
        print 'Pump is off'

def off():
    print 'Switching off'
    GPIO.output(PIN.PUMP, GPIO.LOW)
    state = GPIO.input(PIN.PUMP)

    logger.info('Override - Pump {0}'.format(('OFF', 'ON')[state]))
    log_to_iot({'pump': state})

    if state:
        print 'Pump is on'
    else:
        print 'Pump is off'

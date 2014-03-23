#! /usr/bin/python
import time
import RPi.GPIO as GPIO
from datetime import datetime

from config import (PIN, UPLIFT_THRESHOLD, TEMP_CHECK_INTERVAL, PROBE_IN,
                    PROBE_OUT, PROBE_AIR)
from models import Pump, DataLog, FlowMeter, Thermometer

GPIO.setwarnings(False)
# Choose numbering scheme
GPIO.setmode(GPIO.BCM)
# Setup relay outputs
GPIO.setup(PIN.RELAY1, GPIO.OUT)
GPIO.setup(PIN.RELAY2, GPIO.OUT)
# Setup Input channel, using pulldown load
GPIO.setup(PIN.FLOW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

datalogger = DataLog(10)
p = Pump()

probe_in = Thermometer(*PROBE_IN)
probe_out = Thermometer(*PROBE_OUT)
probe_air = Thermometer(PROBE_AIR)

while True:
    # Make a reading and record it
    temp_in = probe_in.tick()
    temp_out = probe_out.tick()
    temp_air = probe_air.tick()

    # Log data every few loops
    datalogger.tick(temp_in, temp_out, None, temp_air)

    uplift = temp_out - temp_in
    if uplift >= UPLIFT_THRESHOLD:
        print 'Off {0}'.format(uplift)
        p.turn_on()
    else:
        print 'Off {0}'.format(uplift)
        p.turn_off()

    time.sleep(TEMP_CHECK_INTERVAL)

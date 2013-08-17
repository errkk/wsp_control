import time
import redis
import RPi.GPIO as GPIO
from datetime import datetime

from config import (PIN, REDIS_CONF, UPLIFT_THRESHOLD, TEMP_CHECK_INTERVAL,
                    PROBE_IN, PROBE_OUT)
from models import Pump, SpreadSheet, FlowMeter, Thermometer


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN.RELAY1, GPIO.OUT) # Pump Relay
GPIO.setup(PIN.GREEN, GPIO.OUT) # Green LED
GPIO.setup(PIN.FLOW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Switch

ss = SpreadSheet('Solar Panel Temp')
p = Pump()

probe_in = Thermometer(PROBE_IN, 'In')
probe_out = Thermometer(PROBE_OUT, 'Out')
t = FlowMeter(probe_in, probe_out)

# Loop 1 Check temperature all the time
while True:
    # Make a reding and record it
    temp_in = probe_in.tick()
    temp_out = probe_out.tick()

    ss.tick(temp_in, temp_out)

    uplift = temp_out - temp_in
    if uplift >= UPLIFT_THRESHOLD:
        p.turn_on()
    else:
        p.turn_off()

    time.sleep(TEMP_CHECK_INTERVAL)

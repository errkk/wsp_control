import time
import redis
import RPi.GPIO as GPIO
from datetime import datetime

from config import (PIN, REDIS_CONF, UPLIFT_THRESHOLD, TEMP_CHECK_INTERVAL,
                    PROBE_IN, PROBE_OUT)
from models import Pump, SpreadSheet, FlowMeter
from display import Display


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN.RED, GPIO.OUT) # Green LED
GPIO.setup(PIN.GREEN, GPIO.OUT) # Green LED
GPIO.setup(PIN.FLOW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Switch

t = FlowMeter()
r = redis.StrictRedis(**REDIS_CONF)
d = Display()
ss = SpreadSheet()
p = Pump()

probe_in = Thermometer(PROBE_IN)
probe_out = Thermometer(PROBE_OUT)

# Loop 1 Check temperature all the time
while True:
    # Make a reding and record it
    temp_in = probe_in.tick()
    temp_out = probe_out.tick()

    d.write_all('In: {0}C'.format(str(temp_in))),
                'Out: {0}C'.format(str(temp_out)))

    ss.tick(temp_in, temp_out)

    uplift = temp_out - temp_in
    if uplift >= UPLIFT_THRESHOLD:
        p.turn_on()
    else:
        p.turn_off()

    time.sleep(TEMP_CHECK_INTERVAL)

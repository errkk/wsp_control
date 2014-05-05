#! /usr/bin/python
import sys
import time
import requests
import RPi.GPIO as GPIO
from datetime import datetime

from config import (PIN, UPLIFT_THRESHOLD, TEMP_CHECK_INTERVAL, PROBE_IN,
                    PROBE_OUT, PROBE_AIR, DAYLIGHT, FLUSH_INTERVAL, PUSHCO_URL,
                    FLUSH_DURATION)
from local_config import PUSHCO_SECRET, PUSHCO_KEY
from models import Pump, DataLog, FlowMeter, Thermometer

OVERRIDE = False  # Dont switch pump with the script

GPIO.setwarnings(False)
# Choose numbering scheme
GPIO.setmode(GPIO.BCM)
# Setup relay outputs
GPIO.setup(PIN.RELAY1, GPIO.OUT)
GPIO.setup(PIN.RELAY2, GPIO.OUT)
# Setup Input channel, using pulldown load
GPIO.setup(PIN.FLOW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Log temperatures every 10 loops (10 mins)
datalogger = DataLog(10)
p = Pump()

probe_in = Thermometer(*PROBE_IN)
probe_out = Thermometer(*PROBE_OUT)
probe_air = Thermometer(*PROBE_AIR)

requests.post(PUSHCO_URL, params={'api_key': PUSHCO_KEY,
    'api_secret': PUSHCO_SECRET,
    'message': 'WSP Monitor Starting'})

def daytime():
    dt = datetime.now()
    return dt.hour in range(*DAYLIGHT)

flushcounter = 0

try:
    while True:
        # Make a reading and record it
        temp_in = probe_in.tick()
        temp_out = probe_out.tick()
        temp_air = probe_air.tick()

        # Log data every few loops
        datalogger.tick(temp_in, temp_out, None, temp_air)
        if OVERRIDE:
            time.sleep(TEMP_CHECK_INTERVAL)
            continue # To prevent pump switching during override


        # During daylight run the pump for 2 mins outside of the checking cycle
        if FLUSH_INTERVAL == flushcounter:
            print "Flush interval", daytime(), p.is_on()
            flushcounter = 0
            if daytime() and not p.is_on():
                print "Running the pump for 2 mins to get water on the sensor"
                p.turn_on(silent=True)
                time.sleep(FLUSH_DURATION)
                p.turn_off(silent=True)
                # Incase the pump needs to turn back on (cos of being warm enough)
                time.sleep(10)

        flushcounter += 1

        uplift = temp_out - temp_in
        if uplift >= UPLIFT_THRESHOLD:
            print 'On {0}'.format(uplift)
            if p.turn_on(uplift=uplift):
                print 'Pump On {0}'.format(uplift)
        else:
            print 'Off {0}'.format(uplift)
            if p.turn_off(uplift=uplift):
                print 'Off {0}'.format(uplift)

        time.sleep(TEMP_CHECK_INTERVAL)
except KeyboardInterrupt:
    print 'Exiting'
    sys.exit()

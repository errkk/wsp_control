#! /usr/bin/python
import pusher
import sys
import time
import requests
import RPi.GPIO as GPIO
from datetime import datetime

from config import (PIN, UPLIFT_THRESHOLD, TEMP_CHECK_INTERVAL, PROBE_IN,
                    PROBE_OUT, PROBE_AIR)
from local_config import PUSHER_CONFIG, PUSHCO_SECRET, PUSHCO_KEY
from models import Pump, DataLog, FlowMeter, Thermometer

PUSHCO_URL = 'https://api.push.co/1.0/push'

pu = pusher.Pusher(**PUSHER_CONFIG)

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
probe_air = Thermometer(*PROBE_AIR)

requests.post(PUSHCO_URL, params={'api_key': PUSHCO_KEY,
    'api_secret': PUSHCO_SECRET,
    'message': 'WSP Monitor Starting'})

try:
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
            if p.turn_on():
                try:
                    requests.post(PUSHCO_URL, params={'api_key': PUSHCO_KEY,
                        'api_secret': PUSHCO_SECRET,
                        'message': 'Pump ON {0}'.format(uplift)})
                except:
                    pass

                try:
                    pu['pump'].trigger('on', uplift)
                except:
                    pass

        else:
            print 'Off {0}'.format(uplift)
            if p.turn_off():
                try:
                    requests.post(PUSHCO_URL, params={'api_key': PUSHCO_KEY,
                        'api_secret': PUSHCO_SECRET,
                        'message': 'Pump OFF {0}'.format(uplift)})
                except:
                    pass

                try:
                    pu['pump'].trigger('off', uplift)
                except:
                    pass

        time.sleep(TEMP_CHECK_INTERVAL)
except KeyboardInterrupt:
    print 'Exiting'
    sys.exit()

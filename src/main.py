import time
import redis
import RPi.GPIO as GPIO
from datetime import datetime

from config import PIN
from timer import Timer
from therm import get_temp

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN.RED, GPIO.OUT) # Green LED
GPIO.setup(PIN.GREEN, GPIO.OUT) # Green LED
GPIO.setup(PIN.FLOW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Switch

t = Timer()
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Loop 1 Check temperature all the time
while True:
    temp_in, temp_out = get_temp('in'), get_temp('out')
    r.set('TMP:IN', temp_in)
    r.set('TMP:OUT', temp_out)
    time.sleep(5)

import time
import redis
import RPi.GPIO as GPIO
from datetime import datetime
from pigredients.displays import textStarSerialLCD as textStarSerialLCD

from config import PIN, REDIS_CONF
from timer import Timer
from therm import get_temp
from spreadsheet import SpreadSheet


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN.RED, GPIO.OUT) # Green LED
GPIO.setup(PIN.GREEN, GPIO.OUT) # Green LED
GPIO.setup(PIN.FLOW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Switch

t = Timer()
r = redis.StrictRedis(**REDIS_CONF)

display = textStarSerialLCD.Display(baud_rate=9600)

ss = SpreadSheet()


# Loop 1 Check temperature all the time
while True:
    try:
        temp_in, temp_out = get_temp('in'), get_temp('out')
    except IOError:
        pass
    else:
        display.clear()
        display.position_cursor(1, 1)
        display.ser.write('In: {0}C'.format(str(temp_in)))
        display.position_cursor(2, 1)
        display.ser.write('Out: {0}C'.format(str(temp_out)))
        r.set('TMP:IN', temp_in)
        r.set('TMP:OUT', temp_out)
        ss.update_spreadsheet(temp_in, temp_out)
    time.sleep(5)

import time
import RPi.GPIO as GPIO
from datetime import datetime
from config import PIN
from timer import Timer

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN.RED, GPIO.OUT) # Green LED
GPIO.setup(PIN.GREEN, GPIO.OUT) # Green LED
GPIO.setup(PIN.FLOW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Switch

t = Timer()

while True:
    time.sleep(1)

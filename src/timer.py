import redis
import pusher
from datetime import datetime
import RPi.GPIO as GPIO

from config import PIN, LITERS_PER_REV, REDIS_CONF, PUSHER_CONF
from therm import get_temp

r = redis.StrictRedis(**REDIS_CONF)
p = pusher.Pusher(**PUSHER_CONF)

class Timer:
    LITERS_PER_REV = LITERS_PER_REV

    def __init__(self):
        self.pump_on = False
        GPIO.output(PIN.RED, GPIO.LOW)
        self.t1 = datetime.now()
        GPIO.output(PIN.GREEN, GPIO.LOW)
        GPIO.add_event_detect(PIN.FLOW, GPIO.RISING,
                              callback=self.toggle,
                              bouncetime=400)

    def uplift(self):
        d_temp = float(r.get('TMP:OUT')) -  float(r.get('TMP:IN'))
        return d_temp

    def energy(self, td):
        grams = self.LITERS_PER_REV * 1000
        uplift = self.uplift()
        calories = uplift * grams
        jouels = calories * 4.1
        power = jouels / td
        return (power / 1000, uplift)

    def toggle(self, data):
        t2 = datetime.now()
        td = t2 - self.t1
        self.t1 = t2
        td = td.total_seconds()
        power, uplift = self.energy(td)
        print '{0:.2f} liters/sec, {1:.3f} kW +{2}C'.format(
             self.LITERS_PER_REV / td,
             power, uplift)

        GPIO.output(PIN.GREEN, not GPIO.input(PIN.GREEN))

        if uplift > 2 and not self.pump_on:
            GPIO.output(PIN.RED, GPIO.HIGH)
            p['WSP_PUMP'].trigger('pump', {'state': 'on'})
            self.pump_on = True

        elif uplift < 2 and self.pump_on:
            GPIO.output(PIN.RED, GPIO.LOW)
            p['WSP_PUMP'].trigger('pump', {'state': 'off'})
            self.pump_on = False

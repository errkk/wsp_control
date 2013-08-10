from datetime import datetime
import RPi.GPIO as GPIO

from config import PIN, LITERS_PER_REV
from therm import get_temp


class Timer:
    LITERS_PER_REV = LITERS_PER_REV

    def __init__(self):
        self.t1 = datetime.now()
        GPIO.output(PIN.GREEN, GPIO.LOW)
        GPIO.add_event_detect(PIN.FLOW, GPIO.RISING,
                              callback=self.toggle,
                              bouncetime=200)

    def uplift(self):
        d_temp = get_temp('out') - get_temp('in')
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
             self.LITERS_PER_REV * td,
             power, uplift)

        GPIO.output(PIN.GREEN, not GPIO.input(PIN.GREEN))
        if uplift > 2:
            GPIO.output(PIN.RED, GPIO.HIGH)
        else:
            GPIO.output(PIN.RED, GPIO.LOW)

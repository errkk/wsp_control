import time
import gspread
import redis
import RPi.GPIO as GPIO
from datetime import datetime
import pusher

from config import PIN, LITERS_PER_REV, REDIS_CONF, PUSHER_CONF, GOOGLE_CONF

r = redis.StrictRedis(**REDIS_CONF)
p = pusher.Pusher(**PUSHER_CONF)


class SpreadSheet:
    """ Interface with google docs for logging temperatures to a spreadsheet
    """
    INTERVALS = 2
    def __init__(self):
        multiplier = 0

    def tick(self, temp_in, temp_out):
        multiplier += 1
        if self.multiplier >= self.INTERVALS:
            self.multiplier = 0
            self.update_spreadsheet(temp_in, temp_out)

    def update_spreadsheet(self, temp_in, temp_out):
        gc = gspread.login(*GOOGLE_CONF)
        sh = gc.open("Solar Panel Temp").sheet1
        values = [datetime.now(), temp_in, temp_out]
        sh.append_row(values)


class FlowMeter:
    """ Counter to calculate flow rate and energy from the on off signal
    provided by the flow meter, runs as an externally controlled loop
    """
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


class Pump:
    """ Controller for pump relay, retains the pump's state
    """
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        if self.is_on:
            return False
        self.is_on = True
        GPIO.output(PIN.RED, GPIO.HIGH)
        p['WSP_PUMP'].trigger('pump', {'state': 'on'})
        return True

    def turn_off(self):
        if not self.is_on:
            return False
        self.is_on = False
        GPIO.output(PIN.RED, GPIO.LOW)
        p['WSP_PUMP'].trigger('pump', {'state': 'off'})
        return True

    def check(self):
        " Check the state of the output pin (to the relay) "
        return GPIO.input(PIN.RED)


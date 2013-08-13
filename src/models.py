import time
import gspread
import redis
import RPi.GPIO as GPIO
from datetime import datetime
import pusher

from config import (PIN, LITERS_PER_REV, REDIS_CONF, PUSHER_CONF, GOOGLE_CONF)

r = redis.StrictRedis(**REDIS_CONF)
p = pusher.Pusher(**PUSHER_CONF)


class SpreadSheet:
    """ Interface with google docs for logging temperatures to a spreadsheet
    """
    def __init__(self, sheet_title, intervals=2):
        self.multiplier = 0
        self.sheet_title = sheet_title
        self.intervals = intervals

    def tick(self, *args):
        self.multiplier += 1
        if self.multiplier >= self.intervals:
            self.multiplier = 0
            self.update_spreadsheet(*args)

    def update_spreadsheet(self, *args):
        try:
            gc = gspread.login(*GOOGLE_CONF)
            sh = gc.open(self.sheet_title).sheet1
            values = [datetime.now(), *args]
            sh.append_row(values)
        except:
            print 'Couldnt write to the spreadsheet this time'


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


class Thermometer:
    """ Manages the reading of the DS18B20 temperature probes
        Reads from the probe (slow) on an interval and records the latest
        value to a redis cache for fast retrieval by other parts of the app
    """
    def __init__(self, uuid):
        self.uuid = uuid
        self.path = "/sys/bus/w1/devices/{0}/w1_slave".format(self.uuid)

    def tick(self):
        " Loop method, triggered from an external loop to keep probes in sync "
        return self._read()

    def _read(self):
        try:
            with open(self.path) as tfile:
                text = tfile.read()
                secondline = text.split("\n")[1]
                temperaturedata = secondline.split(" ")[9]
                temperature = float(temperaturedata[2:])
                self._temperature = temperature / 1000
        except IOError:
            pass
        else:
            r.set(self.uuid, self._temperature)
            return self._temperature

    def get(self):
        " Try to get from redis, if there is no cached value read and return "

        cached = r.get(self.uuid)
        if cached:
            return cached
        else:
            return self._read()

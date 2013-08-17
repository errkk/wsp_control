import time
import gspread
import redis
import RPi.GPIO as GPIO
from datetime import datetime

from config import (PIN, LITERS_PER_REV, REDIS_CONF, GOOGLE_CONF)

r = redis.StrictRedis(**REDIS_CONF)


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
        #try:
        gc = gspread.login(*GOOGLE_CONF)
        sh = gc.open(self.sheet_title).sheet1
        values = list((datetime.now(), ) +  args)
        sh.append_row(values)
        #except:
            #print 'Couldnt write to the spreadsheet this time'


class FlowMeter:
    """ Counter to calculate flow rate and energy from the on off signal
    provided by the flow meter, runs as an externally controlled loop
    """
    LITERS_PER_REV = LITERS_PER_REV

    def __init__(self, probe_in, probe_out):
        self.pump_on = False
        GPIO.output(PIN.RELAY1, GPIO.LOW)
        self.t1 = datetime.now()
        GPIO.output(PIN.GREEN, GPIO.LOW)
        GPIO.add_event_detect(PIN.FLOW, GPIO.RISING,
                              callback=self.tick,
                              bouncetime=400)
        self.probe_in = probe_in
        self.probe_out = probe_out

    def uplift(self):
        d_temp = self.probe_out.get() - self.probe_in.get()
        return d_temp

    def energy(self, td):
        grams = self.LITERS_PER_REV * 1000
        uplift = self.uplift()
        calories = uplift * grams
        jouels = calories * 4.1
        power = jouels / td
        return (power / 1000, uplift)

    def tick(self, data):
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
    PIN = PIN.RELAY1

    def __init__(self):
        self.is_on = False
        GPIO.output(self.PIN, GPIO.LOW)

    def turn_on(self):
        if self.is_on:
            return False
        GPIO.output(self.PIN, GPIO.HIGH)
        self.check()
        return True

    def turn_off(self):
        if not self.is_on:
            return False
        GPIO.output(self.PIN, GPIO.LOW)
        self.check()
        return True

    def check(self):
        " Check the state of the output pin (to the relay) "
        self.is_on = GPIO.input(self.PIN)
        return self.is_on


class Thermometer:
    """ Manages the reading of the DS18B20 temperature probes
        Reads from the probe (slow) on an interval and records the latest
        value to a redis cache for fast retrieval by other parts of the app
    """
    def __init__(self, uuid, label=None):
        self.uuid = uuid
        self.path = '/sys/bus/w1/devices/{0}/w1_slave'.format(self.uuid)
        self.label = label
        self.temperature = None

    def tick(self):
        " Loop method, triggered from an external loop to keep probes in sync "
        self._read()

    def _read(self):
        try:
            with open(self.path) as tfile:
                text = tfile.read()
                secondline = text.split("\n")[1]
                temperaturedata = secondline.split(" ")[9]
                temperature = float(temperaturedata[2:]) / 100
                if temperature < 0:
                    raise Exception('Unlikely temperature')
        except IOError, e:
            print 'IO ERROR', e
            pass
        except Exception, e:
            print e
        else:
            self.temperature = temperature
            return self.temperature

import pusher
import logging
import time
import requests
import RPi.GPIO as GPIO
from datetime import datetime

from config import (PIN, LITERS_PER_REV, TEMP_ENDPOINT, PUMP_ENDPOINT,
                    PUSHCO_URL)
from local_config import AUTH, PUSHCO_SECRET, PUSHCO_KEY, PUSHER_CONFIG


pu = pusher.Pusher(**PUSHER_CONFIG)

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('/var/log/wsp_control.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

logger.info('Starting Up')


class DataLog:
    """ Publish to website
    """

    def __init__(self, intervals=2):
        self.count = 0
        self.intervals = intervals

    def tick(self, *args):
        self.count += 1
        if self.count >= self.intervals:
            self.count = 0
            self.update(*args)

    def update(self, *args):
        """ Post arg values as keys named "t[n]" to the webserver
        """
        data = {'t' + str(i+1): v for i, v in enumerate(args)}
        r = requests.post(TEMP_ENDPOINT, data, auth=AUTH)
        if r.status_code != 200:
            logger.error('Http error publishing data: {0}'
                         .format(r.status_code))


class FlowMeter:
    """ Counter to calculate flow rate and energy from the on off signal
    provided by the flow meter, runs as an externally controlled loop
    """

    def __init__(self, probe_in, probe_out):
        self.t1 = datetime.now()
        GPIO.add_event_detect(PIN.FLOW, GPIO.RISING,
                              callback=self.tick,
                              bouncetime=600)

    def tick(self, data):
        t2 = datetime.now()
        td = t2 - self.t1
        self.t1 = t2
        td = td.total_seconds()
        return LITERS_PER_REV / td


class Pump:
    """ Controller for pump relay, retains the pump's state
    """
    PIN = PIN.PUMP

    def __init__(self):
        GPIO.output(self.PIN, GPIO.LOW)

    def is_on(self):
        return bool(GPIO.input(self.PIN))

    def turn_on(self, silent=False, uplift=None):
        if self.is_on():
            return False
        GPIO.output(self.PIN, GPIO.HIGH)
        if not silent:
            self.report(uplift)
        return True

    def turn_off(self, silent=False, uplift=None):
        if not self.is_on():
            return False
        GPIO.output(self.PIN, GPIO.LOW)
        if not silent:
            self.report(uplift)
        return True

    def report(self, uplift=None):
        " report the state of the output pin (to the relay) "
        r = requests.post(PUMP_ENDPOINT, {'is_on': self.is_on()}, auth=AUTH)

        if self.is_on():
            state = 'on'
            message = 'Pump ON {0}'.format(uplift)
        else:
            state = 'off'
            message = 'Pump OFF {0}'.format(uplift)

        try:
            requests.post(PUSHCO_URL, params={'api_key': PUSHCO_KEY,
                'api_secret': PUSHCO_SECRET,
                'message': message})
        except:
            pass

        try:
            pu['pump'].trigger(state, uplift)
        except:
            pass


class Thermometer:
    """ Manages the reading of the DS18B20 temperature probes
        Reads from the probe (slow) on an interval and caches the latest
        value to the instance for quick retrieval
    """
    def __init__(self, uuid, adjustment=0, label=None):
        self.uuid = uuid
        self.adjustment = adjustment
        self.path = '/sys/bus/w1/devices/{0}/w1_slave'.format(self.uuid)
        self.label = label
        self.temperature = 0

    def tick(self):
        " Loop method, triggered from an external loop to keep probes in sync "
        return self._read()

    def _read(self):
        try:
            with open(self.path) as tfile:
                text = tfile.read()
                secondline = text.split("\n")[1]
                temperaturedata = secondline.split(" ")[9]
                temperature = float(temperaturedata[2:]) / 1000
                if temperature < 0 or temperature > 50:
                    raise Exception('Unlikely temperature')
        except IOError, e:
            logger.error('Can\'t read temp from thermometer {0}'.format(self.label))
            print 'Probe fucked up, using cached temperature'
            return self.temperature
        except Exception, e:
            logger.error('Thermometer error {0}'.format(e))
            print 'Probe fucked up, using cached temperature'
            return self.temperature
        else:
            self.temperature = temperature - self.adjustment
            return self.temperature

    def get(self):
        return self.temperature

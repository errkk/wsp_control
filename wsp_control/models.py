from __future__ import division

import time
from datetime import datetime

import requests
import RPi.GPIO as GPIO

from wsp_control.config import (PIN,
                                LITERS_PER_REV,
                                TEMP_ENDPOINT,
                                PUMP_ENDPOINT,
                                AUTH,
                                logger)

from .mqtt_client import log_to_iot

def post_data(endpoint, data):

    try:
        r = requests.post(endpoint, data, auth=AUTH)
    except:
        logger.error('Requests error publishing data')
    else:
        if r.status_code != 200:
            logger.error('Http error publishing data: {0}'\
                    .format(r.status_code))
        return r

class DataLog:
    """ Publish to website
    """

    def __init__(self, intervals=2):
        self.count = 0
        self.intervals = intervals

    def tick(self, *args):
        """ Post only every {internvals}th value
        """
        self.count += 1
        if self.count >= self.intervals:
            self.count = 0
            self.update(*args)

    def update(self, *args):
        """ Post arg values as keys named "t[n]" to the webserver
        """
        data = {'t' + str(i + 1): v for i, v in enumerate(args)}
        post_data(TEMP_ENDPOINT, data)
        log_to_iot(data)


class FlowMeter:
    """ Counter to calculate flow rate and energy from the on off signal
    provided by the flow meter, runs as an externally controlled loop
    """

    def __init__(self):
        self.t1 = datetime.now()
        GPIO.add_event_detect(PIN.FLOW, GPIO.RISING,
                              callback=self.tick,
                              bouncetime=2000)

    def tick(self, data):
        t2 = datetime.now()
        td = t2 - self.t1
        self.t1 = t2
        td = td.total_seconds()
        flow = LITERS_PER_REV / td

        logger.info('Flowmeter tick: {0:.2f}l/s'.format(flow))
        log_to_iot({'flow': flow})


class Pump:
    """ Controller for pump relay, retains the pump's state
    """
    PIN = PIN.PUMP

    def __init__(self):
        GPIO.output(self.PIN, GPIO.LOW)

    def is_on(self):
        return bool(GPIO.input(self.PIN))

    def __repr__(self):
        return ('OFF', 'ON')[self.is_on()]

    def turn_on(self):
        if self.is_on():
            return False
        GPIO.output(self.PIN, GPIO.HIGH)
        self.check()
        return True

    def turn_off(self):
        if not self.is_on():
            return False
        GPIO.output(self.PIN, GPIO.LOW)
        self.check()
        return True

    def check(self):
        " Check the state of the output pin (to the relay) "
        state = self.is_on()
        logger.info('Turning Pump {0}'.format(('OFF', 'ON')[state]))

        post_data(PUMP_ENDPOINT, {'is_on': state})
        log_to_iot({'pump': bool(state)})


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
            return self.temperature
        except Exception, e:
            logger.error('Thermometer error {0}'.format(e))
            return self.temperature
        else:
            self.temperature = temperature - self.adjustment
            return self.temperature

    def get(self):
        return self.temperature

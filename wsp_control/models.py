from __future__ import division

import time
from datetime import datetime

import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

from wsp_control.config import (PIN,
                                LITERS_PER_REV,
                                logger,
                                SPI_PORT,
                                SPI_DEVICE)

from .http_client import post_temp, post_pump

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

    def update(self, t1, t2, t3, t4, chlorine, ph):
        """ Post data to the server """
        post_temp(t1=t1, t2=t2, t3=t3, t4=t4, chlorine=chlorine, ph=ph)


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


class Pump:
    """ Controller for pump relay, retains the pump's state
    """
    PIN = PIN.PUMP

    def __init__(self, disconnect_mqtt=False):
        GPIO.output(self.PIN, GPIO.LOW)
        self.disconnect_mqtt = disconnect_mqtt

    def is_on(self):
        return bool(GPIO.input(self.PIN))

    def __repr__(self):
        return ('OFF', 'ON')[self.is_on()]

    def turn_on(self):
        if self.is_on():
            return False
        GPIO.output(self.PIN, GPIO.HIGH)
        self.confirm()
        return True

    def turn_off(self):
        if not self.is_on():
            return False
        GPIO.output(self.PIN, GPIO.LOW)
        self.confirm()
        return True

    def confirm(self):
        " Check the state of the output pin (to the relay) "
        state = self.is_on()
        logger.info('Turning Pump {0}'.format(('OFF', 'ON')[state]))

        post_pump(is_on=state)


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
            logger.error(
                'Can\'t read temp from thermometer {0}'.format(self.label))
            return self.temperature
        except Exception, e:
            logger.error('Thermometer error {0}'.format(e))
            return self.temperature
        else:
            self.temperature = temperature - self.adjustment
            return self.temperature

    def get(self):
        return self.temperature

try:
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
except:
    pass

class ADC:

    def __init__(self, index, out_min, out_max, is_4_20=False):
        self.index = index
        self.out_min = out_min
        self.out_max = out_max
        self.is_4_20 = is_4_20
        self._value = 0

    def tick(self):
        self._read()
        return self.get()

    def _read(self):
        try:
            self._value = mcp.read_adc(self.index)
        except:
            logger.error('Couldn\'t read ADC')

    def get(self):
        if self.is_4_20:
            return self.convert_4_to_20(self._value)
        else:
            return self.convert_0_to_20(self._value)

    def convert(self, value, in_min, in_max, out_min, out_max):
        return ((value - in_min) * (out_max - out_min)
            / (in_max - in_min) + out_min)

    def convert_from_adc(self, value, out_min, out_max):
        return self.convert(value, 0, 1024, out_min, out_max)

    def convert_4_to_20(self, value):
        current = self.convert_from_adc(value, 0, 20)
        if current < 4.0:
            logger.error("Fault on ADC Channel {}".format(self.index))
        return self.convert(current, 4, 20, self.out_min, self.out_max)

    def convert_0_to_20(self, value):
        current = self.convert_from_adc(value, 0, 20)
        return self.convert(current, 0, 20, self.out_min, self.out_max)


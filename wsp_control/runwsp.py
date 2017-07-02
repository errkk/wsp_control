#! /usr/bin/python
import sys
import time
from datetime import datetime

from wsp_control.models import Pump, DataLog, FlowMeter, Thermometer, ADC
from wsp_control.config import (UPLIFT_THRESHOLD,
                                TEMP_CHECK_INTERVAL,
                                PROBE_IN,
                                PROBE_OUT,
                                PROBE_AIR,
                                logger)

""" Instanciate stuff """
datalogger = DataLog(1)
pump = Pump()

probe_in = Thermometer(*PROBE_IN)
probe_out = Thermometer(*PROBE_OUT)
probe_air = Thermometer(*PROBE_AIR)

adc_chlorine = ADC(0, 0.0, 4.0, is_4_20=True)
adc_ph = ADC(1, 0.0, 14.0)

flow_meter = FlowMeter()


def minutely():
    """ Runs every minute
    """

    # Make a reading and record it
    temp_in = probe_in.tick()
    temp_out = probe_out.tick()
    temp_air = probe_air.tick()
    chlorine = adc_chlorine.tick()
    ph = adc_ph.tick()

    # Log data every few loops
    datalogger.tick(temp_in, temp_out, None, temp_air, chlorine, ph)

    uplift = temp_out - temp_in
    logger.info('Checking Uplift: {0} Pump is {1}'.format(uplift, pump))
    if uplift >= UPLIFT_THRESHOLD:
        pump.turn_on()
    else:
        pump.turn_off()


def ten_minutely(now):
    """ Runs every 10 minutes, just after the 10 secondly stuffs.
    """

    # Turn the pump on to flush water through the system.
    # 10 seconds later, the ten_secondly function will decide
    # whether the pump should stay on
    if now.hour in range(8, 18):
        logger.info('Flushing water')
        pump.turn_on()


def main():

    logger.info('Starting Up')

    try:
        while True:
            now = datetime.now()
            seconds = now.second
            minutes = now.minute

            # Do it on the minute
            if int(seconds) == 0:
                print 'Doing minutely thing', now
                minutely()

                # If its the first second of a 10 minute interval
                # then do this too. But after the temp checking
                if minutes % 10 == 0:
                    print 'Doing ten minutely thing', now
                    ten_minutely(now)

            # Sleep for the resolution of how much we want to match
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info('Exiting')
        sys.exit()

if '__main__' == __name__:
    main()

import sys
import os

# Probe addresses
DS_INTERNAL = ('28-000004abe48d', 0)
PROBE_IN = ('28-000004f1952b', 0, 'In') # HK1
PROBE_OUT = ('28-000004bdb407', -0.188, 'Out') # HK2
PROBE_AIR = ('28-000004f230a3', 0, 'Air') # UK1

class PIN:
    " GPIO Pin numbering "
    RELAY1 = 22
    RELAY2 = 18
    FLOW = 21
    PUMP = 22

# Flow meter
LITERS_PER_REV = 10

# How often to check the temperature (from the probe)
TEMP_CHECK_INTERVAL = 60

# Number of degrees of temperature difference to switch the pump
UPLIFT_THRESHOLD = 1.0


# Sparkfun creds
PUBLIC_KEY = 'ZG0n4wdp1KTz051dYwmZ'
PRIVATE_KEY = '2mJ7v9Zx1PHgElJ1ZM5j'
TEMP_ENDPOINT = 'http://data.sparkfun.com/input/{0}/'.format(PUBLIC_KEY)

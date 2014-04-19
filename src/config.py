import sys
import os

# Probe addresses
DS_INTERNAL = ('28-000004abe48d', 0)
PROBE_IN = ('28-000004f1952b', 0, 'In') # HK1
PROBE_OUT = ('28-000004f11ece', -0.188, 'Out') # HK2
PROBE_AIR = ('28-000004f230a3', 0, 'Air') # UK1

PUSHCO_URL = 'https://api.push.co/1.0/push'

API = 'http://wottonpool.co.uk/panel/input'
TEMP_ENDPOINT = os.path.join(API, 'temperature/')
FLOW_ENDPOINT = os.path.join(API, 'flow/')
PUMP_ENDPOINT = os.path.join(API, 'pump/')

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
# How often to run the pump when its not already on to check the temp
# Number is multipied by TEMP_CHECK_INTERVAL in seconds
FLUSH_INTERVAL = 15 # 15 minutes
FLUSH_DURATION = 60 * 2

# Number of degrees of temperature difference to switch the pump
UPLIFT_THRESHOLD = 1.0

DAYLIGHT = [9, 18]

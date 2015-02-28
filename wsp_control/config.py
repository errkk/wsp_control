import sys
import os

# Probe addresses
DS_INTERNAL = ('28-000004abe48d', 0)
PROBE_IN = ('28-000004f1952b', 0, 'In') # HK1
PROBE_OUT = ('28-000004bdb407', -0.188, 'Out') # HK2
PROBE_AIR = ('28-000004f230a3', 0, 'Air') # UK1

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

# Number of degrees of temperature difference to switch the pump
UPLIFT_THRESHOLD = 1.0

# Basic auth creds for posting data to the server
try:
    AUTH = ('raspi', os.environ['WSP_AUTH_PW'])
except:
    print 'Don\'t forget the Basic Auth PW'
    sys.exit()
import sys
import os
import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
LOG_PATH = '/var/log/wsp_control.log'

if os.access(LOG_PATH, os.W_OK):
    hdlr = logging.FileHandler(LOG_PATH)
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


# Probe addresses
DS_INTERNAL = ('28-000004abe48d', 0)
PROBE_IN = ('28-000004f1952b', 0, 'In')
PROBE_OUT = ('28-000004bdb407', -0.188, 'Out')
PROBE_AIR = ('28-000004f230a3', 0, 'Air')

API = 'https://wottonpool.co.uk/panel/input'
if os.environ.get('DEVELOPMENT'):
    API = 'http://stage.wsp.web3.errkk.co/panel/input'
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
TEMP_CHECK_INTERVAL = 1

# Number of degrees of temperature difference to switch the pump
UPLIFT_THRESHOLD = 1.0

# Basic auth creds for posting data to the server
try:
    AUTH = ('raspi', os.environ['WSP_AUTH_PW'])
except:
    print 'Don\'t forget the Basic Auth PW'

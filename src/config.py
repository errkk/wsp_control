from _google_conf import GOOGLE_CONF as GC

# Probe addresses
DS_INTERNAL = '28-000004abe48d'
HK1 = ('28-000004f1952b', 0)
HK2 = ('28-000004f11ece', -0.188)
UK1 = '28-000004f230a3'
PROBE_IN = HK1
PROBE_OUT = HK2
PROBE_AIR = UK1

API = 'http://planner.wottonpool.co.uk/panel/input/{0}/'
TEMP_ENDPOINT = API.format('temperature')
FLOW_ENDPOINT = API.format('flow')
PUMP_ENDPOINT = API.format('pump')


# Flow meter
LITERS_PER_REV = 10

class PIN:
    " GPIO Pin numbering "
    RELAY1 = 22
    RELAY2 = 18
    FLOW = 21
    PUMP = 22

GOOGLE_CONF = GC

# How often to check the temperature (from the probe)
TEMP_CHECK_INTERVAL = 60
# Number of degrees of temperature difference to switch the pump
UPLIFT_THRESHOLD = 2.0

SENTRY_URL = 'https://38dcd26d3c2541518e88b9164e758645:'\
             'd2bcc2caa71643369cda4db963a4cfa0@app.getsentry.com/8647'

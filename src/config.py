from _google_conf import GOOGLE_CONF as GC
# Probe addresses
PROBE1 = '28-000004abe48d'
PROBE2 = '28-000004aca5fc'
PROBE3 = '28-000004bdb407'
PROBE_IN = PROBE2
PROBE_OUT = PROBE3

# Flow meter
LITERS_PER_REV = 10

class PIN:
    " GPIO Pin numbering "
    RELAY1 = 22
    GREEN = 18
    FLOW = 21

PUSHER_CONF = dict(
    app_id='51377',
    key='5c4f611479dafe53705e',
    secret='e6b4935bb205d95cf57e',
)
REDIS_CONF = dict(host='localhost', port=6379, db=0)
GOOGLE_CONF = GC

# How often to check the temperature (from the probe)
TEMP_CHECK_INTERVAL = 5
# Number of degrees of temperature difference to switch the pump
UPLIFT_THRESHOLD = 2.0

SENTRY_URL = 'https://38dcd26d3c2541518e88b9164e758645:'\
             'd2bcc2caa71643369cda4db963a4cfa0@app.getsentry.com/8647'

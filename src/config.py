from _google_conf import GOOGLE_CONF as GC
# Probe addresses
PROBE1 = '28-000004abe48d'
PROBE2 = '28-000004aca5fc'
PROBE3 = '28-000004bdb407'
PROBE_IN = PROBE1
PROBE_OUT = PROBE3

# Flow meter
LITERS_PER_REV = 10

class PIN:
    " GPIO Pin numbering "
    RED = 22
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

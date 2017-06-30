import json
from logging import getLogger
from os import path

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

logger = getLogger(__FILE__)

IOT_HOST = 'am763te2vwsh1.iot.eu-west-2.amazonaws.com'
CERTS = path.abspath(path.join('..', path.dirname(__FILE__), 'certs'))
ROOT_CA_PATH = path.join(certs, 'root-CA.crt')
PRIVATE_KEY_PATH = path.join(certs, 'Panels.private.key')
CERTIFICATE_PATH = path.join(certs, 'Panels.cert.pem')
CLIENT_ID = 'arn:aws:iot:eu-west-2:902208111599:thing/Panels'
THING_NAME = 'Panels'

client = AWSIoTMQTTShadowClient(CLIENT_ID)
client.configureEndpoint(IOT_HOST, 8883)
client.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)

client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

client.connect()

shadow_handler = client.createShadowHandlerWithName(THING_NAME, True)


def log_to_iot(**data):
    payload = {"state": {"desired": data}}
    shadow_handler.shadowUpdate(json.dumps(payload), shadow_callback_update, 5)

def shadow_callback_update(payload, , token):
    logger.debug("IOT update: %s", status)

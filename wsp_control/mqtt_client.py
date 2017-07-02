import json
from os import path, environ

import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

from .config import logger

IOT_HOST = environ.get('IOT_HOST')
CERTS = path.abspath(path.join(path.dirname(__file__), 'certs'))
ROOT_CA_PATH = path.join(CERTS, 'root-CA.crt')
PRIVATE_KEY_PATH = path.join(CERTS, 'Panels.private.key')
CERTIFICATE_PATH = path.join(CERTS, 'Panels.cert.pem')
THING_NAME = environ.get('IOT_THING_NAME')

client = AWSIoTMQTTShadowClient(THING_NAME)
client.configureEndpoint(IOT_HOST, 8883)
client.configureCredentials(
    ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)

client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

shadow_handler = client.createShadowHandlerWithName(THING_NAME, True)

client.connect()

def log_to_iot(data):
    payload = {"state": {"desired": data}}
    shadow_handler.shadowUpdate(json.dumps(payload), shadow_callback_update, 5)


def shadow_callback_update(payload, status, token):
    logger.debug("IOT update: %s", status)

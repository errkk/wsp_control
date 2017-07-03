import requests

from config import PUMP_ENDPOINT, TEMP_ENDPOINT, AUTH, logger

def post_data(endpoint, data):

    try:
        r = requests.post(endpoint, data, auth=AUTH)
    except:
        logger.error('Requests error publishing data')
    else:
        if r.status_code != 200:
            logger.error('Http error publishing data: {0}'\
                    .format(r.status_code))
        return r

def post_temp(**data):
    return post_data(TEMP_ENDPOINT, data)

def post_pump(**data):
    return post_data(PUMP_ENDPOINT, data)


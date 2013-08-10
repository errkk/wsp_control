from config import PROBE1, PROBE2


def get_temp(direction='IN'):
    probe = {'in': PROBE1, 'out': PROBE2}[direction]
    with open("/sys/bus/w1/devices/{0}/w1_slave".format(probe)) as tfile:
        text = tfile.read()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        return temperature

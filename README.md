# wsp_control
A Python app to control a solar panel with a Raspberry Pi


    sudo apt-get update
    sudo apt-get install python-dev python-rpi.gpio python-smbus
    sudo python setup.py develop

## Enable SPI:
http://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/

## Ensure 1 Wire bus is enabled:

    sudo vim /etc/modules
    
...add this to the bottom to load the modules:
    w1-gpio
    w1_therm
    
And edit `/boot/config.txt` adding

    dtoverlay=w1-gpio
    
to the bottom.

## Command line utilities

Check pump state

    sudo wcheck

Turn pump on and off

    sudo won
    sudo woff

Auto, for testing

    sudo wtoggle


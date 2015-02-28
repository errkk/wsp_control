# wsp_control
A Python app to control a solar panel with a Raspberry Pi

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


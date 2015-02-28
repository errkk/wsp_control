# wsp_control
A Python app to control a solar panel with a Raspberry Pi

# Ensure 1 Wire bus is enabled:
    sudo vim /etc/modules
    
...add this to the bottom:
   w1-gpio
   w1_therm

Oryx KB LEDs
~~~~~~~~~~~~~~

****
What
****

A utility to control the LED colors and brightness on the System76 Oryx Pro. Includes modes like:

* Breathing: pulses the brightness of the LEDs in a pattern similar to human breathing. Can hook into CPU usage to determine breathing speed.
* Color gradients: smoothly transition between 2 or more colors. Speed adjustable.
* Seizure disco: just random color flashing as fast as possible.

***
How
***

The class OryxKBDLeds provides R/W access methods to various sysfs endpoints related to KB LEDs. Uses locks to prevent concurrent writes, asserts certain limits aren't exceeded.

class ColorControl uses the prev class to implement certain patterns. Figures out gradients between colors, does the math required to approximate human breathing, etc.

*****
To-Do
*****

* Implement command line options, config files for all settings
* Implement as a systemd service
* Add more patterns, functionality, eg.: link breathing speed to network throughput, etc
* multi-threading, to allow colors and brightness to be modified concurrently

# systemd service for breathe API
# needs config file for service
# /etc/oryxkbleds
# /etc/oryxleds/config.yml
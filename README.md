Oryx KB LEDs
~~~~~~~~~~~~

****
What
****

A utility to control the LED colors and brightness on the System76 Oryx Pro. Includes modes like:

* Breathing: pulses the brightness of the LEDs in a pattern similar to human breathing. Can hook into CPU usage to
determine breathing speed.
* Color gradients: smoothly transition between 2 or more colors. Speed adjustable.
* Seizure disco: just random color flashing as fast as possible.

***
How
***

The class OryxKBDLeds provides R/W access methods to various sysfs endpoints related to KB LEDs. Uses locks to prevent
concurrent writes, asserts certain limits aren't exceeded.

class ColorControl uses the prev class to implement certain patterns. Figures out gradients between colors, does the
math required to approximate human breathing, etc.

# Usage
manually install, enable, and start the ./systemd/oryxkbleds.service - this sets relevant /sysfs files related to color
& brightness world writable; otherwise would need to run this script as root

make install
$ oryxkbleds --help
usage: oryxkbleds [-h] [--config CONF_PATH] [--mode {breathe,disco}]
                  [--speed SPEED] [--colors SET_COLORS [SET_COLORS ...]]
                  [--brightness SET_BRIGHTNESS]

Oryx KB LED Controller

optional arguments:
  -h, --help            show this help message and exit
  --config CONF_PATH, --conf CONF_PATH, --path CONF_PATH
                        path to config file
  --mode {breathe,disco}, -m {breathe,disco}
                        mode name
  --speed SPEED, -s SPEED
                        speed
  --colors SET_COLORS [SET_COLORS ...], -c SET_COLORS [SET_COLORS ...]
                        set static colors
  --brightness SET_BRIGHTNESS, -b SET_BRIGHTNESS
                        set static brightness

$ oryxkbleds --colors red white blue
$ oryxkbleds --mode breathe

*****
To-Do
*****

* Implement config files for all settings
* Implement as a systemd service
* Add more patterns, functionality, eg.: link breathing speed to network throughput, etc

# systemd service for breathe API
# needs config file for service
# /etc/oryxkbleds
# /etc/oryxleds/config.yml
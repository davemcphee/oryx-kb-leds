#!/bin/env python3

"""
Oryx_KB_LEDs
~~~~~~~~~~~~

Does blinky flashy lighty thing on Oryx4 Pro KB

"""
import os
from threading import RLock
from colour import Color


class OryxKBDLeds(object):
    def __init__(self):
        self.led_base_dir = '/sys/class/leds/system76::kbd_backlight'
        self.led_locations = [os.path.join(self.led_base_dir, "color_{}".format(pos))
                              for pos in ['left', 'center', 'right']]
        self.brightness_path = os.path.join(self.led_base_dir, 'brightness')
        self._max_brightness = int(open(os.path.join(self.led_base_dir, 'max_brightness'), 'r').read().strip())
        for setting_file in self.led_locations + [self.brightness_path]:
            assert os.access(
                setting_file, os.W_OK), "Please ensure use has write access to following settings: {}".format(
                "\n".join(self.led_locations + [self.brightness_path])
            )
        self._color_rlock = RLock()
        self._brightness_lock = RLock()

    @property
    def colors(self):
        return tuple(open(path, 'r').read().strip() for path in self.led_locations)

    @colors.setter
    def colors(self, vals):
        """
        Given a tuple of 3 hex values, will set those values to left, center, right
        """
        assert isinstance(vals, tuple)
        with self._color_rlock:
            for path, v in zip(self.led_locations, vals):
                with open(path, 'w+') as led:
                    led.write(str(v))

    @property
    def brightness(self):
        return int(open(self.brightness_path, 'r').read().strip())

    @brightness.setter
    def brightness(self, val):
        assert isinstance(val, int)
        if val > self.max_brightness:
            val = self.max_brightness
        with self._brightness_lock:
            with open(self.brightness_path, 'w+') as brightness:
                brightness.write(str(val))

    @property
    def max_brightness(self):
        return self._max_brightness

    @max_brightness.setter
    def max_brightness(self, *_):
        raise IOError("Max Brightness is a read-only value.")

    @staticmethod
    def hex_to_rgb(hexx):
        if isinstance(hexx, int):
            hexx = str(hexx)
        elif isinstance(hexx, str):
            if hexx.startswith('0x'):
                hexx = hexx[2:]
            elif hexx.startswith('#'):
                hexx = hex[1:]
        assert len(hexx) == 6
        return tuple(int(hexx[i:i+2], 16) for i in (0, 2, 4))



t = OryxKBDLeds()
vals = t.colors

teal = Color("Cyan")
colors = list(teal.range_to(Color("Magenta"), 100))

original_colors = list(t.colors)

while True:
    for col in colors + list(reversed(colors)):
        for i in range(3):
            original_colors[i] = col.hex_l[1:]
            t.colors = tuple(original_colors)
            # time.sleep(0.01)

# 3 sets of rgb values - either 3 tuples, or 3 strings.




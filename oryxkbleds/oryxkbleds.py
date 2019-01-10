#!/bin/env python3

"""
Oryx_KB_LEDs
~~~~~~~~~~~~

Does blinky flashy lighty thing on Oryx4 Pro KB

"""
import math
import os
import psutil
import random
import time
from collections import deque
from itertools import repeat
from threading import RLock, Thread
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

        # save initial state, so can restore on exit if desired
        self.initial_state_color = self.colors
        self.initial_state_brightness = self.brightness

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

    def reset(self):
        self.colors = self.initial_state_color
        self.brightness = self.initial_state_brightness


class ColorControl(object):
    """
    Uses OryxKBLeds class to implement some patterns.
    """
    def __init__(self):
        self.led_controller = OryxKBDLeds()

    def example_color_transition(self, color_a="red", color_b="blue", speed_s=0.1, forever=False):
        """
        Transitions from a to b, and back again.
        :param color_a: Color
        :param color_b: Color
        :param speed_s: change speed
        :param forever: should we ever stop?
        :return:
        """
        color_start = Color(color_a)
        color_end = Color(color_b)
        colors = list(color_start.range_to(color_end, 100))

        while True:
            original_colors = list(self.led_controller.colors)
            for col in colors + list(reversed(colors)):
                for i in range(3):
                    original_colors[i] = col.hex_l[1:]
                    self.led_controller.colors = tuple(original_colors)
                    # time.sleep(speed_s)
                time.sleep(speed_s)
            if not forever:
                break
        return

    def breathe(self, forever=False):
        """
        Pulses brightness, speed depends on cpu load
        :return: True
        """

        sleep_timers = [
            0.05, 0.04, 0.03, 0.02, 0.01, 0.009, 0.008, 0.005, 0.003, 0.001, 0.0007, 0.0005,
            0.0003, 0.0003, 0.0002, 0.0002, 0.0001
        ]

        theta = 0.0
        tan_list = []
        while True:
            tan_list.append(math.sin(theta))
            theta += 0.01
            if theta >= 3.14159:
                break

        # store last ... 3 cpu percent values and take average, to avoid jitter
        cpu_percent_cache = deque([], 7)

        while True:
            for i in tan_list + list(reversed(tan_list)):
                self.led_controller.brightness = int(i * 255)
                # get current cpu load percentage, 0-100
                cpu_per = psutil.cpu_percent()
                cpu_per = cpu_per / 100.0

                if cpu_per >= 1:
                    cpu_per = 0.99

                cpu_percent_cache.append(cpu_per)
                avg_cpu = sum(cpu_percent_cache) / len(cpu_percent_cache)

                sleep_time_map = sleep_timers[int(len(sleep_timers) * avg_cpu)]
                print("cpu percent: {:.2f}\tsleep timer: {}".format(avg_cpu, sleep_time_map))
                time.sleep(sleep_time_map)
            if not forever:
                break

        self.led_controller.reset()
        return

    def disco(self):
        init_colors = list(self.led_controller.colors)
        cols = ['red', 'green', 'blue']
        colors = [Color(x).hex_l[1:] for x in cols]

        while True:
            for c in range(3):
                init_colors[c] = random.choice(colors)
                self.led_controller.colors = tuple(init_colors)
                time.sleep(0.05)
            time.sleep(0.05)


cc = ColorControl()
# # cc.example_color_transition("BlueViolet", "RosyBrown", speed_s=0.0, forever=True)
cc.breathe(forever=True)
#cc.disco()


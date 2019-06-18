#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit
import math
import random
import string
import time
from collections import deque
from threading import Thread, Event

import psutil
from colour import Color

from oryxkbleds.oryxkbleds import OryxKBDLeds


class ColorControl(object):
    """
    Uses OryxKBLeds class to implement some patterns.
    """
    def __init__(self):
        self.led_controller = OryxKBDLeds()
        self.threads = list()
        self.thread_stop = Event()
        self.should_reset = False
        atexit.register(self.stop)

    def stop(self):
        if self.threads:
            # print("setting kill flag")
            self.thread_stop.set()
            for t in self.threads:
                t.join()
        if self.should_reset:
            self.led_controller.reset()

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
            if not forever or self.thread_stop.isSet():
                break
        return

    def _forever_wrapper(self, func, *args, **kwargs):
        """checks for forever == True, and runs method in thread instead"""
        if 'forever' in kwargs.keys() and kwargs['forever']:
            # forever is set, run <func> it's own func forever (or interrupted)
            our_func = getattr(self, func, None)
            if callable(our_func):
                t = Thread(target=our_func, args=args, kwargs=kwargs)
                self.threads.append(t)
                t.start()
            else:
                raise NotImplementedError("Missing function {} - this is a bug".format(func))
        else:
            self._breathe(*args, **kwargs)

    def breathe(self, *args, **kwargs):
        """either launches func _breathe, or runs it in it's own thread if forever"""
        self._forever_wrapper('_breathe', *args, **kwargs)

    def _breathe(self, forever=False):
        """
        Pulses brightness, speed depends on cpu load
        :return: True
        """

        self.should_reset = True

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
                if self.thread_stop.is_set():
                    break
                self.led_controller.brightness = int(i * 255)
                # get current cpu load percentage, 0-100
                cpu_per = psutil.cpu_percent()
                cpu_per = cpu_per / 100.0

                if cpu_per >= 1:
                    cpu_per = 0.99

                cpu_percent_cache.append(cpu_per)
                avg_cpu = sum(cpu_percent_cache) / len(cpu_percent_cache)

                sleep_time_map = sleep_timers[int(len(sleep_timers) * avg_cpu)]
                time.sleep(sleep_time_map)
            if not forever or self.thread_stop.is_set():
                break

        self.led_controller.reset()
        return

    def disco(self):
        self.should_reset = True

        init_colors = list(self.led_controller.colors)
        cols = ['red', 'green', 'blue']
        colors = [Color(x).hex_l[1:] for x in cols]

        while True:
            for c in range(3):
                init_colors[c] = random.choice(colors)
                self.led_controller.colors = tuple(init_colors)
                # time.sleep(0.05)
            # time.sleep(0.05)

    @staticmethod
    def cast_colors(vals):
        """
        We only test the first item in the tuple, and assume the
        other two are the same
        """
        if not isinstance(vals, tuple):
            raise ValueError("cast_colors() takes a tuple of colors")

        if vals[0].startswith('0x'):
            return tuple([x[2:].upper() for x in vals])
        elif all(c in string.hexdigits for c in vals[0]):
            return tuple([x.upper() for x in vals])
        else:
            # are these string colors?
            try:
                new_vals = tuple([Color(x).get_hex_l() for x in vals])
                return tuple([x[1:].upper() for x in new_vals])
            except Exception:
                print("What are these supposed to be, 3 colors?")
                raise

    def set_colors(self, colors):

        clean_values = self.cast_colors(colors)
        self.led_controller.colors = clean_values

    def set_brightness(self, brightness):
        assert isinstance(brightness, int)
        self.led_controller.brightness = brightness


# if __name__ == '__main__':
#     cc = ColorControl()
#     cc.set_colors(('red', 'blue', 'beige'))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import yaml

from . import colorcontrol


def parse_config(path):
    abs_path = path
    if os.path.isfile(path):
        pass

    elif not os.path.isabs(path):
        here = os.path.dirname(os.path.realpath(__file__))
        abs_path = os.path.join(here, path)

    if not os.path.isfile(abs_path):
        raise IOError(f"{abs_path} not found")

    with open(abs_path, "r") as conf_file:
        config = yaml.load(conf_file)

    if 'brightness' in config:
        set_brightness(config['brightness'])
    if 'color' in config:
        set_colors(tuple(config.colors))
    if 'mode' in config:
        led_mode(config['mode'])


def led_mode(mode):
    cc = colorcontrol.ColorControl()
    func = getattr(cc, mode, None)

    if not func:
        raise NotImplementedError(f"ColorControl.{func}() does not exist")

    try:
        func()
    except KeyboardInterrupt:
        pass


def set_colors(colors):
    cc = colorcontrol.ColorControl()
    cc.set_colors(tuple(colors))


def set_brightness(brightness):
    cc = colorcontrol.ColorControl()
    cc.set_brightness(int(brightness))


def entry_point():
    parser = argparse.ArgumentParser(description='Oryx KB LED Controller')

    parser.add_argument('--config', '--conf', '--path', action="store", type=str, help="path to config file",
                        dest="conf_path")

    parser.add_argument('--mode', '-m', help="mode name", choices=["breathe", "disco"], dest="led_mode")
    parser.add_argument('--speed', '-s', help="speed", type=int, dest="speed")
    parser.add_argument('--colors', '-c', help="set static colors", dest="set_colors", nargs="+")
    parser.add_argument('--brightness', '-b', help="set static brightness", dest="set_brightness")

    args = parser.parse_args()
    # parser.parse_args('--foo 1 --foo 2'.split())
    if sum(map(bool, [args.conf_path, args.led_mode, args.set_colors, args.set_brightness])) > 1:
        parser.error("config, mode, colors and brightness are mutually exclusive")

    if args.conf_path:
        parse_config(args.conf_path)
    elif args.led_mode:
        led_mode(args.led_mode)
    elif args.set_colors:
        set_colors(args.set_colors)
    elif args.set_brightness:
        set_brightness(args.set_brightness)
    else:
        raise ValueError("Say what ?!")


if __name__ == '__main__':
    entry_point()

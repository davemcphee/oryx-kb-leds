import os
import random
import time

import pytest


@pytest.fixture
def rnd_colors():
    def r():
        return random.randint(0, 255)
    return ('%02X%02X%02X' % (r(), r(), r()),
            '%02X%02X%02X' % (r(), r(), r()),
            '%02X%02X%02X' % (r(), r(), r())
            )


@pytest.fixture
def okbled():
    from oryxkbleds.oryxkbleds import OryxKBDLeds
    return OryxKBDLeds()


def test_color_property_get(okbled):
    colors = okbled.colors
    print(colors)
    assert isinstance(colors, tuple)
    for c in colors:
        assert isinstance(c, (bytes, str))
    assert len(colors) == 3


def test_color_property_set(okbled, rnd_colors):
    okbled.colors = rnd_colors
    assert okbled.colors == rnd_colors


def test_brightness_property_get(okbled):
    b = okbled.brightness
    assert isinstance(b, int)


def test_brightness_property_set(okbled):
    max_b = okbled.max_brightness
    okbled.brightness = max_b
    time.sleep(0.1)
    assert okbled.brightness == max_b

    b = 97
    okbled.brightness = b
    time.sleep(0.1)
    assert okbled.brightness == b


def test_max_brightness_property_get(okbled):
    b = okbled.brightness
    assert isinstance(b, int)


def test_max_brightness_property_set(okbled):
    with pytest.raises(IOError):
        okbled.max_brightness = 123


def test_sys_write_permissions(okbled):
    for f in okbled.led_locations + [okbled.brightness_path]:
        assert os.access(f, os.W_OK)

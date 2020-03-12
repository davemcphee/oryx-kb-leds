import pytest


@pytest.fixture
def cc():
    from oryxkbleds.colorcontrol import ColorControl
    return ColorControl()


def test_cc_led_controller(cc):
    from oryxkbleds.ledcontrol import OryxKBDLeds
    assert isinstance(cc.led_controller, OryxKBDLeds)


def test_stop(cc):
    cc.stop()
    assert cc.threads == []


def test_version_is_set(cc):
    from oryxkbleds import __version__
    assert __version__.__version__ is not None
    assert isinstance(__version__.__version__, str)


def test_cast_colors_not_a_tuple(cc):
    with pytest.raises(ValueError):
        cc.cast_colors(["pure", "garbage", "list"])


def test_cast_colors_not_real_colours(cc):
    assert isinstance(cc.cast_colors(("reed", "bloo", "wite")), ValueError)


def test_cast_colors_0x_hex(cc):
    hex_vals = ("0xdeadbeef", "0xFF00FF", "0xaabbcd")
    ret = cc.cast_colors(hex_vals)
    assert ret == ("DEADBEEF", "FF00FF", "AABBCD")


def test_cast_colors_hex_no_0x(cc):
    hex_vals = ("deadbeef", "FF00FF", "aabbcd")
    ret = cc.cast_colors(hex_vals)
    assert ret == ("DEADBEEF", "FF00FF", "AABBCD")


def test_cast_colors_string_colors(cc):
    hex_vals = ("red", "pink", "PURPLE")
    ret = cc.cast_colors(hex_vals)
    assert ret == ("FF0000", "FFC0CB", "800080")


def test_threaded_disco_stop(cc):
    cc.disco(forever=True)
    assert len(cc.threads) > 0
    cc.stop()
    assert len(cc.threads) == 0


def test_threaded_breathe_stop(cc):
    cc.breathe(forever=True)
    assert len(cc.threads) > 0
    cc.stop()
    assert len(cc.threads) == 0

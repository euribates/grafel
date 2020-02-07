#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pytest
from colors import Color


def test_create_color():
    Color(12, 33, 211)


@pytest.fixture
def color():
    return Color(12, 33, 211)


def test_set_red_value(color):
    color.red = 64
    assert color.red == 64
    assert str(color) =='#4021d3'


def test_set_green_value(color):
    color.green = 64
    assert color.green == 64
    assert str(color) == '#0c40d3'


def test_set_blue_value(color):
    color.blue = 64
    assert color.blue == 64
    assert str(color) == '#0c2140'


def test_creation_from_tuple(color):
    assert color.red == 12
    assert color.r == 12
    assert color.green == 33
    assert color.g == 33
    assert color.blue == 211
    assert color.b == 211


def test_as_rgb(color):
    assert color.as_rgb() == (12, 33, 211)


def test_as_hex(color):
    assert color.as_hex() == '#0c21d3'


def test_as_rgb(color):
    assert color.as_svg() == 'rgb(12,33,211)'


def test_equal():
    r1 = Color('azure')
    r2 = Color(240, 255, 255)
    assert r1 == r2


_named_colors = {
    'aliceblue': (240, 248, 255),
    'brown4': (139, 35, 35),
    'cadetblue': (95, 158, 160),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 128, 0),
    'yellow': (255, 255, 0),
    'black': (0, 0, 0),
    }

@pytest.fixture(params=_named_colors.items(), ids=_named_colors.keys())
def named_colors(request): 
    name, rgb = request.param
    return Color(name), rgb 


def test_names(named_colors):
    color, (red, green, blue) = named_colors
    assert color.red == red
    assert color.green == green
    assert color.blue == blue


def test_wrong_color_name():
    with pytest.raises(ValueError):
        Color('non-existing-color')


def test_hexcodes():
    c = Color('#32BF98')
    assert c.red == 50
    assert c.green == 191
    assert c.blue == 152


def test_create_by_random_values():
    for r in random.sample(range(0, 256), 12):
        for g in random.sample(range(0, 256), 12):
            for b in random.sample(range(0, 256), 12):
                c = Color(r, g, b)
                assert c.red == r
                assert c.green == g
                assert c.blue == b


if __name__ == '__main__':
    pytest.main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import random
import unittest
from colors import Color

class TestColor(unittest.TestCase):

    def test_creation_from_tuple(self):
        c = Color(12, 33, 211)
        self.assertEqual(c.red, 12)
        self.assertEqual(c.r, 12)
        self.assertEqual(c.green, 33)
        self.assertEqual(c.g, 33)
        self.assertEqual(c.blue, 211)
        self.assertEqual(c.b, 211)
    
    def test_as_rgb(self):
        c = Color(12, 33, 211)
        self.assertEqual(c.as_rgb(), (12, 33, 211))

    def test_as_hex(self):
        c = Color(12, 33, 211)
        self.assertEqual(c.as_hex(), '#0c21d3')

    def test_as_rgb(self):
        c = Color(12, 33, 211)
        self.assertEqual(c.as_svg(), 'rgb(12,33,211)')

    def test_equal(self):
        r1 = Color('azure')
        r2 = Color(240, 255, 255)
        self.assertEqual(r1, r2)

    def test_pure_colors(self):
        white = Color('white')
        assert white.r == 255 and white.g == 255 and white.b == 255
        red = Color('red')
        assert red.r == 255 and red.g == 0 and red.b == 0
        red = Color('blue')
        assert red.r == 0 and red.g == 0 and red.b == 255
        red = Color('green')
        assert red.r == 0 and red.g == 128 and red.b == 0
        black = Color('black')
        assert black.r == 0 and black.g == 0 and black.b == 0
        yellow = Color('yellow')
        assert yellow.r == 255 and yellow.g == 255 and yellow.b == 0


    def test_names(self):

        aliceblue = Color('aliceblue')
        assert aliceblue.red == 240 
        assert aliceblue.green == 248 
        assert aliceblue.blue == 255

        brown4 = Color('brown4')
        assert brown4.red == 139 
        assert brown4.green == 35 
        assert brown4.blue == 35

        cadetblue = Color('cadetblue')
        assert cadetblue.red == 95 
        assert cadetblue.green == 158 
        assert cadetblue.blue == 160

        self.assertRaises(ValueError, Color, 'no-existo')

    def test_hexcodes(self):
        c = Color('#32BF98')
        self.assertEqual(c.red, 50)
        self.assertEqual(c.green, 191)
        self.assertEqual(c.blue, 152)

    def test_create_by_values(self):
        for r in random.sample(range(0, 256), 12):
            for g in random.sample(range(0, 256), 12):
                for b in random.sample(range(0, 256), 12):
                    c = Color(r, g, b)
                    self.assertEqual(c.red, r)
                    self.assertEqual(c.green, g)
                    self.assertEqual(c.blue, b)

if __name__ == '__main__':
    unittest.main()

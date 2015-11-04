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

    def test_pure_colors(self):
        white = Color('white')
        assert white.red == 255 and white.green == 255 and white.blue == 255

        red = Color('red')
        assert red.red == 255 and red.green == 0 and red.blue == 0
        
        red = Color('blue')
        assert red.red == 0 and red.green == 0 and red.blue == 255

        red = Color('green')
        assert red.red == 0 and red.green == 128 and red.blue == 0

        black = Color('black')
        assert black.red == 0 and black.green == 0 and black.blue == 0

        yellow = Color('yellow')
        assert yellow.red == 255 and yellow.green == 255 and yellow.blue == 0


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


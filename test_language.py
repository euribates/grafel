#!/usr/bin/python3
# -*- coding: utf-8 -*-    

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest
import sys
from vectors import Vector
from colors import Color
import actors
import actions
import language
import logs

test_string = '''
Cast:

    bob = Square size 50x50 color red 
    star = Star color white
'''

#print(table_of_symbols)
#print(result.asList())

logger = logs.create(__name__)

class TestActionLine(unittest.TestCase):

    def test_action_move(self):
        from language import ActionLine 
        l = ActionLine.parseString('1-23 Move bob 50x50')
        t = l[0]
        self.assertEqual(t[0], actions.Interval(1, 23))
        self.assertEqual(t[1], 'Move')
        self.assertEqual(t[2], 'bob')
        self.assertEqual(t[3], Vector(50, 50))

    def test_action_move_relative_interval(self):
        from language import ActionLine 
        l = ActionLine.parseString('10+20 Move bob 50x50')
        t = l[0]
        self.assertEqual(t[0], actions.Interval(10, 30))
        self.assertEqual(t[1], 'Move')
        self.assertEqual(t[2], 'bob')
        self.assertEqual(t[3], Vector(50, 50))

class TestCastLine(unittest.TestCase):

    def test_attr_size(self):
        from language import attr
        l = attr.parseString('size 10x10')
        self.assertEqual(l[0], 'size')
        self.assertEqual(l[1], Vector(10, 10))

    def test_attr_color_name(self):
        from language import attr
        l = attr.parseString('color gold')
        self.assertEqual(l[0], 'color')
        self.assertEqual(l[1], Color('gold'))
        
    def test_attr_color_html_color_code(self):
        from language import attr
        l = attr.parseString('color #FF4433')
        self.assertEqual(l[0], 'color')
        self.assertEqual(l[1], Color(0xFF, 0x44, 0x33))

    def test_attr_pos(self):
        from language import attr
        l = attr.parseString('pos 32x67')
        self.assertEqual(l[0], 'pos')
        self.assertEqual(l[1], Vector(32, 67))

    def test_attr_num(self):
        from language import attr
        from pyparsing import ParseException
        l = attr.parseString('num 1')
        self.assertEqual(l[0], 'num')
        self.assertEqual(l[1], 1)
        self.assertRaises(
            ParseException,  
            attr.parseString,
            'num 7'
            )

    def test_attr_radius(self):
        from language import attr
        l = attr.parseString('radius 100')
        self.assertEqual(l[0], 'radius')
        self.assertEqual(l[1], 100)
    
    def test_attr_width(self):
        from language import attr
        l = attr.parseString('width 100')
        self.assertEqual(l[0], 'width')
        self.assertEqual(l[1], 100)
        
    def test_attr_height(self):
        from language import attr
        l = attr.parseString('height 100')
        self.assertEqual(l[0], 'height')
        self.assertEqual(l[1], 100)

    def test_attr_text_simple_quotes(self):
        from language import attr
        l = attr.parseString("text 'this is a goat'")
        self.assertEqual(l[0], 'text')
        self.assertEqual(l[1], 'this is a goat')

    def test_attr_text_double_quotes(self):
        from language import attr
        l = attr.parseString('text "hello"')
        self.assertEqual(l[0], 'text')
        self.assertEqual(l[1], 'hello')

    def test_attr_alpha(self):
        from language import attr
        l = attr.parseString('alpha .33')
        self.assertEqual(l[0], 'alpha')
        self.assertEqual(l[1], 0.33)
        l = attr.parseString('alpha 0.75')
        self.assertEqual(l[0], 'alpha')
        self.assertEqual(l[1], 0.75)

    def test_attr_points(self):
        from language import attr
        l = attr.parseString('points (33x22, 10x10, 50x50)')
        self.assertEqual(l[0], 'points')
        self.assertEqual(len(l[1]), 3)
        self.assertEqual(l.points[0], Vector(33, 22))
        self.assertEqual(l.points[1], Vector(10, 10)) 
        self.assertEqual(l.points[2], Vector(50, 50))

        l = attr.parseString('points (33x22, 10x10, 50x50,12x12)')
        self.assertEqual(l[0], 'points')
        self.assertEqual(len(l[1]), 4)
        self.assertEqual(l.points[0], Vector(33, 22))
        self.assertEqual(l.points[1], Vector(10, 10)) 
        self.assertEqual(l.points[2], Vector(50, 50))
        self.assertEqual(l.points[3], Vector(12, 12))

    def test_cast_line(self):
        from language import castline

        r = castline.parseString('bob = Square size 50x50 color red')
        self.assertEqual(r.name, 'bob')
        self.assertEqual(r.role, 'Square')
        params = language.params_to_dict(r.params)
        self.assertEqual(params['size'], Vector(50, 50))
        self.assertEqual(params['color'], Color('red'))


if __name__ == '__main__':
    unittest.main()

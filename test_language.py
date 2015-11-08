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

class TestCastLine(unittest.TestCase):

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

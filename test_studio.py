#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_stage.py

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import math
import unittest
from unittest.mock import Mock
import vectors
from vectors import Vector, origin, zero
from studio import Stage
from engines import BaseEngine, SVGEngine, PyGameEngine
from actors import Actor, Square, Star, Dice, Text
from actions import MoveTo, Land, Fall
from colors import Color

class TestBaseEngine(unittest.TestCase):

    def test_calls(self):
        eng = BaseEngine()
        eng.clear(0)
        eng.polygon(0, 0, [(50, 0), (50, 50), (0, 50)], color=Color('white'))
        eng.end()

class TestSVGEngine(unittest.TestCase):

    def test_create_frame(self):
        s = Stage(SVGEngine())
        star = Star('star')
        star.color = 'red'
        star.place(100, 100)
        s.add_actor(star)
        s.add_actor(Square('bob'), on_stage=False)
        s.draw()

    def test_create_sequence(self):
        s = Stage(SVGEngine(), num_frames=100)
        star = Star('star')
        star.color = 'red'
        star.place(0, 0)
        MoveTo(star, 0, 100, s.bottom_right)
        s.add_actor(star)

        bob = Square('bob')
        bob.place(0, s.height // 2)
        Land(bob, 0, 100, Vector(s.width, s.height//2))
        s.add_actor(bob, on_stage=True)
        for frame in range(0, 100):
            s.draw()
            s.next()


class TestPyGameEngine(unittest.TestCase):

    def test_create(self):
        s = Stage(PyGameEngine())
        star = Star('star')
        star.color = 'red'
        star.place(100, 100)
        s.add_actor(star)
        s.add_actor(Square('bob'), on_stage=False)
        s.draw()

    def test_create_sequence(self):
        s = Stage(PyGameEngine(), num_frames=100)
        star = Star('star')
        star.color = 'red'
        star.place(0, 0)
        MoveTo(star, 0, 100, s.bottom_right)
        s.add_actor(star)

        bob = Square('bob')
        bob.place(0, s.height // 2)
        Land(bob, 0, 100, Vector(s.width, s.height//2))
        s.add_actor(bob, on_stage=True)

        dice = Dice('D1')
        s.add_actor(dice)

        for frame in range(0, 100):
            s.draw()
            s.next()

class TestDice(unittest.TestCase):
    
    def test_sequence(self):

        #s = Stage(PyGameEngine(), num_frames=150)
        s = Stage(SVGEngine(output_dir='./tmp'), num_frames=150)
        middle = s.height // 2
        dice1 = Dice('D1', num=1)
        dice1.place(1*s.width//7, middle)
        Land(dice1, 0, 150, Vector(1*s.width//7, s.height-50))
        s.add_actor(dice1)

        dice2 = Dice('D2', num=2)
        dice2.place(2*s.width//7, middle)
        Fall(dice2, 0, 150, Vector(2*s.width//7, s.height-50))
        s.add_actor(dice2)

        dice3 = Dice('D3', num=3)
        dice3.place(3*s.width//7, middle)
        Fall(dice3, 0, 150, Vector(3*s.width//7, 50))
        s.add_actor(dice3)

        dice4 = Dice('D4', num=4)
        dice4.place(4*s.width//7, middle)
        Land(dice4, 0, 150, Vector(4*s.width//7, 50))
        s.add_actor(dice4)
        
        dice5 = Dice('D5', num=5)
        dice5.place(5*s.width//7, middle)
        MoveTo(dice5, 0, 150, Vector(5*s.width//7, s.height-50))
        s.add_actor(dice5)

        dice6 = Dice('D6', num=6)
        dice6.place(6*s.width//7, middle)
        MoveTo(dice6, 0, 150, Vector(6*s.width//7, 50))
        s.add_actor(dice6)

#        t1 = Text('Texto1')
#        t1.place(s.width//2, 50)
#        for i in range(0, 150, 25):
#            Land(t1, i, i+25, vectors.get_random_position_vector(s.width, s.height))
#            Fall(t1, i, i+25, vectors.get_random_position_vector(s.width, s.height))
#        s.add_actor(t1)

        for frame in range(0, 250):
            s.draw()
            s.next()




if __name__ == '__main__':
    unittest.main()


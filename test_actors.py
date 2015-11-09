#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_actors.py

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import math
import unittest
import random

from vectors import Vector
import actors
from actors import State, Actor, Square, Star
from colors import Color
import logs

logger = logs.create(__name__)

class TestState(unittest.TestCase):

    def test_create_state_without_params(self):
        state = State()
        self.assertEqual(state.pos, Vector(0, 0))
        self.assertEqual(state.color.name, 'white')
        self.assertEqual(state.scale, Vector(1, 1))
        self.assertEqual(state.alpha, 1.0)

    def test_create_state_with_params(self):
        state = State(
            pos=Vector(3,4),
            color='red',
            scale=Vector(50, 100),
            alpha=0.5
            )
        self.assertEqual(state.pos, Vector(3, 4))
        self.assertEqual(state.color.name, 'red')
        self.assertEqual(state.scale.x, 50)
        self.assertEqual(state.scale.y, 100)
        self.assertEqual(state.alpha, 0.5)

    def test_alter_state_relative_pos(self):
        state = State()
        state.delta(pos=Vector(1,2))
        self.assertEqual(state.pos.x, 1)
        self.assertEqual(state.pos.y, 2)
        state.delta(pos=Vector(1,2))
        self.assertEqual(state.pos.x, 2)
        self.assertEqual(state.pos.y, 4)

    def test_alter_state_color(self):
        state = State()
        state.delta(color='red')
        self.assertEqual(state.color.name, 'red')

    def test_alter_state_relative_scale(self):
        state = State()
        state.delta(scale=Vector(1,2))
        self.assertEqual(state.scale, Vector(1,2))
        state.delta(scale=Vector(2,1))
        self.assertEqual(state.scale, Vector(2,2))
        state.delta(scale=Vector(3,2))
        self.assertEqual(state.scale, Vector(6,4))

    def test_alter_state_alpha(self):
        state = State()
        state.delta(alpha=0.75)
        self.assertEqual(state.alpha, 0.75)

            

class TestActor(unittest.TestCase):

    def test_as_string(self):
        a = Actor('A')
        self.assertEqual(str(a), 'Actor A')

    def test_creacion_actor(self):
        a = Actor('A')
        self.assertEqual(a.name, 'A')
        self.assertEqual(a.frame, 0)
        self.assertEqual(a.pos.x, 0)
        self.assertEqual(a.pos.y, 0)
        self.assertEqual(a.color.name, 'white')
        self.assertEqual(a.color.red, 255)
        self.assertEqual(a.color.green, 255)
        self.assertEqual(a.color.blue, 255)

        self.assertEqual(a.scale.x, 1)
        self.assertEqual(a.scale.y, 1)
        self.assertEqual(a.alpha, 1.0)


    def test_move_actor(self):
        a = Actor('A')
        a.place(100, 200)
        self.assertEqual(a.pos.x, 100)
        self.assertEqual(a.pos.y, 200)
        a.pos += Vector(-2, 4)
        self.assertEqual(a.pos.x, 98)
        self.assertEqual(a.pos.y, 204)



class TestLabel(unittest.TestCase):

    def test_create_label(self):
        label = actors.Label('l1', 'L1')
        self.assertEqual(label.name, 'l1')
        self.assertEqual(label.text, 'L1')

class TestSquare(unittest.TestCase):

    def test_creacion_square_bob(self):
        bob = Square('Bob', pos=(23, 74))
        self.assertEqual(bob.name, 'Bob')
        self.assertEqual(bob.pos.x, 23)
        self.assertEqual(bob.pos.y, 74)
        self.assertEqual(bob.initial_state.pos.x, 23)
        self.assertEqual(bob.initial_state.pos.y, 74)
        self.assertEqual(bob.width, 50)
        self.assertEqual(bob.height, 50)

    def test_as_string(self):
        bob = Square('Bob')
        self.assertEqual(str(bob), 'Square Bob')


class ComposeActors(unittest.TestCase):

    def test_creation_of_combined_actors(self):
        p = Actor('Parent')
        bob = Square('bob')
        p.add_son(bob)
        star = Star('star')
        p.add_son(star)
        self.assertEqual(len(p.sons), 2)
        self.assertEqual(p.sons[0].name, 'bob')
        self.assertEqual(p.sons[1].name, 'star')
        self.assertEqual(bob.parent, p)
        self.assertEqual(star.parent, p)
        self.assertEqual(p.parent, None)



    def test_get_offset(self):
        a = Actor('A', pos=(50, 70))
        self.assertEqual(a.pos, (50, 70))
        self.assertEqual(a.get_offset(), (0, 0))
        b = Actor('B', pos=(10, 10))
        self.assertEqual(b.pos, (10, 10))
        self.assertEqual(b.get_offset(), (0, 0))
        a.add_son(b)
        self.assertEqual(b.pos, (10, 10))
        self.assertEqual(b.get_offset(), (50, 70))
        c = Actor('C', pos=(11, 22))
        self.assertEqual(c.pos, (11, 22))
        self.assertEqual(c.get_offset(), (0, 0))
        b.add_son(c)
        self.assertEqual(c.pos, (11, 22))
        self.assertEqual(c.get_offset(), (60, 80))








if __name__ == '__main__':
    unittest.main()








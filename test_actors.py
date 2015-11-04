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

class TestState(unittest.TestCase):

    def test_create_state_without_params(self):
        state = State()
        self.assertEqual(state.pos, Vector(0, 0))
        self.assertEqual(state.color.name, 'white')
        self.assertEqual(state.scale, Vector(1, 1))
        self.assertEqual(state.alpha, 1.0)

    def test_create_state_with_params(self):
        state = State(Vector(3,4), 'red', Vector(50, 100), 0.5)
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
        self.assertEqual(a.state.pos.x, 0)
        self.assertEqual(a.state.pos.y, 0)
        self.assertEqual(a.state.color.name, 'white')
        self.assertEqual(a.state.color.red, 255)
        self.assertEqual(a.state.color.green, 255)
        self.assertEqual(a.state.color.blue, 255)

        self.assertEqual(a.state.scale.x, 1)
        self.assertEqual(a.state.scale.y, 1)
        self.assertEqual(a.state.alpha, 1.0)


    def test_move_actor(self):
        a = Actor('A')
        a.place(100, 200)
        self.assertEqual(a.state.pos.x, 100)
        self.assertEqual(a.state.pos.y, 200)
        a.state.pos += Vector(-2, 4)
        self.assertEqual(a.state.pos.x, 98)
        self.assertEqual(a.state.pos.y, 204)

class TestBob(unittest.TestCase):

    def test(self):
        import sys
        from actors import Square
        from actions import MoveTo

        bob = Square('Bob', State(color='cadetblue'), width=50, height=50)
        MoveTo(bob, 0, 10, Vector(100, 0))
        dump = bob.dump(40)

class CreateManyActors(unittest.TestCase):

    def test(self):
        from actions import Fall, MoveTo

        charles = Square('Charles', 
            State(pos=Vector(100, 0), color='brown4'), 
            width=75, height=25
            )
        self.assertEqual(len(charles.actions[0]), 0)
        Fall(charles, 0, 40, Vector(100, 300))
        self.assertEqual(len(charles.actions[0]), 1)

        dorothy = Square('Dorothy', 
            state=State(pos=Vector(400, 5), color='#32BF98'),
            width=75, height=25
            )

        self.assertEqual(len(dorothy.actions[0]), 0)
        MoveTo(dorothy, 0, 40, Vector(100, 300))
        self.assertEqual(len(dorothy.actions[0]), 1)

        charles.next()

        self.assertEqual(len(charles.actions[0]), 1)
        self.assertEqual(len(dorothy.actions[0]), 1)
        
        self.assertEqual(charles.state.pos.x, 100)
        self.assertEqual(charles.state.pos.y, 0)
        self.assertEqual(str(charles.state.color), 'brown4')

        self.assertEqual(dorothy.state.pos.x, 400)
        self.assertEqual(dorothy.state.pos.y, 5)
        self.assertEqual(str(dorothy.state.color), '#32BF98')


class TestSquare(unittest.TestCase):

    def test_creacion_square_bob(self):
        bob = Square('Bob', State(pos=Vector(23, 74)))
        self.assertEqual(bob.name, 'Bob')
        self.assertEqual(bob.initial_state.pos.x, 23)
        self.assertEqual(bob.initial_state.pos.y, 74)
        self.assertEqual( len(bob.vertexs), 4 )

    def test_as_string(self):
        bob = Square('Bob')
        self.assertEqual(str(bob), 'Square Bob')


class ComposeActors(unittest.TestCase):

    def test_creation_of_combined_actors(self):
        p = Actor('Parent')
        p.place(100, 100)
        box = Square('bob')
        p.sons.append(box)
        star = Star('star')
        p.sons.append(star)

if __name__ == '__main__':
    unittest.main()








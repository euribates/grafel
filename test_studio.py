#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_stage.py

import math
import unittest
from unittest.mock import Mock
import vectors
from vectors import Vector, origin, zero
from studio import Stage
from engines import BaseEngine, SVGEngine, PyGameEngine
from actors import Actor, Square, Star, Dice, Text, Label, Bitmap
from actions import Move, Land, Fall, Swing
from colors import Color
from control import Scheduler
import logs

logger = logs.create(__name__)

class TestSVGEngine(unittest.TestCase):

    def test_create_frame(self):
        s = Stage(SVGEngine(output_dir='./tmp'))
        star = Star('star', color='red', pos=(0, 0))
        s.add_actor(star)
        s.add_actor(Square('bob'))
        s.draw(0)

    def test_create_sequence(self):

        # stage = Stage(SVGEngine(output_dir='./tmp'))
        stage = Stage()
        stage.num_frames = 100
        star = Star('star', color='red', pos=(0, 0))
        stage.add_actor(star)
        stage.add_action(Move(star, 0, 100, stage.refs['bottom_right']))

        bob = Square('bob', pos=stage.refs['center'])
        stage.add_actor(bob)
        stage.add_action(Land(bob, 0, 100, (stage.width, stage.height//2)))

        for frame in range(0, 100):
            stage.draw(frame)


class TestPyGameEngine(unittest.TestCase):

    def test_create(self):
        s = Stage(PyGameEngine())

    def test_create_sequence(self):
        s = Stage(PyGameEngine())
        s.num_frames = 100
        star = Star('star', color='gold', pos=(1280, 720), radius=20)
        s.add_actor(star)

        bob = Square('bob', pos=(0, s.height // 2))
        s.add_actor(bob)
        
        dice = Dice('D1', pos=(400, 400))
        s.add_actor(dice)

        mf = Bitmap('mf', 'mf.png', pos=(200, 200))
        s.add_actor(mf)

        sch = Scheduler()
        sch.add_action(Move(star, 0, 100, (0,0)))
        sch.add_action(Swing(mf, 0, 100, (1080,520)))
        sch.add_action(Land(bob, 0, 100, Vector(s.width, s.height//2)))

        for frame in range(0, 100):
            s.draw(frame)
            sch.next()

class TestDices(unittest.TestCase):
    
    def test_sequence(self):

        sch = Scheduler()
        s = Stage(PyGameEngine())
        s.num_frames=80
        #s = Stage(SVGEngine(output_dir='./tmp'), num_frames=150)
        middle = s.height // 2
        dice1 = Dice('D1', num=1)
        dice1.place(1*s.width//7, middle)
        sch.add_action(Land(dice1, 0, 60, Vector(1*s.width//7, s.height-50)))
        sch.add_action(Swing(dice1, 60, 80, dice1.initial_state.pos))
        s.add_actor(dice1)

        dice2 = Dice('D2', num=2)
        dice2.place(2*s.width//7, middle)
        sch.add_action(Fall(dice2, 0, 60, Vector(2*s.width//7, s.height-50)))
        sch.add_action(Swing(dice2, 60, 80, dice2.initial_state.pos))
        s.add_actor(dice2)

        dice3 = Dice('D3', num=3)
        dice3.place(3*s.width//7, middle)
        sch.add_action(Fall(dice3, 0, 60, Vector(3*s.width//7, 50)))
        sch.add_action(Swing(dice3, 60, 80, dice3.initial_state.pos))
        s.add_actor(dice3)

        dice4 = Dice('D4', num=4)
        dice4.place(4*s.width//7, middle)
        sch.add_action(Land(dice4, 0, 60, Vector(4*s.width//7, 50)))
        sch.add_action(Swing(dice4, 60, 80, dice4.initial_state.pos))
        s.add_actor(dice4)
        
        dice5 = Dice('D5', num=5)
        dice5.place(5*s.width//7, middle)
        sch.add_action(
            Move(dice5, 0, 60, Vector(5*s.width//7, s.height-50))
            )
        sch.add_action(Swing(dice5, 60, 80, dice5.initial_state.pos))
        s.add_actor(dice5)

        dice6 = Dice('D6', num=6)
        dice6.place(6*s.width//7, middle)
        sch.add_action(Move(dice6, 0, 60, Vector(6*s.width//7, 50)))
        sch.add_action(Swing(dice6, 60, 80, dice6.initial_state.pos))
        s.add_actor(dice6)

        t1 = Label('Texto1', pos=(s.width//2, 50),
            color='gold',
            width=200,
            height=100,
            )
        for i in range(0, 81, 20):
            fall_pos = vectors.get_random_position_vector(s.width, s.height)
            land_pos = vectors.get_random_position_vector(s.width, s.height)
            sch.add_action(Land(t1, i, i+25, fall_pos))
            sch.add_action(Fall(t1, i, i+25, land_pos))

        s.add_actors(t1)

        for frame in range(0, 100):
            s.draw(frame)
            sch.next()




if __name__ == '__main__':
    unittest.main()


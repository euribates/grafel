#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_actions.py

import sys
import math
import logging
import unittest

import logs
import actions
from vectors import Vector
from studio import Stage
from control import Scheduler
from actors import Actor, Square, State, Label, Text, Rect
import colors
from engines import PyGameEngine
import random

logger = logs.create(__name__)

class TestActions(unittest.TestCase):

    def test_uso(self):
        sch = Scheduler()
        bob = Square('Bob')
        task = actions.Action(bob, 5, 10)
        sch.add_action(task)
        self.assertTrue((task.actor.name, 5) in sch.actions)

    def test_get_relative_frame(self):
        task = actions.Action(Actor('A'), 5, 10)
        self.assertEqual(task.get_relative_frame(5), 0)
        self.assertEqual(task.get_relative_frame(6), 1)
        self.assertEqual(task.get_relative_frame(7), 2)
        self.assertEqual(task.get_relative_frame(8), 3)
        self.assertEqual(task.get_relative_frame(9), 4)
        self.assertEqual(task.get_relative_frame(10), 5)


    def test_action_inverval(self):
        task = actions.Action(Actor('A'), 5, 10)
        self.assertEqual(task.lower_bound, 5)
        self.assertEqual(task.upper_bound, 10)
        self.assertEqual(task.num_steps, 5)

    def test_last_frame(self):
        task = actions.Action(Actor('A'), 5, 10)
        self.assertRaises(ValueError, task.is_last, 4)
        self.assertFalse(task.is_last(5))
        self.assertFalse(task.is_last(6))
        self.assertFalse(task.is_last(7))
        self.assertFalse(task.is_last(8))
        self.assertFalse(task.is_last(9))
        self.assertTrue(task.is_last(10))
        self.assertRaises(ValueError, task.is_last, 11)


    def test_calls(self):
        sch = Scheduler()

        class TestAction(actions.Action):
            def start(self, frame):
                self.started_at_frame = frame
                self.called_on_frames = []

            def step(self, frame):
                self.called_on_frames.append(frame)

            def end(self, frame):
                self.ended_at_frame = frame

        a = Actor('A')
        task = TestAction(a, 3, 6)
        sch.add_action(task)
        for f in range(15):
            sch.next()
        self.assertEqual(task.started_at_frame, 3)
        self.assertEqual(task.ended_at_frame, 6)
        self.assertEqual(task.called_on_frames, [4, 5, 6])


    def test_start(self):
        sch = Scheduler()
        bob = Actor('Bob')
        sch.add_action(actions.Move(bob, 5, 10, Vector(72, 54)))
        sch.add_action(actions.Blink(bob, 8, 12))

        self.assertEqual(len(sch.active_actions), 0)  # 0
        sch.next(); self.assertEqual(len(sch.active_actions), 0)  # 1
        sch.next(); self.assertEqual(len(sch.active_actions), 0)  # 2
        sch.next(); self.assertEqual(len(sch.active_actions), 0)  # 3
        sch.next(); self.assertEqual(len(sch.active_actions), 0)  # 4
        sch.next(); self.assertEqual(len(sch.active_actions), 0) # 5
        sch.next(); self.assertEqual(len(sch.active_actions), 1)  # 6
        sch.next(); self.assertEqual(len(sch.active_actions), 1)  # 7
        sch.next(); self.assertEqual(len(sch.active_actions), 1)  # 8
        sch.next(); self.assertEqual(len(sch.active_actions), 2)  # 9
        sch.next(); self.assertEqual(len(sch.active_actions), 2)  # 10
        sch.next(); self.assertEqual(len(sch.active_actions), 1)  # 11
        sch.next(); self.assertEqual(len(sch.active_actions), 1)  # 12
        sch.next(); self.assertEqual(len(sch.active_actions), 0)  # 13
        sch.next(); self.assertEqual(len(sch.active_actions), 0)  # 14
        sch.next(); self.assertEqual(len(sch.active_actions), 0)  # 15

class TestMove(unittest.TestCase):

    def test_move_not_in_origin(self):
        sujeto = Actor('A', pos=Vector(50, 50))
        a = actions.Move(sujeto, 0, 5, Vector(50, 0))
        a.start(0)
        a.step(1); self.assertEqual(sujeto.pos, Vector(50, 40))
        a.step(2); self.assertEqual(sujeto.pos, Vector(50, 30))
        a.step(3); self.assertEqual(sujeto.pos, Vector(50, 20))
        a.step(4); self.assertEqual(sujeto.pos, Vector(50, 10))
        a.step(5); self.assertEqual(sujeto.pos, Vector(50, 0))
        a.end(5)

    def test_move_five_steps(self):
        sujeto = Actor('A')
        a = actions.Move(sujeto, 0, 5, Vector(50, 0))
        a.start(0)
        a.step(1); self.assertEqual(sujeto.pos, Vector(10, 0))
        a.step(2); self.assertEqual(sujeto.pos, Vector(20, 0))
        a.step(3); self.assertEqual(sujeto.pos, Vector(30, 0))
        a.step(4); self.assertEqual(sujeto.pos, Vector(40, 0))
        a.step(5); self.assertEqual(sujeto.pos, Vector(50, 0))
        a.end(5)

    def test_move_ten_steps(self):
        sujeto = Actor('A')
        a = actions.Move(sujeto, 0, 10, Vector(100, 10))
        a.start(0)
        a.step(1); self.assertEqual(sujeto.pos, Vector(10, 1))
        a.step(2); self.assertEqual(sujeto.pos, Vector(20, 2))
        a.step(3); self.assertEqual(sujeto.pos, Vector(30, 3))
        a.step(4); self.assertEqual(sujeto.pos, Vector(40, 4))
        a.step(5); self.assertEqual(sujeto.pos, Vector(50, 5))
        a.step(6); self.assertEqual(sujeto.pos, Vector(60, 6))
        a.step(7); self.assertEqual(sujeto.pos, Vector(70, 7))
        a.step(8); self.assertEqual(sujeto.pos, Vector(80, 8))
        a.step(9); self.assertEqual(sujeto.pos, Vector(90, 9))
        a.step(10); self.assertEqual(sujeto.pos, Vector(100, 10))
        a.end(10)


class TestFall(unittest.TestCase):

    def test(self):
        sujeto = Actor('A')
        a = actions.Fall(sujeto, 0, 5, Vector(100, 0))
        a.start(0)
        a.step(1); self.assertEqual(sujeto.pos, Vector(4, 0))
        a.step(2); self.assertEqual(sujeto.pos, Vector(16, 0))
        a.step(3); self.assertEqual(sujeto.pos, Vector(36, 0))
        a.step(4); self.assertEqual(sujeto.pos, Vector(64, 0))
        a.step(5); self.assertEqual(sujeto.pos, Vector(100, 0))
        a.end(5)

    def test_fall_not_in_origin(self):
        sujeto = Actor('A', pos=(100,0))
        a = actions.Fall(sujeto, 0, 5, Vector(200, 0))
        a.start(0)
        a.step(1); self.assertEqual(sujeto.pos, Vector(104, 0))
        a.step(2); self.assertEqual(sujeto.pos, Vector(116, 0))
        a.step(3); self.assertEqual(sujeto.pos, Vector(136, 0))
        a.step(4); self.assertEqual(sujeto.pos, Vector(164, 0))
        a.step(5); self.assertEqual(sujeto.pos, Vector(200, 0))
        a.end(5)

class TestEasing(unittest.TestCase):

    def test(self):
        from actors import Label

        move = Label('Move', width=190, pos=(100,30), color='gold')
        fall = Label('Fall', width=190, pos=(300,30), color='gold')
        land = Label('Land', width=190, pos=(500,30), color='gold')
        ease_in = Label('EaseIn', width=190, pos=(700,30), color='gold')
        ease_out = Label('EaseOut', width=190, pos=(900,30), color='gold')
        swing = Label('Swing', width=190, pos=(1100,30), color='gold')
        sch = Scheduler()
        sch.add_action(actions.Move(move, 5, 70, (100, 700)))
        sch.add_action(actions.Fall(fall, 5, 70, (300, 700)))
        sch.add_action(actions.Land(land, 5, 70, (500, 700)))
        sch.add_action(actions.EaseIn(ease_in, 5, 70, (700, 700)))
        sch.add_action(actions.EaseOut(ease_out, 5, 70, (900, 700)))
        sch.add_action(actions.Swing(swing, 5, 70, (1100, 700)))
        engine = PyGameEngine()
        stage = Stage(engine)
        stage.add_actors(move, fall, land, ease_in, ease_out, swing)
        for frame in range(75):
            stage.draw(frame)
            sch.next()

class TestLevel(unittest.TestCase):

    def test(self):
        t = Text('timer', pos=(1000, 700), color='navy')
        e1 = Label('e1', text='Enter on 75', width=190, color='gold')
        bg = Rect('bg', width=30, height=600, pos=(620, 320), color='orange')
        fg = Rect('fg', width=30, height=600, pos=(660, 320), color='navy')
        e = Label('exit', text="I'll go on 2s", pos=(200, 200))

        sch = Scheduler()
        sch.add_action(actions.Timer(t, 0, 150))
        sch.add_action(actions.Enter(e1, 75, 76, (640, 320)))
        sch.add_action(actions.Background(bg, 100, 101))
        sch.add_action(actions.Foreground(fg, 125, 126))
        sch.add_action(actions.Exit(e, 50, 51))
        engine = PyGameEngine()
        studio = Stage(engine)
        studio.add_actors(t, fg, e, e1, bg)
        for frame in range(150):
            studio.draw(frame)
            sch.next()

class TestFadeOut(unittest.TestCase):

    def test_fide_out(self):
        bob = Square('bob')
        hide = actions.FadeOut(bob, 0, 10)
        sch = Scheduler()
        sch.add_action(hide)
        self.assertEqual(bob.alpha, 1.0)
        sch.next()  # Frame 0 -> 1, no action
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.9)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.8)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.7)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.6)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.5)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.4)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.3)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.2)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.1)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.0)
        self.assertEqual(sch.frame, 11)

    def test_fade_out_in_pygame(self):
        sch = Scheduler()
        engine = PyGameEngine()
        studio = Stage(engine)
        for row in range(50, 780, 100):
            for col in range(50, 1280, 100):
                from_frame = random.randint(5, 30)
                size = random.randint(10, 70)
                to_frame = from_frame + size
                name = 'bob{}x{}'.format(col, row)
                actor = Square(name,
                    color=colors.random_color(),
                    pos=(col, row),
                    side=90,
                    )
                sch.add_action(actions.FadeOut(actor, from_frame, to_frame))
                studio.add_actor(actor)

        for frame in range(75):
            studio.draw(frame)
            sch.next()


class TestFadeIn(unittest.TestCase):

    def test_show_calls(self):
        bob = Square('bob', alpha=0.0)
        show = actions.FadeIn(bob, 0, 10)
        sch = Scheduler()
        sch.add_action(show)
        self.assertEqual(bob.alpha, 0.0)
        sch.next()  # Frame 0 -> 1, no action
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.1)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.2)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.3)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.4)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.5)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.6)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.7)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.8)
        sch.next(); self.assertAlmostEqual(bob.alpha, 0.9)
        sch.next(); self.assertAlmostEqual(bob.alpha, 1.0)

    def test_fade_in_in_pygame(self):
        sch = Scheduler()
        engine = PyGameEngine()
        studio = Stage(engine)
        for row in range(50, 780, 100):
            for col in range(50, 1280, 100):
                from_frame = random.randint(5, 30)
                size = random.randint(10, 70)
                to_frame = from_frame + size
                name = 'bob{}x{}'.format(col, row)
                actor = Square(name,
                    color=colors.random_color(),
                    pos=(col, row),
                    side=90,
                    alpha=0.1,
                    )
                sch.add_action(actions.FadeIn(actor, from_frame, to_frame))
                studio.add_actor(actor)
        for frame in range(75):
            studio.draw(frame)
            sch.next()

if __name__ == '__main__':
    unittest.main()

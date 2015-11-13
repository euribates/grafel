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

class TestIntervalo(unittest.TestCase):

    def test_creacion_de_intervalos_con_dos_valores(self):
        interval = actions.Interval(5, 7)
        self.assertNotIn(4, interval)
        self.assertIn(5, interval)
        self.assertIn(6, interval)
        self.assertIn(7, interval)
        self.assertNotIn(8, interval)

    def test_creacion_de_intervalos_con_un_valor(self):
        interval = actions.Interval(3)
        self.assertNotIn(2, interval)
        self.assertIn(3, interval)
        self.assertIn(4, interval)
        self.assertNotIn(5, interval)

    def test_calcular_lengitud(self):
        i1 = actions.Interval(5, 7)
        self.assertEqual(len(i1), 3)
        i2 = actions.Interval(9)
        self.assertEqual(len(i2), 2)

    def test_as_iterator(self):
        self.assertEqual(
            list(actions.Interval(7, 12)),
            [7, 8, 9, 10, 11, 12]
            )

    def test_last_method(self):
        i = actions.Interval(7, 12)
        self.assertRaises(ValueError, i.is_last, 6)
        self.assertEqual(i.is_last(7), False)
        self.assertEqual(i.is_last(8), False)
        self.assertEqual(i.is_last(9), False)
        self.assertEqual(i.is_last(10), False)
        self.assertEqual(i.is_last(11), False)
        self.assertEqual(i.is_last(12), True)

class TestActions(unittest.TestCase):

    def test_uso(self):
        sch = Scheduler()
        bob = Square('Bob')
        task = actions.Action(bob, 5, 10)
        sch.add_action(task)
        self.assertTrue((bob.name, 5) in sch.actions)


    def test_calls(self):
        sch = Scheduler()

        class TestAction(actions.Action):
            def start(self, frame):
                self.started_at_frame = frame
                self.called_on_frames = []

            def __call__(self, frame):
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
        sch.add_action(actions.MoveTo(bob, 5, 10, Vector(72, 54)))
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

class TestMoveTo(unittest.TestCase):

    def test_move_to_not_in_origin(self):
        sujeto = Actor('A', pos=Vector(50, 50))
        a = actions.MoveTo(sujeto, 0, 5, Vector(50, 0))
        a.start(0)
        self.assertEqual(a(1), {'pos': Vector(0, -10)})
        self.assertEqual(a(2), {'pos': Vector(0, -10)})
        self.assertEqual(a(3), {'pos': Vector(0, -10)})
        self.assertEqual(a(4), {'pos': Vector(0, -10)})
        self.assertEqual(a(5), {'pos': Vector(0, -10)})
        a.end(5)

    def test_move_to_five_steps(self):
        a = actions.MoveTo(Actor('A'), 0, 5, Vector(50, 0))
        a.start(0)
        self.assertEqual(a(1), {'pos': Vector(10, 0)})
        self.assertEqual(a(2), {'pos': Vector(10, 0)})
        self.assertEqual(a(3), {'pos': Vector(10, 0)})
        self.assertEqual(a(4), {'pos': Vector(10, 0)})
        self.assertEqual(a(5), {'pos': Vector(10, 0)})
        a.end(5)

    def test_move_to_ten_steps(self):
        a = actions.MoveTo(Actor('A'), 0, 10, Vector(100, 0))
        a.start(0)
        self.assertEqual(a(1), {'pos': Vector(10, 0)})
        self.assertEqual(a(2), {'pos': Vector(10, 0)})
        self.assertEqual(a(3), {'pos': Vector(10, 0)})
        self.assertEqual(a(4), {'pos': Vector(10, 0)})
        self.assertEqual(a(5), {'pos': Vector(10, 0)})
        self.assertEqual(a(6), {'pos': Vector(10, 0)})
        self.assertEqual(a(7), {'pos': Vector(10, 0)})
        self.assertEqual(a(8), {'pos': Vector(10, 0)})
        self.assertEqual(a(9), {'pos': Vector(10, 0)})
        self.assertEqual(a(10), {'pos': Vector(10, 0)})
        a.end(10)


class TestFall(unittest.TestCase):

    def test(self):
        a = actions.Fall(Actor('A'), 0, 5, Vector(100, 0))
        a.start(0)
        self.assertEqual(a(1), {'pos': Vector(4, 0)})
        self.assertEqual(a(2), {'pos': Vector(12, 0)})
        self.assertEqual(a(3), {'pos': Vector(20, 0)})
        self.assertEqual(a(4), {'pos': Vector(28, 0)})
        self.assertEqual(a(5), {'pos': Vector(36, 0)})
        a.end(5)

    def test_fall_not_in_origin(self):
        import actors
        actors.logger.setLevel(logging.DEBUG)
        actor = Actor('A', pos=(100,0))
        a = actions.Fall(actor, 0, 5, Vector(200, 0))
        a.start(0)
        self.assertEqual(a(1), {'pos': Vector(4, 0)})
        self.assertEqual(a(2), {'pos': Vector(12, 0)})
        self.assertEqual(a(3), {'pos': Vector(20, 0)})
        self.assertEqual(a(4), {'pos': Vector(28, 0)})
        self.assertEqual(a(5), {'pos': Vector(36, 0)})
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
        sch.add_action(actions.MoveTo(move, 0, 100, (100, 700)))
        sch.add_action(actions.Fall(fall, 0, 100, (300, 700)))
        sch.add_action(actions.Land(land, 0, 100, (500, 700)))
        sch.add_action(actions.EaseIn(ease_in, 0, 100, (700, 700)))
        sch.add_action(actions.EaseOut(ease_out, 0, 100, (900, 700)))
        sch.add_action(actions.Swing(swing, 0, 100, (1100, 700)))
        engine = PyGameEngine()
        stage = Stage(engine)
        stage.add_actors(move, fall, land, ease_in, ease_out, swing)
        for frame in range(150):
            stage.draw(frame)
            sch.next()

class TestLevel(unittest.TestCase):

    def test(self):
        logger.error('Empezamos')
        t = Text('timer', pos=(1000, 700), color='navy')
        e1 = Label('e1', text='Enter on 75', width=190, color='gold')
        bg = Rect('bg', width=30, height=600, pos=(620, 320), color='orange')
        fg = Rect('fg', width=30, height=600, pos=(660, 320), color='navy')
        e = Label('exit', text="I'll go on 2s", pos=(200, 200))

        logger.error('e1.level: {}'.format(e1.level))
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
                from_frame = random.randint(0, 30)
                size = random.randint(10, 120)
                to_frame = from_frame + size
                name = 'bob{}x{}'.format(col, row)
                actor = Square(name,
                    color=colors.random_color(),
                    pos=(col, row),
                    side=90,
                    )
                sch.add_action(actions.FadeOut(actor, from_frame, to_frame))
                studio.add_actor(actor)

        for frame in range(150):
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
                from_frame = random.randint(0, 30)
                size = random.randint(10, 120)
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
        for frame in range(150):
            studio.draw(frame)
            sch.next()

if __name__ == '__main__':
    unittest.main()

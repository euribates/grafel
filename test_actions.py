#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_actions.py

import sys
import math
import logging
import unittest

import logs
from vectors import Vector
from actors import Actor, Square, State
from actions import Action, MoveTo, Blink, Fall, Interval
from control import Scheduler

logger = logs.create(__name__)

class TestIntervalo(unittest.TestCase):

    def test_creacion_de_intervalos_con_dos_valores(self):
        interval = Interval(5, 7)
        self.assertNotIn(4, interval)
        self.assertIn(5, interval)
        self.assertIn(6, interval)
        self.assertIn(7, interval)
        self.assertNotIn(8, interval)

    def test_creacion_de_intervalos_con_un_valor(self):
        interval = Interval(3)
        self.assertNotIn(2, interval)
        self.assertIn(3, interval)
        self.assertIn(4, interval)
        self.assertNotIn(5, interval)

    def test_calcular_lengitud(self):
        i1 = Interval(5, 7)
        self.assertEqual(len(i1), 3)
        i2 = Interval(9)
        self.assertEqual(len(i2), 2)

    def test_as_iterator(self):
        self.assertEqual(
            list(Interval(7, 12)),
            [7, 8, 9, 10, 11, 12]
            )

    def test_last_method(self):
        i = Interval(7, 12)
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
        task = Action(bob, 5, 10)
        sch.add_action(task)
        self.assertTrue((bob.name, 5) in sch.actions)


    def test_calls(self):
        sch = Scheduler()

        class TestAction(Action):
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
        sch.add_action(MoveTo(bob, 5, 10, Vector(72, 54)))
        sch.add_action(Blink(bob, 8, 12))

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
        a = MoveTo(sujeto, 0, 5, Vector(50, 0))
        a.start(0)
        self.assertEqual(a(1), {'pos': Vector(0, -10)})
        self.assertEqual(a(2), {'pos': Vector(0, -10)})
        self.assertEqual(a(3), {'pos': Vector(0, -10)})
        self.assertEqual(a(4), {'pos': Vector(0, -10)})
        self.assertEqual(a(5), {'pos': Vector(0, -10)})
        a.end(5)

    def test_move_to_five_steps(self):
        a = MoveTo(Actor('A'), 0, 5, Vector(50, 0))
        a.start(0)
        self.assertEqual(a(1), {'pos': Vector(10, 0)})
        self.assertEqual(a(2), {'pos': Vector(10, 0)})
        self.assertEqual(a(3), {'pos': Vector(10, 0)})
        self.assertEqual(a(4), {'pos': Vector(10, 0)})
        self.assertEqual(a(5), {'pos': Vector(10, 0)})
        a.end(5)

    def test_move_to_ten_steps(self):
        a = MoveTo(Actor('A'), 0, 10, Vector(100, 0))
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
        a = Fall(Actor('A'), 0, 5, Vector(100, 0))
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
        a = Fall(actor, 0, 5, Vector(200, 0))
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
        from actions import MoveTo, Fall, Land, EaseIn, EaseOut, Swing
        from control import Scheduler
        from engines import PyGameEngine

        move = Label('Move', width=190, pos=(100,30), color='gold')
        fall = Label('Fall', width=190, pos=(300,30), color='gold')
        land = Label('Land', width=190, pos=(500,30), color='gold')
        ease_in = Label('EaseIn', width=190, pos=(700,30), color='gold')
        ease_out = Label('EaseOut', width=190, pos=(900,30), color='gold')
        swing = Label('Swing', width=190, pos=(1100,30), color='gold')
        sch = Scheduler()
        sch.add_action(MoveTo(move, 0, 100, (100, 700)))
        sch.add_action(Fall(fall, 0, 100, (300, 700)))
        sch.add_action(Land(land, 0, 100, (500, 700)))
        sch.add_action(EaseIn(ease_in, 0, 100, (700, 700)))
        sch.add_action(EaseOut(ease_out, 0, 100, (900, 700)))
        sch.add_action(Swing(swing, 0, 100, (1100, 700)))
        engine = PyGameEngine()
        for frame in range(150):
            engine.clear(frame)
            for a in (move, fall, land, ease_in, ease_out, swing):
                a.start_draw(engine)
            engine.end()
            sch.next()

class TestLevel(unittest.TestCase):

    def test(self):
        from studio import Stage
        from actors import Label, Text, Rect
        from actions import Enter, Exit, Background, Foreground, Timer
        from control import Scheduler
        from engines import PyGameEngine

        logger.error('Empezamos')
        t = Text('timer', pos=(1000, 700), color='navy')
        e1 = Label('e1', text='Enter on 75', width=190, color='gold')
        bg = Rect('bg', width=30, height=600, pos=(620, 320), color='orange')
        fg = Rect('fg', width=30, height=600, pos=(660, 320), color='navy')
        e = Label('exit', text="I'll go on 2s", pos=(200, 200))

        logger.error('e1.level: {}'.format(e1.level))
        sch = Scheduler()
        sch.add_action(Timer(t, 0, 150))
        sch.add_action(Enter(e1, 75, 76, (640, 320)))
        sch.add_action(Background(bg, 100, 101))
        sch.add_action(Foreground(fg, 125, 126))
        sch.add_action(Exit(e, 50, 51))
        
        engine = PyGameEngine()
        studio = Stage(engine)
        studio.add_actors(t, fg, e, e1, bg)
        for frame in range(150):
            engine.clear(frame)
            studio.draw(frame)
            engine.end()
            sch.next()

        


if __name__ == '__main__':
    unittest.main()

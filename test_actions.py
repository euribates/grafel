#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_actions.py

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import sys
import math
import logging
import unittest

from vectors import Vector
from actors import Actor, Square, State
from actions import Action, MoveTo, Blink, Fall, Interval

logger = logging.getLogger('test_actions')
logger.setLevel(logging.WARNING) 

class TestIntervalo(unittest.TestCase):

    def test_creacion_de_intervalos_con_dos_valores(self):
        interval = Interval(5, 7)
        self.assertNotIn(4, interval)
        self.assertIn(5, interval)
        self.assertIn(6, interval)
        self.assertIn(7, interval)
        self.assertIn(7, interval)
        self.assertNotIn(8, interval)

    def test_creacion_de_intervalos_con_un_valor(self):
        interval = Interval(3)
        self.assertNotIn(2, interval)
        self.assertIn(3, interval)
        self.assertNotIn(4, interval)

    def test_calcular_lengitud(self):
        i1 = Interval(5, 7)
        self.assertEqual(len(i1), 3)
        i2 = Interval(9)
        self.assertEqual(len(i2), 1)

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
        bob = Square('Bob')
        action_move_left_down = Action(bob, 5, 10)
        self.assertNotIn(4, bob.actions)
        self.assertEqual(len(bob.actions[5]), 1)
        self.assertNotIn(6, bob.actions)

    def test_calls(self):

        class TestAction(Action):
            def start(self, frame):
                self.started_at_frame = frame
                self.called_on_frames = []

            def __call__(self, frame):
                self.called_on_frames.append(frame)

            def end(self, frame):
                self.ended_at_frame = frame

        a = Actor('A')
        t = TestAction(a, 3, 6)
        for f in range(15):
            a.next()
        self.assertEqual(t.started_at_frame, 3)
        self.assertEqual(t.ended_at_frame, 6)
        self.assertEqual(t.called_on_frames, [3, 4, 5, 6])





    def test_start(self):
        bob = Actor('Bob')
        a5_10 = MoveTo(bob, 5, 10, Vector(72, 54))
        a8_12 = Blink(bob, 8, 12)

        self.assertEqual(len(bob.active_actions), 0)  # 0
        bob.next(); self.assertEqual(len(bob.active_actions), 0)  # 1
        bob.next(); self.assertEqual(len(bob.active_actions), 0)  # 2
        bob.next(); self.assertEqual(len(bob.active_actions), 0)  # 3
        bob.next(); self.assertEqual(len(bob.active_actions), 0)  # 4
        bob.next(); self.assertEqual(len(bob.active_actions), 0) # 5
        bob.next(); self.assertEqual(len(bob.active_actions), 1)  # 6
        bob.next(); self.assertEqual(len(bob.active_actions), 1)  # 7
        bob.next(); self.assertEqual(len(bob.active_actions), 1)  # 8
        bob.next(); self.assertEqual(len(bob.active_actions), 2)  # 9
        bob.next(); self.assertEqual(len(bob.active_actions), 2)  # 10
        bob.next(); self.assertEqual(len(bob.active_actions), 1)  # 11
        bob.next(); self.assertEqual(len(bob.active_actions), 1)  # 12
        bob.next(); self.assertEqual(len(bob.active_actions), 0)  # 13
        bob.next(); self.assertEqual(len(bob.active_actions), 0)  # 14
        bob.next(); self.assertEqual(len(bob.active_actions), 0)  # 15

class TestMoveTo(unittest.TestCase):

    def test_move_to_not_in_origin(self):
        sujeto = Actor('A', pos=Vector(50, 50))
        a = MoveTo(sujeto, 0, 5, Vector(50, 0))
        a.start(0)
        self.assertEqual(a(0), {})
        self.assertEqual(a(1), {'pos': Vector(0, -10)})
        self.assertEqual(a(2), {'pos': Vector(0, -10)})
        self.assertEqual(a(3), {'pos': Vector(0, -10)})
        self.assertEqual(a(4), {'pos': Vector(0, -10)})
        self.assertEqual(a(5), {'pos': Vector(0, -10)})
        a.end(5)

    def test_move_to_five_steps(self):
        a = MoveTo(Actor('A'), 0, 5, Vector(50, 0))
        a.start(0)
        self.assertEqual(a(0), {})
        self.assertEqual(a(1), {'pos': Vector(10, 0)})
        self.assertEqual(a(2), {'pos': Vector(10, 0)})
        self.assertEqual(a(3), {'pos': Vector(10, 0)})
        self.assertEqual(a(4), {'pos': Vector(10, 0)})
        self.assertEqual(a(5), {'pos': Vector(10, 0)})
        a.end(5)

    def test_move_to_ten_steps(self):
        a = MoveTo(Actor('A'), 0, 10, Vector(100, 0))
        a.start(0)
        self.assertEqual(a(0), {})
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
        self.assertEqual(a(0), {'pos': Vector(0, 0)})
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
        self.assertEqual(a(0), {'pos': Vector(0, 0)})
        self.assertEqual(a(1), {'pos': Vector(4, 0)})
        self.assertEqual(a(2), {'pos': Vector(12, 0)})
        self.assertEqual(a(3), {'pos': Vector(20, 0)})
        self.assertEqual(a(4), {'pos': Vector(28, 0)})
        self.assertEqual(a(5), {'pos': Vector(36, 0)})
        a.end(5)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import unittest

import control

from actors import Square
from actions import Fall, Move
import logs

logger = logs.create('__name__')


class TestBob(unittest.TestCase):

    def test(self):
        bob = Square('Bob')
        sch = control.Scheduler()
        sch.add_action(Move(bob, 1, 14, (100, 0)))
        self.assertAlmostEqual(bob.pos.x, 0.000, 3)
        sch.next()  # Frame 1
        self.assertAlmostEqual(bob.pos.x, 0.000)
        sch.next()  # Frame 2
        self.assertAlmostEqual(bob.pos.x, 7.692, 3)
        sch.next()  # Frame 3
        self.assertAlmostEqual(bob.pos.x, 15.385, 3)
        sch.next()  # Frame 4
        self.assertAlmostEqual(bob.pos.x, 23.077, 3)
        sch.next()  # Frame 5
        self.assertAlmostEqual(bob.pos.x, 30.769, 3)
        sch.next()  # Frame 6
        self.assertAlmostEqual(bob.pos.x, 38.462, 3)
        sch.next()  # Frame 7
        self.assertAlmostEqual(bob.pos.x, 46.154, 3)
        sch.next()  # Frame 8
        self.assertAlmostEqual(bob.pos.x, 53.846, 3)
        sch.next()  # Frame 9
        self.assertAlmostEqual(bob.pos.x, 61.538, 3)
        sch.next()  # Frame 10
        self.assertAlmostEqual(bob.pos.x, 69.231, 3)
        sch.next()  # Frame 11
        self.assertAlmostEqual(bob.pos.x, 76.923, 3)
        sch.next()  # Frame 12
        self.assertAlmostEqual(bob.pos.x, 84.615, 3)
        sch.next()  # Frame 13
        self.assertAlmostEqual(bob.pos.x, 92.308, 3)
        sch.next()  # Frame 14
        self.assertAlmostEqual(bob.pos.x, 100.0, 3)
        sch.next()  # Frame 15
        self.assertAlmostEqual(bob.pos.x, 100.0, 3)
        sch.next()  # Frame 16
        self.assertAlmostEqual(bob.pos.x, 100.0, 3)


class TestScheduler(unittest.TestCase):

    def test_two_actions(self):

        scheduler = control.Scheduler()
        self.assertEqual(len(scheduler.actors), 0)
        
        charles = Square('Charles', pos=(100, 0), color='brown4', side=75)
        scheduler.add_action(Fall(charles, 0, 5, (100, 300)))

        self.assertEqual(len(scheduler.actors), 1)

        dorothy = Square('Dorothy', pos=(0, 0), color='#32BF98', side=25)
        scheduler.add_action(Move(dorothy, 0, 5, (100, 100)))
        self.assertEqual(len(scheduler.actors), 2)
        
        # Frame 0
        self.assertEqual(charles.pos, (100, 0))
        self.assertEqual(dorothy.pos, (0, 0))

        self.assertEqual(scheduler.next(), 1) # Frame 1
        self.assertEqual(charles.pos, (100, 12))
        self.assertEqual(dorothy.pos, (20, 20))

        self.assertEqual(scheduler.next(), 2) # Frame 2
        self.assertEqual(charles.pos, (100, 48))
        self.assertEqual(dorothy.pos, (40, 40))

        self.assertEqual(scheduler.next(), 3) # Frame 3
        self.assertEqual(charles.pos, (100, 108))
        self.assertEqual(dorothy.pos, (60, 60))

        self.assertEqual(scheduler.next(), 4) # Frame 4
        self.assertEqual(charles.pos, (100, 192))
        self.assertEqual(dorothy.pos, (80, 80))
        
        self.assertEqual(scheduler.next(), 5) # Frame 5
        self.assertEqual(charles.pos, (100, 300))
        self.assertEqual(dorothy.pos, (100, 100))

        self.assertEqual(scheduler.next(), 6) # Frame 6
        self.assertEqual(charles.pos, (100, 300))
        self.assertEqual(dorothy.pos, (100, 100))

if __name__ == '__main__':
    unittest.main()

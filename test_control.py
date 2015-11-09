#!/usr/bin/python3
# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import sys
import unittest

import control

from actors import Square
from actions import Fall, MoveTo
import logs

logger = logs.create('__name__')


class TestBob(unittest.TestCase):

    def test(self):
        bob = Square('Bob')
        sch = control.Scheduler()
        sch.add_action(MoveTo(bob, 0, 2, (100, 0)))
        for i in range(15):
            print('{:5} {}'.format(sch.frame, repr(bob)), file=sys.stderr)
            sch.next()

class TestScheduler(unittest.TestCase):

    def test(self):

        scheduler = control.Scheduler()
        self.assertEqual(len(scheduler.actors), 0)
        
        charles = Square('Charles', pos=(100, 0), color='brown4', side=75)
        scheduler.add_action(Fall(charles, 0, 5, (100, 300)))

        self.assertEqual(len(scheduler.actors), 1)

        dorothy = Square('Dorothy', pos=(0, 0), color='#32BF98', side=25)
        scheduler.add_action(MoveTo(dorothy, 0, 5, (100, 100)))
        self.assertEqual(len(scheduler.actors), 2)
        
        # Frame 0
        self.assertEqual(charles.pos, (100, 0))
        self.assertEqual(dorothy.pos, (0, 0))

        self.assertEqual(scheduler.next(), 1) # Frame 1
        
        self.assertEqual(charles.pos, (100, 0))
        self.assertEqual(dorothy.pos, (0, 0))

        self.assertEqual(scheduler.next(), 2) # Frame 2
        self.assertEqual(dorothy.pos, (20, 20))

        self.assertEqual(scheduler.next(), 3) # Frame 3
        self.assertEqual(dorothy.pos, (40, 40))

        #self.assertEqual(int(round(dorothy.pos.x)), 392)
        #self.assertEqual(int(round(dorothy.pos.y)), 12)

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import engines
import actors
import vectors
import colors

class TestBaseEngine(unittest.TestCase):
    def test_create_without_params(self):
        engine = engines.BaseEngine()
        self.assertEqual(engine.width, 1280)
        self.assertEqual(engine.height, 720)
        self.assertEqual(engine.size, vectors.Vector(1280, 720))
        self.assertEqual(engine.fps, 25)
        self.assertEqual(engine.bg_color, colors.black)



class TestSVGEngine(unittest.TestCase):

    SIZE = (500, 500)

    def test(self):
        sq = actors.Rect('sq', size=vectors.Vector(50, 150))
        self.assertEqual(sq.width, 50)
        self.assertEqual(sq.height, 150)
        sq.place(250, 200)
        self.assertEqual(sq.pos.x, 250)
        self.assertEqual(sq.pos.y, 200)
        
        bob = actors.Square('bob', side=72)
        bob.place(250, 100)

        engine = engines.SVGEngine(output_dir='./tmp')
        engine.clear(0)
        engine.draw_actor(sq)
        engine.draw_actor(bob)
        engine.end()
        

if __name__ == '__main__':
    unittest.main()

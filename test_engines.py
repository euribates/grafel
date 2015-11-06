#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import tempfile
import unittest
import engines
import actors
import vectors
import colors
import random

class TestCreation(unittest.TestCase):
    
    def test_create_base_engine_without_params(self):
        engine = engines.BaseEngine()
        self.assertEqual(engine.width, 1280)
        self.assertEqual(engine.height, 720)
        self.assertEqual(engine.size, vectors.Vector(1280, 720))
        self.assertEqual(engine.fps, 25)
        self.assertEqual(engine.bg_color, colors.black)

    
    def test_create_svg_engine(self):
        d = tempfile.mkdtemp(dir='.', prefix='tmp_test')
        engine = engines.SVGEngine(output_dir=d)
        engine.clear(0)
        engine.end()
        assert os.path.exists(os.path.join(d, 'frame_00000.svg'))
        for fn in os.listdir(d):
            os.unlink(os.path.join(d, fn))
        os.rmdir(d)

    def test_create_pygame_engine(self):
        engine = engines.PyGameEngine()
        engine.clear(0)
        for i in range(120):
            x = random.randint(0, engine.width)
            y = random.randint(0, engine.width)
            w = random.randint(0, engine.width // 4)
            h = random.randint(0, engine.width // 4)
            color = colors.Color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                )
            alpha = random.random()
            engine.rect(x, y, w, h, color=color, alpha=alpha)
        engine.end()
        time.sleep(1.5)




def draw_rects(engine):
    engine.rect(10, 10, 40, 40)
    engine.rect(60, 10, 40, 40, color='navy')
    engine.rect(110, 10, 40, 40, color='red')
    engine.rect(160, 10, 40, 40, color='red', alpha=0.5)
    engine.rect(210, 10, 40, 40, color='red', alpha=0.25)
    engine.rect(260, 10, 40, 40, color='yellow')

def draw_circles(engine):
    engine.circle(30, 80, 20)
    engine.circle(80, 80, 20, color='navy')
    engine.circle(130, 80, 20, color='red')
    engine.circle(180, 80, 20, color='red', alpha=0.5)
    engine.circle(230, 80, 20, color='red', alpha=0.25)
    engine.circle(280, 80, 20, color='yellow')

def draw_polygons(engine):
    engine.polygon(10, 110, [(40, 25), (-40, 25)])
    engine.polygon(60, 110, [(40, 25), (-40, 25)], color='navy')
    engine.polygon(110, 110, [(40, 25), (-40, 25)], color='red')
    engine.polygon(160, 110, [(40, 25), (-40, 25)], color='red', alpha=0.5)
    engine.polygon(210, 110, [(40, 25), (-40, 25)], color='red', alpha=0.25)
    engine.polygon(260, 110, [(40, 25), (-40, 25)], color='yellow')


class TestPyGameEngine(unittest.TestCase):

     def test_draw_methods(self):
        engine = engines.PyGameEngine()
        engine.clear(0)

        draw_rects(engine)
        draw_circles(engine)
        draw_polygons(engine)

        engine.end()
        time.sleep(1.5)



class TestSVGEngine(unittest.TestCase):

    
    def test_draw_methods(self):
        engine = engines.SVGEngine(output_dir='./tmp')
        engine.clear(0)

        draw_rects(engine)
        draw_circles(engine)
        draw_polygons(engine)

        engine.end()
       

class TestGrid(unittest.TestCase):
    
    def test_show_grid(self):
        import actors

        engine = engines.PyGameEngine()
        engine.clear(0)
        engine.grid()
        engine.end()
        time.sleep(1)


class TestWithActors(unittest.TestCase):

    def test_pygame(self):
        import actors

        engine = engines.PyGameEngine()
        engine.clear(0)
        engine.grid()
        bob = actors.Square('Bob', alpha=0.5)
        c1 = actors.Circle('C1', color='red', radius=5)
        c1.pos =(10, 10)

        c2 = actors.Circle('C2', color='red', radius=5)
        c2.pos =(50, 50)
        bob.add_son(c2)
        #bob.place(100, 100)
        bob.start_draw(engine)

        a = actors.Square('A', pos=(350, 70), color='green')
        b = actors.Square('B', pos=(10, 10), color='palegreen')
        a.add_son(b)
        c = actors.Square('C', pos=(11, 22), color='yellow')
        b.add_son(c)
        a.start_draw(engine)

        self.assertEqual(c.parent, b)
        self.assertEqual(c.parent.parent, a)



        star = actors.Star('Star', pos=(200, 200), alpha=0.33, color='yellow')
        star.start_draw(engine)
        for i in range(40, 101, 10):
            star.state.delta(pos=vectors.Vector(25, 0),
                alpha=i/100, 
                scale=vectors.Vector(1.1, 1.1))
            star.start_draw(engine)


        engine.end()
        time.sleep(1.5)



if __name__ == '__main__':
    unittest.main()

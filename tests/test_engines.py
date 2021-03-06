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

class TestBaseEngine(unittest.TestCase):

    def test_calls(self):
        eng = engines.BaseEngine()
        eng.clear(0)
        eng.polygon(0, 0, [(50, 0), (50, 50), (0, 50)], color=colors.white)
        eng.end()

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
        try:
            engine = engines.SVGEngine(output_dir=d)
            engine.clear(0)
            engine.end()
            assert os.path.exists(os.path.join(d, 'frame_00000.svg'))
            for fn in os.listdir(d):
                os.unlink(os.path.join(d, fn))
        finally:
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
            engine.roundrect(x, y, w, h, 15, color=color, alpha=alpha)
        engine.end()
        time.sleep(1)


def draw_rects(engine):
    engine.rect(10, 10, 40, 40)
    engine.rect(60, 10, 40, 40, color='navy')
    engine.rect(110, 10, 40, 40, color='red')
    engine.rect(160, 10, 40, 40, color='red', alpha=0.5)
    engine.rect(210, 10, 40, 40, color='red', alpha=0.25)
    engine.rect(260, 10, 40, 40, color='yellow')

    engine.roundrect(310, 10, 40, 40, 5)
    engine.roundrect(360, 10, 40, 40, 5, color='navy')
    engine.roundrect(410, 10, 40, 40, 5, color='red')
    engine.roundrect(460, 10, 40, 40, 5, color='red', alpha=0.5)
    engine.roundrect(510, 10, 40, 40, 5, color='red', alpha=0.25)
    engine.roundrect(560, 10, 40, 40, 5, color='yellow')

    engine.box(660, 10, 40, 40)
    engine.box(710, 10, 40, 40, color='navy')
    engine.box(760, 10, 40, 40, color='red')
    engine.box(810, 10, 40, 40, color='red', alpha=0.5)
    engine.box(860, 10, 40, 40, color='red', alpha=0.5)
    engine.box(910, 10, 40, 40, color='yellow')

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

def draw_actors(engine):
    s1 = actors.Star('star1', radius=25, pos=(35, 175))
    s1.start_draw(engine)
    s2 = actors.Star('star2', radius=25, pos=(90, 175), color='navy')
    s2.start_draw(engine)

    actors.Star('s3', radius=25,
            pos=(145, 175), 
            color='red',
            ).start_draw(engine)
    
    actors.Star('s4', radius=25,
            pos=(200, 175), 
            color='red',
            alpha=0.5
            ).start_draw(engine)

    actors.Star('s4', radius=25,
            pos=(255, 175), 
            color='red',
            alpha=0.25
            ).start_draw(engine)

    actors.Star('s5', radius=25,
            pos=(310, 175), 
            color='yellow',
            ).start_draw(engine)

    # RoundRect
    actors.RoundRect('rr1', pos=(35, 230)).start_draw(engine)
    actors.RoundRect('rr2', pos=(95, 230),
        color='navy',
        ).start_draw(engine)
    actors.RoundRect('rr3', pos=(155, 230),
        color='red',
        ).start_draw(engine)
    actors.RoundRect('rr4', pos=(215, 230),
        color='red',
        alpha=0.5,
        ).start_draw(engine)
    actors.RoundRect('rr5', pos=(275, 230),
        color='red',
        alpha=0.25,
        ).start_draw(engine)
    actors.RoundRect('rr6', pos=(335, 230),
        color='yellow',
        ).start_draw(engine)


    # Dices
    actors.Dice('d1', num=1, pos=(35, 290)).start_draw(engine)
    actors.Dice('d2', num=2,
        color='navy',
        pos=(95, 290),
        ).start_draw(engine)
    actors.Dice('d3', num=3,
        color='red',
        pos=(155, 290)
        ).start_draw(engine)
    actors.Dice('d4', num=4,
        color='red',
        alpha=0.5,
        pos=(215, 290)
        ).start_draw(engine)
    actors.Dice('d5', num=5,
        color='red',
        alpha=0.25,
        pos=(275, 290)
        ).start_draw(engine)
    actors.Dice('d6', num=6,
        color='yellow',
        pos=(335, 290)
        ).start_draw(engine)

def draw_texts(engine):
    l1 = actors.Label('l1', 'L1', color='#333333', pos=(40, 370))
    l1.start_draw(engine)
    l2 = actors.Label('l2', 'L2', color='yellow', pos=(110, 370))
    l2.start_draw(engine)
    l3 = actors.Label('l3', 'L3', color='red', pos=(180, 370))
    l3.start_draw(engine)
    l4 = actors.Label('l4', 'MiljgÁ', color='silver', pos=(290, 370))
    l4.start_draw(engine)

    actors.Label(
        'l5', 'L5', color='#333333',
        pos=(50, 470), fontsize=72
        ).start_draw(engine)
    actors.Label(
        'l6', 'L6', color='yellow',
        pos=(150, 470), fontsize=72
        ).start_draw(engine)
    actors.Label(
        'l7', 'L7', color='red',
        pos=(250, 470), fontsize=72
        ).start_draw(engine)
    actors.Label(
        'l8', 'MiljgÁ', color='silver',
        pos=(450, 470), fontsize=72
        ).start_draw(engine)

def draw_all(engine):
    draw_rects(engine)
    draw_circles(engine)
    draw_polygons(engine)
    draw_actors(engine)
    draw_texts(engine)

class TestPyGameEngine(unittest.TestCase):

     def test_draw_methods(self):
        engine = engines.PyGameEngine()
        engine.clear(0)
        engine.grid()
        draw_all(engine)
        engine.end()
        time.sleep(4)

class TestSVGEngine(unittest.TestCase):

    
    def test_draw_methods(self):
        engine = engines.SVGEngine(output_dir='./tmp')
        engine.clear(0)
        draw_all(engine)
        engine.end()
       

class TestGrid(unittest.TestCase):
    
    def test_show_grid(self):
        engine = engines.PyGameEngine()
        engine.clear(0)
        engine.grid()
        engine.end()
        time.sleep(1)


class TestWithActors(unittest.TestCase):

    def test_pygame(self):
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
            star.pos += vectors.Vector(25, 0)
            star.alpha = i/100 
            star.scale += vectors.Vector(1.1, 1.1)
            star.start_draw(engine)


        engine.end()
        time.sleep(1)

class TestBitmap(unittest.TestCase):
    def get_engine(self):
        from engines import PyGameEngine, SVGEngine
        #return SVGEngine(output_dir='./tmp')
        return  PyGameEngine()


    def test(self):
        engine = self.get_engine()
        engine.clear(0)
        engine.bitmap(300, 300, 'mf.png')
        engine.end()
        time.sleep(1)


class TestText(unittest.TestCase):
   
    def get_engine(self):
        from engines import PyGameEngine, SVGEngine
        # return SVGEngine(output_dir='./tmp')
        return  PyGameEngine()


    def test(self):
        engine = self.get_engine()
        engine.clear(0)
        #engine.grid()
        engine.line(200, 0, 200, 400)
        engine.line(0, 200, 400, 200)

        engine.text(400, 200, 'Hola, mundo')
        engine.line(395, 200, 405, 200, color='yellow')
        engine.line(400, 195, 400, 202, color='yellow')

        t = actors.Text('t', 'Hola, mundo', pos=(200, 200), color='red')
        t.start_draw(engine)

        l = actors.Label('l', 'Hola, mundo', pos=(600, 200), color='coral')
        l.start_draw(engine)

        engine.end()
        time.sleep(1)


if __name__ == '__main__':
    unittest.main()

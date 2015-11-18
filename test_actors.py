#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_actors.py

import math
import unittest
import random

from vectors import Vector
import actors
from actors import Level, Actor, Square, Star
import colors
import actions
from studio import Stage
import logs

logger = logs.create(__name__)

class TestLevel(unittest.TestCase):

    def test_creating_an_actor_without_pos_put_it_off_stage(self):
        a = Square('a', side=80)
        self.assertEqual(a.level, Level.OFF_STAGE)

    def test_creating_an_actor_with_pos_put_it_on_stage(self):
        a = Square('a', side=80, pos=(50, 100))
        self.assertEqual(a.level, Level.ON_STAGE)

class TestBox(unittest.TestCase):
    def test_box(self):
        stage = Stage()
        for col in range(50, 1280, 100):
            for row in range(50, 720, 100):
                b = actors.Box('b{}x{}'.format(col, row),
                    pos=Vector(col, row),
                    width=90,
                    height=90,
                    color=colors.random_color()
                    )
                stage.add_actor(b)
                stage.add_action(actions.Fall(b, 10, 35, Vector(640, 320)))
                stage.add_action(actions.Land(b, 35, 60, b.initial_state['pos']))

        for i in range(75):
            stage.draw(i)

class TestActorCenter(unittest.TestCase):

    def get_engine(self):
        from engines import PyGameEngine, SVGEngine
        #return SVGEngine(output_dir='./tmp')
        return  PyGameEngine()

    def test_all(self):
        import actors
        from vectors import zero
        import time

        engine = self.get_engine()
        engine.clear(0)
        engine.grid() 

        # Square
        sq = actors.Square('square', pos=(50, 50))
        sq.draw(engine)
        sq.spot_center(engine)

        # rect
        r = actors.Rect('rect', width=100, height=50)
        r.place(150, 50)
        r.draw(engine)
        r.spot_center(engine)

        # circle
        c = actors.Circle('circle', radius=25)
        c.place(240, 50)
        c.draw(engine)
        c.spot_center(engine)

        # polygon
        points = [Vector(a,b) for a,b in (
            (0, -20), (10, 0), (0, 20), (20, 0), (0, 10), (-20, 0),
            (0, 20), (-10, 0), (0, -20), (-20, 0), (0, -10)
            )]
        p = actors.Polygon('polygon', points=points)
        p.place(300, 50)
        p.draw(engine)
        p.spot_center(engine)

        # triangle
        t = actors.Triangle('triangle', points=[(0,-25), (50, 0), (0, 25)])
        t.place(350, 50)
        t.draw(engine)
        t.spot_center(engine)

        # star
        star = actors.Star('star', radius=25)
        star.place(420, 50)
        star.draw(engine)
        star.spot_center(engine)

        # roundrect
        round_rect = actors.RoundRect('round_rect',
                width=100, height=50, border_radius=10
                )
        round_rect.place(510, 50)
        round_rect.draw(engine)
        round_rect.spot_center(engine)

        # dices
        for num in range(1, 7):
            dice = actors.Dice('dice{}'.format(num),
                num=num
                )

            dice.place(50 + (num-1)*60, 110)
            dice.start_draw(engine)
            dice.spot_center(engine)

        # Text
        txt = actors.Text('Text', "Hola, mundo", color='yellow')
        txt.place(300, 170)
        txt.start_draw(engine)
        txt.spot_center(engine)
        
        # Label
        lbl = actors.Label('Label', "Hola, mundo", color='#666666')
        lbl.place(300, 220)
        lbl.start_draw(engine)
        lbl.spot_center(engine)

        mf = actors.Bitmap('mf', 'mf.png', pos=(300, 400))
        mf.draw(engine)
        mf.spot_center(engine)

        engine.end()
        time.sleep(1)

class TestActor(unittest.TestCase):

    def test_as_string(self):
        a = Actor('A')
        self.assertEqual(str(a), 'Actor A as Actor')
        a = Square('B')
        self.assertEqual(str(a), 'Actor B as Square')

    def test_creacion_actor(self):
        a = Actor('A')
        self.assertEqual(a.name, 'A')
        self.assertEqual(a.frame, 0)
        self.assertEqual(a.pos.x, 0)
        self.assertEqual(a.pos.y, 0)
        self.assertEqual(a.color.name, 'silver')
        self.assertEqual(a.color.red, 192)
        self.assertEqual(a.color.green, 192)
        self.assertEqual(a.color.blue, 192)

        self.assertEqual(a.scale.x, 1)
        self.assertEqual(a.scale.y, 1)
        self.assertEqual(a.alpha, 1.0)


    def test_move_actor(self):
        a = Actor('A')
        a.place(100, 200)
        self.assertEqual(a.pos.x, 100)
        self.assertEqual(a.pos.y, 200)
        a.pos += Vector(-2, 4)
        self.assertEqual(a.pos.x, 98)
        self.assertEqual(a.pos.y, 204)



class TestLabel(unittest.TestCase):

    def test_create_label(self):
        label = actors.Label('l1', 'L1')
        self.assertEqual(label.name, 'l1')
        self.assertEqual(label.text, 'L1')

class TestSquare(unittest.TestCase):

    def test_creacion_square_bob(self):
        bob = Square('bob', pos=(23, 74))
        self.assertEqual(bob.name, 'bob')
        self.assertEqual(bob.pos.x, 23)
        self.assertEqual(bob.pos.y, 74)
        self.assertEqual(bob.initial_state['pos'].x, 23)
        self.assertEqual(bob.initial_state['pos'].y, 74)
        self.assertEqual(bob.width, 50)
        self.assertEqual(bob.height, 50)

    def test_as_string(self):
        bob = Square('Bob')
        self.assertEqual(str(bob), 'Actor Bob as Square')


class ComposeActors(unittest.TestCase):

    def test_creation_of_combined_actors(self):
        p = Actor('Parent')
        bob = Square('bob')
        p.add_son(bob)
        star = Star('star')
        p.add_son(star)
        self.assertEqual(len(p.sons), 2)
        self.assertEqual(p.sons[0].name, 'bob')
        self.assertEqual(p.sons[1].name, 'star')
        self.assertEqual(bob.parent, p)
        self.assertEqual(star.parent, p)
        self.assertEqual(p.parent, None)



    def test_get_offset(self):
        a = Actor('A', pos=(50, 70))
        self.assertEqual(a.pos, (50, 70))
        self.assertEqual(a.get_offset(), (0, 0))
        b = Actor('B', pos=(10, 10))
        self.assertEqual(b.pos, (10, 10))
        self.assertEqual(b.get_offset(), (0, 0))
        a.add_son(b)
        self.assertEqual(b.pos, (10, 10))
        self.assertEqual(b.get_offset(), (50, 70))
        c = Actor('C', pos=(11, 22))
        self.assertEqual(c.pos, (11, 22))
        self.assertEqual(c.get_offset(), (0, 0))
        b.add_son(c)
        self.assertEqual(c.pos, (11, 22))
        self.assertEqual(c.get_offset(), (60, 80))








if __name__ == '__main__':
    unittest.main()








#!/usr/bin/env python3

import sys
import math
import logging
import pytest
import unittest

import logs
import actions
from vectors import Vector
from studio import Stage
from control import Scheduler
from actors import Actor, Square, Label, Text, Rect
import colors
from engines import PyGameEngine
import random

logger = logs.create(__name__)


# test actions

def test_uso():
    sch = Scheduler()
    bob = Square('Bob')
    task = actions.Action(bob, 5, 10)
    sch.add_action(task)
    assert (task.actor.name, 5) in sch.actions


def test_get_relative_frame():
    task = actions.Action(Actor('A'), 5, 10)
    assert task.get_relative_frame(5) == 1
    assert task.get_relative_frame(6) == 2
    assert task.get_relative_frame(7) == 3
    assert task.get_relative_frame(8) == 4
    assert task.get_relative_frame(9) == 5
    assert task.get_relative_frame(10) == 6


def test_action_inverval():
    task = actions.Action(Actor('A'), 5, 10)
    assert task.lower_bound == 5
    assert task.upper_bound == 10
    assert task.num_steps == 5


def test_last_frame():
    task = actions.Action(Actor('A'), 5, 10)
    with pytest.raises(ValueError):
        task.is_last(4)
    assert not task.is_last(5)
    assert not task.is_last(6)
    assert not task.is_last(7)
    assert not task.is_last(8)
    assert not task.is_last(9)
    assert task.is_last(10)
    with pytest.raises(ValueError):
        task.is_last(11)


def test_calls():
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
    assert task.started_at_frame == 3
    assert task.ended_at_frame == 6
    assert task.called_on_frames == [3, 4, 5]


def test_start():
    sch = Scheduler()
    bob = Actor('Bob')
    sch.add_action(actions.Move(bob, 5, 10, Vector(72, 54)))
    sch.add_action(actions.Blink(bob, 8, 12))

    assert len(sch.active_actions) == 0  # 0
    sch.next(); assert len(sch.active_actions) == 0  # 1
    sch.next(); assert len(sch.active_actions) == 0  # 2
    sch.next(); assert len(sch.active_actions) == 0  # 3
    sch.next(); assert len(sch.active_actions) == 0  # 4
    sch.next(); assert len(sch.active_actions) == 0  # 5
    sch.next(); assert len(sch.active_actions) == 1  # 6
    sch.next(); assert len(sch.active_actions) == 1  # 7
    sch.next(); assert len(sch.active_actions) == 1  # 8
    sch.next(); assert len(sch.active_actions) == 2  # 9
    sch.next(); assert len(sch.active_actions) == 2  # 10
    sch.next(); assert len(sch.active_actions) == 1  # 11
    sch.next(); assert len(sch.active_actions) == 1  # 12
    sch.next(); assert len(sch.active_actions) == 0  # 13
    sch.next(); assert len(sch.active_actions) == 0  # 14
    sch.next(); assert len(sch.active_actions) == 0  # 15


class TestColorize(unittest.TestCase):
    
    def test_colorize(self):
        sujeto = Actor('A', color='#0080FF')
        sch = Scheduler()
        sch.add_action(actions.Colorize(sujeto, 0, 4, '#FF9000'))

        frame = sch.next() # Frame 0 to 1, first step
        self.assertEqual(frame, 1)
        self.assertEqual(str(sujeto.color), '#4084bf')

        frame = sch.next() # Frame 1 to 2, second step
        self.assertEqual(frame, 2)
        self.assertEqual(str(sujeto.color), '#80887f')
        
        frame = sch.next() # Frame 2 to 3, third step
        self.assertEqual(frame, 3)
        self.assertEqual(str(sujeto.color), '#bf8c40')
        
        frame = sch.next() # Frame 3 to 4, fourth step
        self.assertEqual(frame, 4)
        self.assertEqual(str(sujeto.color), '#ff9000')
       
    def test_colorize_on_pygame(self):
        engine = PyGameEngine()
        stage = Stage(engine)
        stage.num_frames = 75
        for row in range(50, 780, 100):
            for col in range(50, 1280, 100):
                name = 'bob{}x{}'.format(col, row)
                actor = Square(name,
                    color=colors.random_color(),
                    pos=(col, row),
                    side=90,
                    )
                stage.add_actor(actor)
                stage.add_action(
                    actions.Colorize(actor, 5, 70, colors.random_color())
                    )
        for frame in range(stage.num_frames):
            stage.draw(frame)


# Test Move actions

def test_move_five_steps():
    sujeto = Actor('A')
    a = actions.Move(sujeto, 0, 5, Vector(50, 0))
    a.start(0)
    a.step(0); assert sujeto.pos == Vector(10, 0)
    a.step(1); assert sujeto.pos == Vector(20, 0)
    a.step(2); assert sujeto.pos == Vector(30, 0)
    a.step(3); assert sujeto.pos == Vector(40, 0)
    a.step(4); assert sujeto.pos == Vector(50, 0)
    a.end(5)


def test_move_not_in_origin():
    sujeto = Actor('A', pos=Vector(50, 50))
    a = actions.Move(sujeto, 0, 5, Vector(50, 0))
    a.start(0)
    a.step(0); assert sujeto.pos == Vector(50, 40)
    a.step(1); assert sujeto.pos == Vector(50, 30)
    a.step(2); assert sujeto.pos == Vector(50, 20)
    a.step(3); assert sujeto.pos == Vector(50, 10)
    a.step(4); assert sujeto.pos == Vector(50, 0)
    a.end(5)


def test_move_ten_steps():
    sujeto = Actor('A')
    a = actions.Move(sujeto, 0, 10, Vector(100, 10))
    a.start(0)
    a.step(0); assert sujeto.pos == Vector(10, 1)
    a.step(1); assert sujeto.pos == Vector(20, 2)
    a.step(2); assert sujeto.pos == Vector(30, 3)
    a.step(3); assert sujeto.pos == Vector(40, 4)
    a.step(4); assert sujeto.pos == Vector(50, 5)
    a.step(5); assert sujeto.pos == Vector(60, 6)
    a.step(6); assert sujeto.pos == Vector(70, 7)
    a.step(7); assert sujeto.pos == Vector(80, 8)
    a.step(8); assert sujeto.pos == Vector(90, 9)
    a.step(9); assert sujeto.pos == Vector(100, 10)
    a.end(10)


# Test Fall action


def test():
    sujeto = Actor('A')
    a = actions.Fall(sujeto, 0, 5, Vector(100, 0))
    a.start(0)
    a.step(0); assert sujeto.pos == Vector(4, 0)
    a.step(1); assert sujeto.pos == Vector(16, 0)
    a.step(2); assert sujeto.pos == Vector(36, 0)
    a.step(3); assert sujeto.pos == Vector(64, 0)
    a.step(4); assert sujeto.pos == Vector(100, 0)
    a.end(5)


def test_fall_not_in_origin():
    sujeto = Actor('A', pos=(100,0))
    a = actions.Fall(sujeto, 0, 5, Vector(200, 0))
    a.start(0)
    a.step(0); assert sujeto.pos == Vector(104, 0)
    a.step(1); assert sujeto.pos == Vector(116, 0)
    a.step(2); assert sujeto.pos == Vector(136, 0)
    a.step(3); assert sujeto.pos == Vector(164, 0)
    a.step(4); assert sujeto.pos == Vector(200, 0)
    a.end(5)



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
    

    def test_fade_out(self):
        bob = Square('bob')
        hide = actions.FadeOut(bob, 0, 10)
        sch = Scheduler()
        sch.add_action(hide)
        self.assertEqual(bob.alpha, 1.0)
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
        self.assertEqual(sch.frame, 10)
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

    def test_fade_out_with_label(self):
        bob = Text('bob', text='Bob', pos=(640, 320))
        studio = Stage()
        studio.add_actor(bob)
        studio.add_action(actions.FadeOut(bob, 10, 40))
        for frame in range(75):
            studio.draw(frame)

class TestFadeIn(unittest.TestCase):

    def test_show_calls(self):
        bob = Square('bob', alpha=0.0)
        show = actions.FadeIn(bob, 0, 10)
        sch = Scheduler()
        sch.add_action(show)
        self.assertEqual(bob.alpha, 0.0)
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
    pytest.main()

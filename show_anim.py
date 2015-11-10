#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_actions.py

import math
import unittest
import pygame
import argparse

import actors
from vectors import Vector
from actors import (
    State, Actor, Square, RoundRect, 
    Circle, Star, Rect, Label,
    )
from actions import (
    Action, MoveTo, Blink, Fall, Land,
    EasingIn, Swing,
    Timer,
    )
import engines
from control import Scheduler

DEBUG = False

MAX_FRAMES = 200 
DEFAULT_FPS = 25 

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)
CENTER = (WIDTH // 2, HEIGHT // 2)

parser = argparse.ArgumentParser(description='Show animations')
parser.add_argument(
    '--fps', dest='fps', type=int,
    help='Define FPS (Frames Per Second)'
    )
parser.add_argument(
    '--debug', dest='debug', action='store_true',
    help='Modo debug activo'
    )

args = parser.parse_args()
FPS = args.fps or DEFAULT_FPS
DEBUG = args.debug

sch = Scheduler()

f1 = Rect('f1', pos=(50, 0), color='brown', width=90, height=25)
sch.add_action(EasingIn(f1, 0, 150, Vector(50, 700)))

f2 = Rect('f2', pos=(150, 0), color='white', width=90, height=25)
sch.add_action(MoveTo(f2, 0, 150, Vector(150, 700)))

f3 = Rect('f3', pos=(250, 0), color='#334588', width=90, height=25)
sch.add_action(Land(f3, 0, 150, Vector(250, 700)))

f4 = Rect('f4', pos=(350, 0), color='#f0A371', width=90, height=25)
sch.add_action(Swing(f4, 0, 150, Vector(350, 700)))


lbl_fall = Label('Fall', 'Fall', pos=(450,10), color="#333333")
sch.add_action(Fall(lbl_fall, 0, 50, (450, 400)))
sch.add_action(EasingIn(lbl_fall, 186, 196, (450, 10)))

lbl_easing_in = Label('easing_in', 'Easing in', pos=(600,10), color="#333333")
sch.add_action(EasingIn(lbl_easing_in, 0, 50, (600, 400)))
sch.add_action(EasingIn(lbl_easing_in, 188, 198, (600, 10)))

lbl_swing = Label('swing', 'Swing', pos=(750, 10), color="#333333")
sch.add_action(Swing(lbl_swing, 0, 50, (750, 400)))
sch.add_action(EasingIn(lbl_swing, 190, 200, (750, 10)))


pelota = Circle('Pelota', pos=(480, 10), color='gold')
sch.add_action(Fall(pelota, 0, 25, (480, 670)))
sch.add_action(Land(pelota, 25, 50, (480, 12)))
sch.add_action(Fall(pelota, 50, 75, (480, 670)))
sch.add_action(Land(pelota, 75, 100, (480, 10)))
sch.add_action(Fall(pelota, 100, 125, (480, 670)))
sch.add_action(Land(pelota, 125, 150, (480, 10)))

sch.add_action(Fall(pelota, 150, 175, (480, 670)))
sch.add_action(Land(pelota, 175, 200, (480, 10)))

bob = RoundRect('Bob', color='cadetblue', width=60, height=50)
bob.place(10, 400)
sch.add_action(Land(bob, 1, 20, Vector(400, 400)))
sch.add_action(Fall(bob, 21, 40, Vector(10, 400)))

star = Star('Marylin', color='red', alpha=0.33)
sch.add_action(Swing(star, 0, 100, (WIDTH, HEIGHT)))
sch.add_action(Swing(star, 100, 200, (0, 0)))

actors =[ 
    pelota, bob, f1, f2, f4,
    f3, star, lbl_fall, 
    lbl_easing_in, lbl_swing
    ]

lbl_clock = Label('clock', '00:00.00',
    pos=(1120, 670),
    color="#CFCFCF",
    alpha=0.5,
    )
sch.add_action(Timer(lbl_clock, 0, 200))

actors.append(lbl_clock)

in_stage = actors[:]
engine = engines.PyGameEngine()
clock = pygame.time.Clock()
frame = 0
inside_loop = True
while inside_loop:
    engine.clear(frame)
    if DEBUG:
        engine.grid()

    for actor in in_stage:
        actor.start_draw(engine) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inside_loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inside_loop = False

    pygame.display.flip()
    clock.tick(FPS)
    frame = sch.next() % MAX_FRAMES
    if frame == 0:
        sch.reset()
        for actor in actors:
            actor.reset()

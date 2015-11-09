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
    Circle, Star, Rect,
    )
from actions import Action, MoveTo, Blink, Fall, Land
import engines
from control import Scheduler

DEBUG = False

MAX_FRAMES = 150
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

dot = Square('dot', color='red', pos=Vector(100,100), width=3, height=3)

charles = Rect('Charles', pos=(100, 0), color='brown', width=75, height=25)
sch.add_action(Fall(charles, 0, 40, Vector(100, 300)))

dorothy = Square('Dorothy', pos=(200, 0), color='white', side=75)
sch.add_action(MoveTo(dorothy, 0, 40, Vector(200, 300)))

evelyn = Square('Evelyn', pos=(300, 0), color='#334588', width=75, height=25)
sch.add_action(Land(evelyn, 0, 40, Vector(300, 300)))

sch.add_action(MoveTo(charles, 41, 48, charles.initial_state.pos))
sch.add_action(MoveTo(dorothy, 41, 48, dorothy.initial_state.pos))
sch.add_action(MoveTo(evelyn, 41, 48, evelyn.initial_state.pos))


albert = Circle('Albert')
albert.place(480, HEIGHT // 2)
albert.color = '#A2E3BB'
sch.add_action(Land(albert, 0, 24, (480, 0)))
sch.add_action(Fall(albert, 25, 48, (480, HEIGHT // 2)))
sch.add_action(Land(albert, 49, 74, (480, 0)))
sch.add_action(Fall(albert, 75, 99, (480, HEIGHT // 2)))


bob = RoundRect('Bob', color='cadetblue', width=60, height=50)
bob.place(10, 400)
sch.add_action(Land(bob, 1, 20, Vector(400, 400)))
sch.add_action(Fall(bob, 21, 40, Vector(10, 400)))

marylin = Star('Marylin', color='red', alpha=0.33)
sch.add_action(MoveTo(marylin, 0, MAX_FRAMES, (WIDTH, HEIGHT)))

actors =[albert, bob, charles, dot, dorothy, evelyn, marylin]
in_stage = [albert, bob, charles, dot, dorothy, evelyn, marylin]

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

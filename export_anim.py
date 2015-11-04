#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_actions.py

import math
import unittest
import argparse

import svgwrite

from vectors import Vector
from actors import State, Actor, Square, RoundSquare, Interval, Circle
from actors import Color
from actions import Action, MoveTo, Blink, Fall, Land





MAX_FRAMES = 150

parser = argparse.ArgumentParser(description='Export animation sequence')
parser.add_argument(
    '--size', dest='size', default='1280x720',
    help='Define Size'
    )
parser.add_argument(
    '--debug', dest='debug', action='store_true',
    help='Modo debug activo'
    )

args = parser.parse_args()
WIDTH, HEIGHT = (int(_) for _ in args.size.split('x'))
SIZE = (WIDTH, HEIGHT)
CENTER = (WIDTH // 2, HEIGHT // 2)
DEBUG = args.debug
    


def draw_grid(dwg):
    y_axis = 100
    while y_axis < WIDTH:
        dwg.add(dwg.line((y_axis, 0), (y_axis, HEIGHT), stroke=svgwrite.rgb(10, 10, 16, '%')))
        y_axis += 100
    x_axis = 100
    while x_axis < HEIGHT:
        dwg.add(dwg.line((0, x_axis), (WIDTH, x_axis), stroke=svgwrite.rgb(10, 10, 16, '%')))
        x_axis += 100

def draw_actor(scr, actor):
    color = actor.state.color.as_rgb()
    points = [actor.state.pos + v for v in actor.vertexs]   
    pygame.draw.polygon(scr, color, points, 0)
    pygame.draw.aalines(scr, WHITE, True, points)
    if DEBUG:
        for v in points:
            pygame.draw.circle(scr, RED, v, 3, 0)
        write_at(scr, actor.state.pos, actor.name)

charles = Square('Charles', 
    State(pos=Vector(100, 0), color='brown4'), 
    width=75, height=25
    )

charles.next()

dwg = svgwrite.Drawing('test.svg', size=(1280, 720))
draw_grid(dwg)
dwg.add(dwg.line((0, 0), (1280, 720), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.rect((10, 10), (100, 100), rx=15, ry=15, stroke='blue'))

dwg.add(dwg.text('Test', insert=(100, 200), fill='red'))
dwg.save()

#        draw_grid(screen)

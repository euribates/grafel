#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_actions.py

import math
import unittest
import pygame
import argparse

from vectors import Vector
from actors import (
    State, Actor, Square, RoundSquare, 
    Interval, Circle, Star,
    )
from actors import Color
from actions import Action, MoveTo, Blink, Fall, Land

DEBUG = False

MAX_FRAMES = 150
DEFAULT_FPS = 25 

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)
CENTER = (WIDTH // 2, HEIGHT // 2)

from colors import BLACK, WHITE, RED

parser = argparse.ArgumentParser(description='Show animations')
parser.add_argument(
    '--fps', dest='fps', type=int,
    help='Define FPS (Frames Per Second)'
    )
parser.add_argument(
    '--debug', dest='debug', action='store_true',
    help='Modo debug activo'
    )
parser.add_argument(
    '--save', dest='save', action='store_true', default=False,
    help='Salvar los frames'
    )

args = parser.parse_args()
FPS = args.fps or DEFAULT_FPS
DEBUG = args.debug
    

class Label(pygame.sprite.DirtySprite):

    def __init__(self, pos=(WIDTH-40, HEIGHT-20), text='', color=None):
        super().__init__()
        self.pos = pos
        self.text = text
        self.color = color if color else pygame.Color(255,255,255,128)
        self.fuente = pygame.font.SysFont('Arial', 16)
        self.image = self.fuente.render(str(self.text), True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

    def update(self, text=''):
        if text:
            self.text = text
            self.image = self.fuente.render(str(self.text), True, self.color)
            self.rect = self.image.get_rect()
            self.rect.topleft = self.pos
            self.dirty = 1


def write_at(scr, pos, text):
    fuente = pygame.font.SysFont('Arial', 12)
    color = pygame.Color(255,255,255,128)
    image = fuente.render(str(text), True, color)
    rect = image.get_rect()
    rect.topleft = pos
    scr.blit(image, rect)
    
def draw_grid(scr):
    y_axis = 100
    while y_axis < WIDTH:
        pygame.draw.line(scr, (64,64,64, 64), (y_axis, 0), (y_axis, HEIGHT), 1)
        y_axis += 100
    x_axis = 100
    while x_axis < HEIGHT:
        pygame.draw.line(scr, (64,64,64, 64), (0, x_axis), (WIDTH, x_axis), 1)
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

dot = Square('dot', State(color='red', pos=Vector(100,100)), width=3, height=3)

charles = Square('Charles', 
    State(pos=Vector(100, 0), color='brown4'), 
    width=75, height=25
    )
Fall(charles, 0, 40, Vector(100, 300))
#MoveTo(charles, 0, 39, Vector(100, 200))

dorothy = Square('Dorothy', 
    state= State(pos=Vector(200, 0), color='white'),
    width=75, height=25
    )
MoveTo(dorothy, 0, 40, Vector(200, 300))

evelyn = Square('Evelyn', 
    state= State(pos=Vector(300, 0), color='#334588'),
    width=75, height=25
    )
Land(evelyn, 0, 40, Vector(300, 300))

MoveTo(charles, 41, 48, charles.initial_state.pos)
MoveTo(dorothy, 41, 48, dorothy.initial_state.pos)
MoveTo(evelyn, 41, 48, evelyn.initial_state.pos)


albert = Circle('Albert')
albert.place(480, HEIGHT // 2)
albert.color = '#A2E3BB'
Land(albert, 0, 24, Vector(480, 0))
Fall(albert, 25, 48, Vector(480, HEIGHT // 2))
Land(albert, 49, 74, Vector(480, 0))
Fall(albert, 75, 99, Vector(480, HEIGHT // 2))


bob = RoundSquare('Bob', State(color='cadetblue'), width=60, height=50)
bob.place(10, 400)
Land(bob, 1, 20, Vector(400, 400))
Fall(bob, 21, 40, Vector(10, 400))

marylin = Star('Marylin')
marylin.color = 'red'
MoveTo(marylin, 0, MAX_FRAMES, Vector(WIDTH, HEIGHT))

actors =[albert, bob, charles, dot, dorothy, evelyn, marylin]
in_stage = [albert, bob, charles, dot, dorothy, evelyn, marylin]

pygame.init()
screen = pygame.display.set_mode(
    SIZE,
    pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SRCALPHA
    )
clock = pygame.time.Clock()

lbl_frame = Label()
labels = pygame.sprite.Group(lbl_frame)
inside_loop = True
frame = 0
first_loop = True
while inside_loop:
    screen.fill(BLACK)
    if DEBUG:
        draw_grid(screen)
    lbl_frame.update(frame)
    labels.draw(screen)
    for actor in in_stage:
        draw_actor(screen, actor) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inside_loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inside_loop = False
    pygame.display.flip()
    if first_loop and args.save:
        pygame.image.save(screen, 'sec/frame_{:04d}.png'.format(frame))

    clock.tick(FPS)
    frame = (frame + 1) % MAX_FRAMES
    if frame == 0:
        for actor in actors:
            actor.reset()
        first_loop = False
    else:
        for actor in actors:
            actor.next()

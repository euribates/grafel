#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os
import six

from six.moves import reduce

import sys

from colors import Color
from vectors import Vector

import svgwrite
import pygame
import logging



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(stream=sys.stderr)
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
    ))
logger.addHandler(ch)


class BaseEngine:

    def prepare(self, scene, debug=False):
        self.scene = scene
        self.debug = debug

    def clear(self):
        logger.debug('Limpiamos la pantalla.')

    def lines(self, points, color):
        logger.debug('draw line {} for {} points: [{}]'.format(
            color,
            len(points),
            ', '.join([str(_) for _ in points]),
            ))

    def end(self):
        logger.debug('Acabamos de dibujar.')


class SVGEngine(BaseEngine):

    def __init__(self, output_dir='/tmp'):
        self.output_dir = output_dir

    def clear(self):
        filename = 'frame_{:05d}.svg'.format(self.scene.tick)
        full_fn = os.path.join(self.output_dir, filename)
        logger.debug('Ready to draw on {}'.format(full_fn))
        self.dwg = svgwrite.Drawing(full_fn, size=self.scene.size)
        self.dwg.add(
            self.dwg.rect(
                insert=(0, 0), 
                size=(self.scene.width, self.scene.height), 
                fill=svgwrite.rgb(0,0,0),
                )
            )

    def lines(self, points, color):
        stroke = svgwrite.rgb(color.red, color.green, color.blue)
        logger.debug('color: {}'.format(color))
        logger.debug('stroke: {}'.format(stroke))
        points.append(points[0])
        def f(a, b):
            self.dwg.add(self.dwg.line(a, b, stroke=stroke))
            return b
        reduce(f, points)

    def end(self):
        self.dwg.save()

class PyGameEngine(BaseEngine):

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()


    def prepare(self, scene, debug=False):
        super().prepare(scene, debug)
        self.screen = pygame.display.set_mode(
            self.scene.size,
            pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SRCALPHA
            )

    def clear(self):
        self.screen.fill(self.scene.background.as_rgb())

    def lines(self, points, color):
        pygame.draw.polygon(self.screen, color.as_rgb(), points, 0)
        pygame.draw.aalines(
            self.screen,
            color.as_rgb(),
            True,
            points
            )
        if self.debug:
            for v in points:
                pygame.draw.circle(scr, (255, 0, 0), v, 3, 0)

    def draw_text(self, pos, text, color):
        f = pygame.font.SysFont('Helvetica,arial', 24, bold=False, italic=False)
        s = f.render(text, True, color.as_rgb())
        rect = s.get_rect()
        rect.center = pos
        self.screen.blit(s, rect)

    def end(self):
        pygame.display.flip()
        self.clock.tick(self.scene.fps)


class Stage:

    DEFAULT_NUM_FRAMES = 150
    DEFAULT_FPS = 25
    DEFAULT_SIZE = (1024, 760)
    DEFAULT_BACKGROUND = Color('black')
    DEFAULT_FOREGROUND = Color('white')

    def __init__(self, engine, **kwargs):
        self.engine = engine
        self.num_frames = kwargs.pop('num_frames', Stage.DEFAULT_NUM_FRAMES)
        self.fps = kwargs.pop('fps', Stage.DEFAULT_FPS)
        self.width, self.height = kwargs.pop('size', Stage.DEFAULT_SIZE)
        self.background = kwargs.pop('background', Stage.DEFAULT_BACKGROUND)
        self.foreground = kwargs.pop('foreground', Stage.DEFAULT_FOREGROUND)
        self.size = Vector(self.width, self.height)
        self.center = self.size / 2
        self.top_right = Vector(self.width, 0)
        self.top_left = Vector(0, 0)
        self.bottom_right = Vector(self.width, self.height)
        self.bottom_left = Vector(0, self.height)
        self.actors = []
        self.on_stage = []
        self.tick = 0
        self.engine.prepare(self)

    def add_actor(self, actor, on_stage=True):
        self.actors.append(actor)
        if on_stage:
            self.on_stage.append(actor)

    def next(self):
        self.tick += 1
        for actor in self.actors:
            actor.next()

    def draw(self):
        self.engine.clear()
        for actor in self.on_stage:
            self.draw_actor(actor)
        self.engine.end()

    def draw_actor(self, actor):
        logger.info('actor: {} (sons: {} | parent: {})'.format(
            actor,
            len(actor.sons),
            actor.parent,
            ))

        for son in actor.sons:
            self.draw_actor(son)
        if actor.vertexs:
            offset = actor.get_offset()
            points = [offset + actor.state.pos + v for v in actor.vertexs]
            self.engine.lines(points, actor.state.color)
        elif actor.text:
            offset = actor.get_offset()
            self.engine.draw_text(
                actor.state.pos + offset,
                actor.text,
                actor.state.color,
                )

        
    def draw_grid(self, dwg):
        color = Color(10, 10, 16)        
        y = 100
        while y < self.width:
            self.engine.lines([(y, 0), (y, self.height)], color)
            y += 100
        x = 100
        while x < self.height:
            self.engine.lines([(0, x), (self.width, x)], color)
            x += 100


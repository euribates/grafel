#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os
import six

from six.moves import reduce

import sys

import colors
import vectors

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

    def __init__(self, width=1280, height=720, fps=25, bg_color=colors.black):
        self.width = width
        self.height = height
        self.size = vectors.Vector(width, height)
        self.fps = fps
        self.bg_color = bg_color
        self.frame = 0

    def clear(self, frame):
        logger.info('Clear screen; prepare for start drawing frame {}.'.format(frame))
        self.frame = frame

    def draw_actor(self, actor):
        logger.info('draw actor "{}" ({}) in color {} at position {}'.format(
            actor.name,
            actor.__class__.__name__,
            actor.color,
            actor.pos,
            ))

    def end(self):
        logger.debug('End of drawing.')


class SVGEngine(BaseEngine):

    def __init__(self, width=1280, height=720, fps=25, output_dir='/tmp'):
        super().__init__(width, height, fps)
        self.output_dir = output_dir

    def clear(self, frame):
        super().clear(frame)
        filename = 'frame_{:05d}.svg'.format(frame)
        full_fn = os.path.join(self.output_dir, filename)
        self.dwg = svgwrite.Drawing(full_fn, size=(self.width, self.height))
        self.dwg.add(
            self.dwg.rect(
                insert=(0, 0), 
                size=(self.width, self.height), 
                fill=self.bg_color.as_svg(),
                )
            )

    def draw_actor(self, actor):
        super().draw_actor(actor)
        self.dwg.add(self.dwg.text(
            actor.name, insert=actor.pos, fill=actor.color,
            font_size="27", text_anchor="middle"
            ))
        self.dwg.add(self.dwg.rect(
            actor.pos,
            (actor.width, actor.height),
            fill=actor.color,
            ))

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




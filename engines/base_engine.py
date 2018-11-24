#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import colors
from colors import white
import vectors
import logs

logger = logs.create(__name__)


class BaseEngine:

    def __init__(self, width=1280, height=720, fps=25):
        self.width = width
        self.height = height
        self.size = vectors.Vector(width, height)
        self.fps = fps
        self.bg_color = colors.black
        self.fg_color = colors.white
        self.frame = 0
        self.debug = False

    def clear(self, frame, grid=False):
        logger.info('Clear screen; prepare for start drawing frame {}.'.format(
            frame))
        self.frame = frame

    def line(self, x0, y0, x1, y1, color=colors.white, alpha=1.0):
        logger.info('Draw line from {}x{} to {}x{} [color:{}|alpha:{}]'.format(
            x0, y0, x1, y1,
            color, alpha
            ))

    def grid(self, step=100):
        for x in range(step, self.width, step):
            self.line(x, 0, x, self.height, alpha=0.25)
        for y in range(step, self.height, step):
            self.line(0, y, self.width, y, alpha=0.25)

    def box(self, x, y, width, height, color=colors.white, alpha=1.0):
        logger.info(
            f'Draw box {x}x{y} width {width} height {height})'
            f' color {color} alpha {alpha}'
            )

    def rect(self, x, y, width, height, color=white, alpha=1.0):
        logger.info('Draw rect ({}, {}, {}, {}) [color:{}|alpha:{}]'.format(
            x, y, width, height, color, alpha,
            ))

    def circle(self, x, y, r, color=white, alpha=1.0):
        logger.info(
            f'Draw circle at {x}x{y}'
            f' radius {r} color {color} alpha {alpha}]'
            )

    def polygon(self, x, y, rpoints, color=white, alpha=1.0):
        n_points = len(rpoints)
        logger.info(
            f'Draw polygon starting as {x}x{y}'
            f' with {n_points}'
            f' color {color}'
            f' alpha:{alpha}'
            )

    def end(self):
        logger.debug('End of drawing.')

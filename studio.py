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

from actors import Level
from colors import Color
from vectors import Vector

import svgwrite
import pygame
import logs

logger = logs.create(__name__)

class Stage:

    DEFAULT_NUM_FRAMES = 150
    DEFAULT_FPS = 25
    DEFAULT_SIZE = (1280, 720)
    DEFAULT_BACKGROUND = Color('black')
    DEFAULT_FOREGROUND = Color('white')

    def __init__(self, engine, **kwargs):
        self.engine = engine
        self.num_frames = (
            kwargs.pop('num_frames', Stage.DEFAULT_NUM_FRAMES) or
            Stage.DEFAULT_NUM_FRAMES
            )
        self.fps = kwargs.pop('fps', Stage.DEFAULT_FPS) or Stage.DEFAULT_FPS
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

    def add_actor(self, actor, on_stage=True):
        self.actors.append(actor)

    def add_actors(self, *args):
        self.actors.extend(args)

    def draw(self, frame):
        self.engine.clear(frame)
        actives = [_ for _ in self.actors if _.level > Level.OFF_STAGE] 
        background = [_ for _ in actives if _.level == Level.ON_BACKGROUND]
        for actor in background:
            actor.start_draw(self.engine)
        on_stage = [_ for _ in actives if _.level == Level.ON_STAGE]
        for actor in on_stage:
            actor.start_draw(self.engine)
        foreground = [_ for _ in actives if _.level == Level.ON_FOREGROUND]
        for actor in foreground:
            actor.start_draw(self.engine)
        self.engine.end()






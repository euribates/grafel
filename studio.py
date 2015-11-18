#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from actors import Level
from colors import Color
from vectors import Vector
from control import Scheduler
from engines import PyGameEngine

import svgwrite
import pygame
import logs
import defaults

logger = logs.create(__name__)

#~ class Singleton(type):
#~     _instances = {}
#~     def __call__(cls, *args, **kwargs):
#~         if cls not in cls._instances:
#~             cls._instances[cls] = super().__call__(*args, **kwargs)
#~         return cls._instances[cls]
#~
#~ class Stage(metaclass=Singleton):


class Stage():
    def __init__(self, engine=None, scheduler=None, options=None):
        self.engine = engine if engine else PyGameEngine()
        self.scheduler = scheduler if scheduler else Scheduler()
        self.actors = []
        if options:
            self.size = Vector(*[int(_) for _ in options.size.split('x')])
            self.width = self.size[0]
            self.height = self.size[1]
            self.num_frames = options.num_frames
            self.fps = options.fps
            self.background = Color(options.background)
            self.foreground = Color(options.foreground)
        else:
            self.width = defaults.WIDTH
            self.height = defaults.HEIGHT
            self.size = Vector(self.width, self.height)
            self.num_frames = defaults.NUM_FRAMES
            self.fps = defaults.FPS
            self.background = Color(defaults.BACKGROUND)
            self.foreground = Color(defaults.FOREGROUND)

        self.engine.fg_color = self.foreground
        self.engine.bgcolor = self.background

        self.refs = {
            'center': self.size / 2,
            'top_right': Vector(self.width, 0),
            'top_left': Vector(0, 0),
            'bottom_right': Vector(self.width, self.height),
            'bottom_left': Vector(0, self.height),
            }

    def add_actor(self, actor):
        self.actors.append(actor)

    def add_actors(self, *args):
        self.actors.extend(args)

    def add_action(self, action):
        self.scheduler.add_action(action)

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
        self.scheduler.next()

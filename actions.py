#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# actions.py

from __future__ import print_function

import sys
from copy import copy
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING) 

#ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)
#ch.setFormatter(logging.Formatter(
#    '%(asctime)s %(name)s %(levelname)s %(message)s'
#    ))
#logger.addHandler(ch)

from vectors import Vector


class Interval:
    def __init__(self, lower_bound, upper_bound=None):
        self.lower_bound = lower_bound
        self.upper_bound = (upper_bound or lower_bound) + 1

    def __contains__(self, key):
        return self.lower_bound <= key < self.upper_bound

    def __str__(self):
        return '[{}-{}]'.format(
            self.lower_bound,
            self.upper_bound-1,
            )

    def __len__(self):
        return self.upper_bound - self.lower_bound

    def is_last(self, item):
        if item < self.lower_bound or item >= self.upper_bound:
            raise ValueError(
                'El valor cae fuera del intervalo {}'.format(self)
                )
        return item == self.upper_bound-1

    def __iter__(self):
        self._next_result = self.lower_bound
        return self

    def __next__(self):
        if self._next_result >= self.upper_bound:
            raise StopIteration 
        result = self._next_result
        self._next_result += 1
        return result

class Action:
    def __init__(self, actor, from_frame, to_frame):
        self.actor = actor
        self.actor.add_action(from_frame, self)
        self.interval = Interval(from_frame, to_frame)
        self.num_frames = len(self.interval) - 1

    def __repr__(self):
        return '{}([{}, {}, {})'.format(
            self.__class__.__name__,
            repr(self.actor),
            self.interval.lower_bound,
            self.interval.upper_bound-1,
            )

    def __str__(self):
        return '{} on {}'.format(
            self.__class__.__name__,
            self.actor
            )

    def start(self, frame):
        logger.debug('Action {} stars at frame {}'.format(
            self.__class__.__name__,
            frame,
            ))

    def end(self, frame):
        logger.debug('Action {} ends at frame {}'.format(
            self.__class__.__name__,
            frame,
            ))
        
    def __call__(self, frame, *args, **kwargs):
        logger.debug('Action {} called for frame {}'.format(
            self.__class__.__name__,
            frame,
            ))


class Blink(Action):
    
    def start(self, frame):
        self.colors = {
                f: self.actor.state.color if f % 2 else 'black' 
                for f in self.interval
                }
        self.colors[self.interval.upper_bound] = self.actor.state.color

    def __call__(self, frame):
        return {'color': self.colors[frame]}


class MoveTo(Action):
    def __init__(self, actor, from_frame, to_frame, new_position):
        super().__init__(actor, from_frame, to_frame)
        self.new_position = new_position

    def start(self, frame):
        super().start(frame)
        position = copy(self.actor.state.pos)
        logger.debug('position: {}'.format(position))
        logger.debug('new_position: {}'.format(self.new_position))
        logger.debug('num_frames: {}'.format(self.num_frames))

        self.delta = Vector(
            (self.new_position.x - position.x) / self.num_frames,
            (self.new_position.y - position.y) / self.num_frames,
            )
        logger.debug('delta: {}'.format(self.delta))

    def __call__(self, frame):
        super().__call__(frame)
        relative_frame = frame - self.interval.lower_bound
        if relative_frame == 0:
            return {}
        else:
            return {'pos': self.delta}

class Fall(Action):
    
    def __init__(self, actor, from_frame, to_frame, new_position):
        super().__init__(actor, from_frame, to_frame)
        self.new_position = new_position

    def start(self, frame):
        logger.debug('start({})'.format(frame))
        self.initial_position = copy(self.actor.state.pos)
        logger.debug('initial_position = {}'.format(self.initial_position))
        self.change_value = self.new_position - self.initial_position
        logger.debug('self.new_position = {}'.format(self.new_position))
        logger.debug('self.change_value = {}'.format(self.change_value))
        self.previo = copy(self.initial_position)

    def __call__(self, frame):
        logger.debug('__call__({})'.format(frame))
        relative_frame = frame - self.interval.lower_bound
        logger.debug('relative_frame = {}'.format(relative_frame))
        t = relative_frame / self.num_frames
        logger.debug('t = {}'.format(t))
        new_position = Vector(
            x = self.change_value.x * t**2 + self.initial_position.x,
            y = self.change_value.y * t**2 + self.initial_position.y,
            )
        delta = new_position - self.previo
        self.previo = new_position
        return { 'pos': delta }

class Land(Action):
    
    def __init__(self, actor, from_frame, to_frame, new_position):
        super().__init__(actor, from_frame, to_frame)
        self.new_position = new_position

    def start(self, frame):
        logger.debug('start({})'.format(frame))
        self.initial_position = copy(self.actor.state.pos)
        logger.debug('initial_position = {}'.format(self.initial_position))
        self.change_value = self.new_position - self.initial_position
        logger.debug('self.new_position = {}'.format(self.new_position))
        logger.debug('self.change_value = {}'.format(self.change_value))
        self.previo = copy(self.initial_position)

    def __call__(self, frame):
        logger.debug('__call__({})'.format(frame))
        relative_frame = frame - self.interval.lower_bound
        logger.debug('relative_frame = {}'.format(relative_frame))
        t = relative_frame / self.num_frames
        logger.debug('t = {}'.format(t))
        new_position = Vector(
            x = -self.change_value.x * t * (t-2) + self.initial_position.x,
            y = -self.change_value.y * t * (t-2) + self.initial_position.y,
            )
        delta = new_position - self.previo
        self.previo = new_position
        return { 'pos': delta }






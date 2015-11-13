#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# actions.py

import sys
from copy import copy
import logs
from vectors import Vector
from actors import Level

logger = logs.create(__name__)


class Interval:
    def __init__(self, lower_bound, upper_bound=None):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound or (lower_bound + 1)

    def __contains__(self, key):
        return self.lower_bound <= key <= self.upper_bound

    def __str__(self):
        return '[{}~{}]'.format(
            self.lower_bound,
            self.upper_bound,
            )

    def __repr__(self):
        return 'Interval({}, {})'.format(
            self.lower_bound,
            self.upper_bound,
            )

    def __eq__(self, op2):
        if isinstance(op2, tuple):
            lower_bound, upper_bound = op2
        else:
            lower_bound = op2.lower_bound
            upper_bound = op2.upper_bound
        return self.lower_bound == lower_bound and  \
               self.upper_bound == upper_bound

    def __len__(self):
        return self.upper_bound - self.lower_bound + 1

    def is_last(self, item):
        if item < self.lower_bound or item > self.upper_bound:
            raise ValueError(
                'El valor cae fuera del intervalo {}'.format(self)
                )
        return item == self.upper_bound

    def __iter__(self):
        self._next_result = self.lower_bound
        return self

    def __next__(self):
        if self._next_result > self.upper_bound:
            raise StopIteration 
        result = self._next_result
        self._next_result += 1
        return result


class Action:
    def __init__(self, actor, from_frame, to_frame):
        self.actor = actor
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

class MoveAction(Action):
    def __init__(self, actor, from_frame, to_frame, new_position):
        super().__init__(actor, from_frame, to_frame)
        self.new_position = new_position
        if isinstance(self.new_position, tuple):
            x, y = self.new_position
            self.new_position = Vector(x, y)


class Exit(Action):
    def start(self, frame):
        self.actor.level = Level.OFF_STAGE

class Enter(MoveAction):
    def start(self, frame):
        self.actor.pos = self.new_position
        self.actor.level = Level.ON_STAGE

class Background(Action):
    def start(self, frame):
        self.actor.level = Level.ON_BACKGROUND

class Foreground(Action):
    def start(self, frame):
        self.actor.level = Level.ON_FOREGROUND


class MoveTo(MoveAction):

    def end(self, frame):
        logger.info('Ended action {} on frame {}'.format(self, frame))


    def start(self, frame):
        logger.info('Started action {} on frame {}'.format(self, frame))
        super().start(frame)
        position = copy(self.actor.state.pos)
        logger.info('position: {}'.format(position))
        logger.info('new_position: {}'.format(self.new_position))
        logger.info('num_frames: {}'.format(self.num_frames))

        self.delta = Vector(
            (self.new_position.x - position.x) / self.num_frames,
            (self.new_position.y - position.y) / self.num_frames,
            )
        logger.info('delta: {}'.format(self.delta))

    def __call__(self, frame):
        logger.info('Called {} on frame {}'.format(self, frame))
        super().__call__(frame)
        relative_frame = frame - self.interval.lower_bound
        logger.info('{} frame: {} | relative_frame:{}'.format(
            self.actor.name,
            frame, relative_frame
            ))
        return {'pos': self.delta}

class Fall(MoveAction):
    
    def start(self, frame):
        self.initial_position = copy(self.actor.state.pos)
        self.change_value = self.new_position - self.initial_position
        self.previo = copy(self.initial_position)

    def __call__(self, frame):
        logger.info('Fall {} __call__({})'.format(self.actor, frame))
        relative_frame = frame - self.interval.lower_bound
        t = relative_frame / self.num_frames
        new_position = Vector(
            x = self.change_value.x * t**2 + self.initial_position.x,
            y = self.change_value.y * t**2 + self.initial_position.y,
            )
        delta = new_position - self.previo
        self.previo = new_position
        return { 'pos': delta }

class Land(MoveAction):
    
    def start(self, frame):
        self.initial_position = copy(self.actor.state.pos)
        self.change_value = self.new_position - self.initial_position
        self.previo = copy(self.initial_position)

    def __call__(self, frame):
        relative_frame = frame - self.interval.lower_bound
        t = relative_frame / self.num_frames
        new_position = Vector(
            x = -self.change_value.x * t * (t-2) + self.initial_position.x,
            y = -self.change_value.y * t * (t-2) + self.initial_position.y,
            )
        delta = new_position - self.previo
        self.previo = new_position
        return { 'pos': delta }


class EaseIn(MoveAction):
    
    def start(self, frame):
        self.initial_position = copy(self.actor.state.pos)
        self.change_value = self.new_position - self.initial_position
        self.previo = copy(self.initial_position)

    def __call__(self, frame):
        logger.info('EasingIn {} __call__({})'.format(self.actor, frame))
        relative_frame = frame - self.interval.lower_bound
        t = relative_frame / self.num_frames
        new_position = Vector(
            x = self.change_value.x * t**3 + self.initial_position.x,
            y = self.change_value.y * t**3 + self.initial_position.y,
            )
        delta = new_position - self.previo
        self.previo = new_position
        return { 'pos': delta }

class EaseOut(MoveAction):
    
    def start(self, frame):
        self.initial_position = copy(self.actor.state.pos)
        self.change_value = self.new_position - self.initial_position
        self.previo = copy(self.initial_position)

    def __call__(self, frame):
        logger.info('EasingIn {} __call__({})'.format(self.actor, frame))
        relative_frame = frame - self.interval.lower_bound
        t = relative_frame / self.num_frames
        t -= 1
        new_position = Vector(
            x = self.change_value.x * (t**3 + 1) + self.initial_position.x,
            y = self.change_value.y * (t**3 + 1) + self.initial_position.y,
            )
        delta = new_position - self.previo
        self.previo = new_position
        return { 'pos': delta }



class Swing(MoveAction):
    
    def start(self, frame):
        self.initial_position = copy(self.actor.state.pos)
        self.change_value = self.new_position - self.initial_position
        self.previo = copy(self.initial_position)

    def __call__(self, frame):
        logger.info('EasingIn {} __call__({})'.format(self.actor, frame))
        relative_frame = frame - self.interval.lower_bound
        t = relative_frame / (self.num_frames / 2)
        if t < 1:
            new_position = Vector(
                x = self.change_value.x / 2 * t**3 + self.initial_position.x,
                y = self.change_value.y / 2 * t**3 + self.initial_position.y,
                )
        else:
            t -= 2
            new_position = Vector(
                x = self.change_value.x / 2 * (t**3 + 2) + self.initial_position.x,
                y = self.change_value.y / 2 * (t**3 + 2) + self.initial_position.y,
                )
        delta = new_position - self.previo
        self.previo = new_position
        return { 'pos': delta }

class Timer(Action):

    FPS = 25

    def start(self, frame):
        logger.info('Timer.start on {} called'.format(self.actor))
        self.actor.text = '00:00.00'

    def __call__(self, frame):
        logger.info('Timer.call({}) on {} called'.format(
            frame, 
            self.actor,
            ))
        fps = Timer.FPS
        self.actor.text = '{mins:02d}:{secs:02d}.{frac:02d}'.format(
            mins = frame // (60*Timer.FPS),  # 60 s/frame * 25 frame/s
            secs = frame // Timer.FPS,
            frac = frame % Timer.FPS,
            )
        


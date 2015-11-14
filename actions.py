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

_map_actions = {}

def register_action(klass):
    global _map_actions
    key = klass.__name__.lower()
    if key in _map_actions:
        raise KeyError('La clase {} ya está registrada'.format(key))
    _map_actions[key] = klass
    return klass

class Action:
    def __init__(self, actor, from_frame, to_frame=None):
        self.actor = actor
        self.lower_bound = from_frame
        self.upper_bound = to_frame or (from_frame + 1)
        self.num_steps = self.upper_bound - self.lower_bound

    def __repr__(self):
        return '{}([{}, {}, {})'.format(
            self.__class__.__name__,
            repr(self.actor),
            self.interval.lower_bound,
            self.interval.upper_bound,
            )

    def __str__(self):
        return 'Action {} on {}'.format(
            self.__class__.__name__,
            self.actor
            )

    def is_last(self, item):
        if item < self.lower_bound or item > self.upper_bound:
            raise ValueError(
                'El valor cae fuera del intervalo {}'.format(self)
                )
        return item == self.upper_bound
    
    def get_relative_frame(self, frame):
        return frame - self.lower_bound

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
        
    def step(self, frame):
        logger.debug('Action {} called for frame {}'.format(
            self.__class__.__name__,
            frame,
            ))


@register_action
class Blink(Action):
    
    def start(self, frame):
        self.src_color = self.actor.color
        self.inv_color = self.actor.color.inverse()

    def step(self, frame): 
        self.actor.color = self.src_color if frame % 2 else self.inv_color

    def end(self, frame):
        self.actor.color = self.src_color


@register_action
class FadeOut(Action):

    def __init__(self, actor, from_frame, to_frame):
        super().__init__(actor, from_frame, to_frame)
        self.initial_alpha = self.actor.alpha
        self.delta_alpha = self.initial_alpha / self.num_steps

    def step(self, frame):
        self.actor.alpha -= self.delta_alpha

    def end(self, frame):
        self.actor.alpha = 0.0


@register_action
class FadeIn(Action):

    def __init__(self, actor, from_frame, to_frame):
        super().__init__(actor, from_frame, to_frame)
        self.initial_alpha = self.actor.alpha
        self.delta_alpha = (1.0 - self.initial_alpha) / self.num_steps

    def step(self, frame):
        self.actor.alpha += self.delta_alpha

    def end(self, frame):
        self.actor.alpha = 1.0


@register_action
class Exit(Action):

    def start(self, frame):
        self.actor.level = Level.OFF_STAGE


@register_action
class Background(Action):

    def start(self, frame):
        self.actor.level = Level.ON_BACKGROUND


@register_action
class Foreground(Action):

    def start(self, frame):
        self.actor.level = Level.ON_FOREGROUND


class MoveAction(Action):

    def __init__(self, actor, from_frame, to_frame, new_position):
        super().__init__(actor, from_frame, to_frame)
        self.new_position = new_position
        if isinstance(self.new_position, tuple):
            x, y = self.new_position
            self.new_position = Vector(x, y)

    def start(self, frame):
        super().start(frame)
        self.initial_position = copy(self.actor.pos)
        self.change_value = self.new_position - self.initial_position

    def end(self, frame):
        self.actor.pos = self.new_position

@register_action
class Enter(MoveAction):

    def step(self, frame):
        self.actor.pos = self.new_position
        self.actor.level = Level.ON_STAGE


@register_action
class Move(MoveAction):

    def start(self, frame):
        super().start(frame)
        self.delta = self.change_value / self.num_steps

    def step(self, frame):
        super().step(frame)
        t = self.get_relative_frame(frame) 
        self.actor.pos = self.initial_position + self.delta * t


@register_action
class Fall(MoveAction):
    
    def step(self, frame):
        logger.info('Fall {} step({})'.format(self.actor, frame))
        relative_frame = self.get_relative_frame(frame)
        t = relative_frame / self.num_steps
        self.actor.pos = Vector(
            x = self.change_value.x * t**2 + self.initial_position.x,
            y = self.change_value.y * t**2 + self.initial_position.y,
            )


@register_action
class Land(MoveAction):
    
    def step(self, frame):
        relative_frame = self.get_relative_frame(frame)
        t = relative_frame / self.num_steps
        self.actor.pos = Vector(
            x = -self.change_value.x * t * (t-2) + self.initial_position.x,
            y = -self.change_value.y * t * (t-2) + self.initial_position.y,
            )


@register_action
class EaseIn(MoveAction):
    
    def step(self, frame):
        logger.info('EasingIn {} step({})'.format(self.actor, frame))
        relative_frame = self.get_relative_frame(frame)
        t = relative_frame / self.num_steps
        self.actor.pos = Vector(
            x = self.change_value.x * t**3 + self.initial_position.x,
            y = self.change_value.y * t**3 + self.initial_position.y,
            )


@register_action
class EaseOut(MoveAction):
    
    def step(self, frame):
        logger.info('EasingIn {} step({})'.format(self.actor, frame))
        relative_frame = self.get_relative_frame(frame)
        t = relative_frame / self.num_steps
        t -= 1
        self.actor.pos = Vector(
            x = self.change_value.x * (t**3 + 1) + self.initial_position.x,
            y = self.change_value.y * (t**3 + 1) + self.initial_position.y,
            )


@register_action
class Swing(MoveAction):
    
    def step(self, frame):
        logger.info('EasingIn {} step({})'.format(self.actor, frame))
        relative_frame = self.get_relative_frame(frame)
        t = relative_frame / (self.num_steps / 2)
        if t < 1:
            self.actor.pos = Vector(
                x = self.change_value.x / 2 * t**3 + self.initial_position.x,
                y = self.change_value.y / 2 * t**3 + self.initial_position.y,
                )
        else:
            t -= 2
            self.actor.pos = Vector(
                x = self.change_value.x / 2 * (t**3 + 2) + self.initial_position.x,
                y = self.change_value.y / 2 * (t**3 + 2) + self.initial_position.y,
                )

@register_action
class Timer(Action):

    FPS = 25

    def start(self, frame):
        self.actor.text = '00:00.00'

    def step(self, frame):
        self.actor.text = '{mins:02d}:{secs:02d}.{frac:02d}'.format(
            mins = frame // (60*Timer.FPS),  # 60 s/frame * 25 frame/s
            secs = frame // Timer.FPS,
            frac = frame % Timer.FPS,
            )
        
def create_action(action_name, actor, from_frame, to_frame, *args):
    global _map_actions

    buff = ['called create_action("{}", {}, {}, {}'.format(
        action_name,
        actor,
        from_frame,
        to_frame,
        )]
    for _ in args:
        buff.append(', {}'.format(_))
    buff.append(')')
    logger.info(''.join(buff))

    key = action_name.lower()
    if key not in _map_actions:
        raise ValueError('No existe la acción {}'.format(action_name))
    ActionKlass = _map_actions[key]
    action = ActionKlass(actor, from_frame, to_frame, *args)
    return action


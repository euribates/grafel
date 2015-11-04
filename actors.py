#!/usr/bni/env python3

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import re
import sys
import math
from copy import copy
import pprint
import logging
from collections import defaultdict
from vectors import Vector, origin, zero
from colors import Color

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(stream=sys.stderr)
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
    ))
logger.addHandler(ch)

class State:

    def __init__(self, pos=None, color='', scale=None, alpha=1.0):
        self.pos = pos or Vector(0, 0)
        self._color = Color(color) if color else Color('white')
        self.scale = scale or Vector(1, 1)
        self.alpha = alpha

    def set_color(self, color):
        if isinstance(color, Color):
            self._color = color
        else:
            self._color = Color(color)

    def get_color(self):
        return self._color

    color = property(get_color, set_color)

    def __repr__(self):
        return 'State({}, "{}", {}, {})'.format(
            repr(self.pos),
            repr(self._color),
            repr(self.scale),
            repr(self.alpha)
            )

    def __str__(self):
        return 'State[pos:{}|color:{}|scale={}|alpha:{}]'.format(
            self.pos,
            self.color,
            self.scale,
            self.alpha,
            )

    def delta(self, **kwargs):
        logger.info('delta method called')
        logger.info('delta method kwargs: {}'.format(kwargs.keys()))
        d_pos = kwargs.pop('pos', None)
        color = kwargs.pop('color', '')
        scale = kwargs.pop('scale', '')
        alpha = kwargs.pop('alpha', None)
        if d_pos:
            self.pos += d_pos
        if color:
            self.color = color
        if scale:
            self.scale.x *= scale.x
            self.scale.y *= scale.y
        if alpha is not None:
            self.alpha = alpha


class Actor():
    
    def __init__(self, name, state=None):
        self.name = name
        if state:
            self.initial_state = copy(state)
        else:
            self.initial_state = State()
        self.vertexs = []
        self.actions = defaultdict(list) 
        self.active_actions = []
        self.sons = []
        self.parent = None
        self.reset()
        self.text = ''

    def get_offset(self):
        return self.parent.state.pos if self.parent else zero

    def add_son(self, actor):
        actor.parent = self
        self.sons.append(actor)

    def reset(self):
        self.frame = 0
        self.state = copy(self.initial_state)
        self.actions_called = False
        for son in self.sons:
            son.reset()

    def __repr__(self):
        return '{}("{}", {})'.format(
            self.__class__.__name__,
            self.name,
            repr(self.state),
            )

    def __str__(self):
        return '{} {}'.format(
            self.__class__.__name__,
            self.name
            )

    def dump(self, num_frames=15):
        buff = ['--[{}]----------------------'.format(self)]
        buff.append(' - State: {}'.format(self.state))
        buff.append(' - N of sons: {}'.format(len(self.sons)))
        buff.append(' - Timeline')
        buff.append('''\
Frame  N Active actions                                     X     Y
------ - -------------------------------------------------- ----- -----
''')
        self.reset()
        for frame in range(0, num_frames):
            self.call_actions_on_frame(frame)
            new_actions = frame in self.actions
            buff.append('{:-6d} {} {:50} {:5.0f} {:5.0f}'.format(
                frame,
                '*' if new_actions else ' ',
                ', '.join([str(_) for _ in self.active_actions]),
                self.state.pos.x,
                self.state.pos.y,
                ))
            self.next()
        return '\n'.join(buff)

    def place(self, x, y):
        self.state.pos = Vector(x, y)
        self.initial_state.pos = Vector(x, y)

    def add_action(self, frame, action):
        self.actions[frame].append(action)

    def call_actions_on_frame(self, frame):
        #logger.info('actor {} execute call_actions_on_frame({})'.format(
        #    self, frame
        #    ))
        if frame in self.actions:
            for a in self.actions[frame]:
                a.start(self.frame)
                self.active_actions.append(a)
        actions_to_remove = []
        for a in self.active_actions:
            data = a(self.frame)
            if data:
                self.state.delta(**data)
            if a.interval.is_last(self.frame):
                actions_to_remove.append(a)
                a.end(self.frame)
        for a in actions_to_remove:
            self.active_actions.remove(a)
        self.actions_called = True

    def next(self):
        if not self.actions_called:
            self.call_actions_on_frame(self.frame)
            for son in self.sons:
                son.call_actions_on_frame(self.frame)
        self.frame += 1
        self.actions_called = False

    def get_color(self):
        return self.state.color

    def set_color(self, color):
        if isinstance(color, Color):
            self.state.color = color
            self.initial_state.color = color
        else:
            self.state.color = Color(color)
            self.initial_state.color = Color(color)

    color = property(get_color, set_color)
    

class Circle(Actor):
    def __init__(self, name, state=None, radius=50):
        super().__init__(name, state=state)
        for i in range(36):
            angle = i * math.pi / 18
            v = Vector(math.sin(angle)*radius, math.cos(angle)*radius)
            self.vertexs.append(v)
        self.size = Vector(radius*2, radius*2)


class Path(Actor):

    def __init__(self, name, state=None, radius=50):
        super().__init__(name, state=state)
    

class Text(Actor):
    
    def __init__(self, name, state=None, text=''):
        super().__init__(name, state)
        self.text = text or self.name


class Star(Actor):
    def __init__(self, name, state=None, radius=50):
        super().__init__(name, state=state)
        self.size = Vector(radius*2, radius*2)
        for angle in (36, 108, 180, 252, 324):
            r = angle * math.pi / 180.0
            self.vertexs.append(
                Vector(math.sin(r)*radius, math.cos(r)*radius)
                )
        r = 72. * math.pi / 180.0
        self.vertexs.insert(1, 
            Vector(math.sin(r)*radius/2.0, math.cos(r)*radius/2.0)
            ) 
        r = 144. * math.pi / 180.0
        self.vertexs.insert(3, 
            Vector(math.sin(r)*radius/2.0, math.cos(r)*radius/2.0)
            ) 
        r = 216. * math.pi / 180.0
        self.vertexs.insert(5, 
            Vector(math.sin(r)*radius/2.0, math.cos(r)*radius/2.0)
            ) 
        r = 288. * math.pi / 180.0
        self.vertexs.insert(7, 
            Vector(math.sin(r)*radius/2.0, math.cos(r)*radius/2.0)
            ) 
        self.vertexs.insert(9, Vector(0, radius/2.0)) 


class Square(Actor):

    def __init__(self, name, state=None, width=50, height=50):
        super().__init__(name, state=state)
        self.size = Vector(width, height)
        ww = width // 2
        hh = height // 2
        self.vertexs.append(Vector(-ww, -hh))
        self.vertexs.append(Vector(ww, -hh))
        self.vertexs.append(Vector(ww, hh))
        self.vertexs.append(Vector(-ww, hh))

class RoundSquare(Actor):
    def __init__(self, name, state=None, width=50, height=50):
        super().__init__(name, state)
        if width < 20:
            width = 20
        if height < 20:
            height = 20

        offset = Vector(width // 2, height // 2)

        self.size = Vector(width, height)

        self.vertexs.append(Vector(10, 0)-offset)
        self.vertexs.append(Vector(self.size.x-10, 0)-offset)

        self.vertexs.append(Vector(self.size.x-6, 1)-offset)
        self.vertexs.append(Vector(self.size.x-3, 3)-offset)
        self.vertexs.append(Vector(self.size.x-1, 6)-offset)

        self.vertexs.append(Vector(self.size.x, 10)-offset)
        self.vertexs.append(Vector(self.size.x, self.size.y-10)-offset)

        self.vertexs.append(Vector(self.size.x-1, self.size.y-6)-offset)
        self.vertexs.append(Vector(self.size.x-3, self.size.y-3)-offset)
        self.vertexs.append(Vector(self.size.x-6, self.size.y-1)-offset)

        self.vertexs.append(Vector(self.size.x-10, self.size.y)-offset)
        self.vertexs.append(Vector(10, self.size.y)-offset)

        self.vertexs.append(Vector(6, self.size.y-1)-offset)
        self.vertexs.append(Vector(3, self.size.y-3)-offset)
        self.vertexs.append(Vector(1, self.size.y-6)-offset)

        self.vertexs.append(Vector(0, self.size.y-10)-offset)
        self.vertexs.append(Vector(0, 10)-offset)
        
        self.vertexs.append(Vector(1, 6)-offset)
        self.vertexs.append(Vector(3, 3)-offset)
        self.vertexs.append(Vector(6, 1)-offset)


class Dice(Actor):
    def __init__(self, name, state=None, width=50, height=50, num=1):
        super().__init__(name, state=state)
        self.size = Vector(width, height)
        border = RoundSquare('dice.border', 
            state=State(pos=zero, color='ghostgray'),
            width=width,
            height=height
            )
        self.add_son(border)
        r = width // 10
        if num == 1:
            dot1 = Circle('dice.dot1', 
                state=State(pos=Vector(0, 0), color='dimgray'),
                radius = width // 5,
                )
            self.add_son(dot1)
        elif num == 2:
            dot1 = Circle('dice.dot1', 
                state=State(pos=Vector(0, -height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot1)
            dot2 = Circle('dice.dot2', 
                state=State(pos=Vector(0, height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot2)
        elif num == 3:
            dot1 = Circle('dice.dot1', 
                state=State(pos=Vector(width//4, -height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot1)

            dot2 = Circle('dice.dot2', 
                state=State(pos=zero, color='dimgray'),
                radius = r,
                )
            self.add_son(dot2)

            dot3 = Circle('dice.dot3', 
                state=State(pos=Vector(-width//4, height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot3)
        elif num == 4:
            dot1 = Circle('dice.dot1', 
                state=State(pos=Vector(-width//4, -height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot1)

            dot2 = Circle('dice.dot2', 
                state=State(pos=Vector(width//4, -height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot2)

            dot3 = Circle('dice.dot3', 
                state=State(pos=Vector(-width//4, height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot3)

            dot4 = Circle('dice.dot4', 
                state=State(pos=Vector(width//4, height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot4)

        elif num == 5:
            dot1 = Circle('dice.dot1', 
                state=State(pos=Vector(-width//4, -height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot1)

            dot2 = Circle('dice.dot2', 
                state=State(pos=Vector(width//4, -height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot2)

            dot3 = Circle('dice.dot3', 
                state=State(pos=Vector(-width//4, height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot3)

            dot4 = Circle('dice.dot4', 
                state=State(pos=Vector(width//4, height//4), color='dimgray'),
                radius = r,
                )
            self.add_son(dot4)

            dot5 = Circle('dice.dot5', 
                state=State(pos=zero, color='dimgray'),
                radius = r,
                )
            self.add_son(dot5)

        elif num == 6:
            dot1 = Circle('dice.dot1', 
                state=State(pos=Vector(-width//4, -height//3), color='dimgray'),
                radius = r,
                )
            self.add_son(dot1)

            dot2 = Circle('dice.dot2', 
                state=State(pos=Vector(-width//4, 0), color='dimgray'),
                radius = r,
                )
            self.add_son(dot2)

            dot3 = Circle('dice.dot3', 
                state=State(pos=Vector(-width//4, height//3), color='dimgray'),
                radius = r,
                )
            self.add_son(dot3)

            dot4 = Circle('dice.dot4', 
                state=State(pos=Vector(width//4, -height//3), color='dimgray'),
                radius = r,
                )
            self.add_son(dot4)

            dot5 = Circle('dice.dot5', 
                state=State(pos=Vector(width//4, 0), color='dimgray'),
                radius = r,
                )
            self.add_son(dot5)

            dot6 = Circle('dice.dot6', 
                state=State(pos=Vector(width//4, height//3), color='dimgray'),
                radius = r,
                )
            self.add_son(dot6)





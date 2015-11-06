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
from colors import Color, black, white

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
ch = logging.StreamHandler(stream=sys.stderr)
ch.setLevel(logging.WARNING)
ch.setFormatter(logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s'
    ))
logger.addHandler(ch)


class State:

    def __init__(self, **kwargs):
        self.pos = kwargs.pop('pos', zero)
        if isinstance(self.pos, tuple):
            self.pos = Vector(self.pos[0], self.pos[1])
        self.color = kwargs.pop('color', white)
        self.scale = kwargs.pop('scale', Vector(1, 1))
        self.alpha = kwargs.pop('alpha', 1.0)

    def set_color(self, color):
        if isinstance(color, Color):
            self._color = color
        else:
            self._color = Color(color)

    def get_color(self):
        return self._color

    color = property(get_color, set_color)

    def __repr__(self):
        return 'State({}, {}, {}, {})'.format(
            repr(self.pos),
            repr(self._color),
            repr(self.scale),
            repr(self.alpha),
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
        if d_pos is not None:
            self.pos += d_pos
        color = kwargs.pop('color', None)
        if color is not None:
            self.color = color
        scale = kwargs.pop('scale', None)
        if scale is not None:
            self.scale.x *= scale.x
            self.scale.y *= scale.y
        alpha = kwargs.pop('alpha', None)
        if alpha is not None:
            self.alpha = alpha




class Actor():
    
    def __init__(self, name, **kwargs):
        self.name = name 
        self.actions = defaultdict(list) 
        self.active_actions = []
        self.sons = []
        self.parent = None
        self.initial_state = State(**kwargs)
        self.reset()

    def get_pos(self):
        return self.state.pos

    def set_pos(self, new_pos):
        if isinstance(new_pos, tuple):
            new_pos = Vector(new_pos[0], new_pos[1])
        self.state.pos = new_pos

    pos = property(get_pos, set_pos)

    def get_color(self):
        return self.state.color

    def set_color(self, color):
        self.state.color = color

    color = property(get_color, set_color)

    def get_scale(self):
        return self.state.scale

    def set_scale(self, new_scale):
        self.state.scale = new_scale

    scale = property(get_scale, set_scale)

    def get_alpha(self):
        return self.state.alpha

    def set_alpha(self, new_alpha):
        self.state.alpha = new_alpha

    alpha = property(get_alpha, set_alpha)

    def get_offset(self):
        if self.parent:
            return self.parent.get_offset() + self.parent.pos 
        else:
            return zero 

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
        self.pos = Vector(x, y)
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

    def start_draw(self, engine):
        for son in self.sons:
            son.start_draw(engine)
        self.draw(engine)

class Rect(Actor):

    def __init__(self, name, size=Vector(50, 50), **kwargs):
        super().__init__(name, **kwargs)
        (self.width, self.height) = self.size = size

    def draw(self, engine):
        pos = self.pos + self.get_offset()
        engine.rect(pos.x, pos.y, self.width, self.height,
            color=self.color,
            alpha=self.alpha,
            )

class Square(Actor):

    def __init__(self, name, side=50, **kwargs):
        super().__init__(name, **kwargs)
        self.width = self.height = side

    def draw(self, engine):
        pos = self.pos + self.get_offset()
        engine.rect(pos.x, pos.y, self.width, self.height,
            color=self.color,
            alpha=self.alpha,
            )

class Circle(Actor):

    def __init__(self, name, radius=50, **kwargs):
        super().__init__(name, **kwargs)
        self.radius = radius

    def draw(self, engine):
        pos = self.pos + self.get_offset()
        engine.circle(pos.x, pos.y, self.radius,
            color=self.color,
            alpha=self.alpha,
            )


class Polygon(Actor):

    def __init__(self, name, points=None, **kwargs):
        super().__init__(name, **kwargs)  
        self.points = points or []
 
    def draw(self, engine):
        pos = self.pos + self.get_offset()
        engine.polygon(pos.x, pos.y, self.points,
            color=self.color,
            alpha=self.alpha,
            )

class Triangle(Polygon):
    def __init__(self, name, a, b, c, **kwargs):
        super().__init__(name, **kwargs)    
        if isinstance(a, tuple):
            a = Vector(a[0], a[1])
        if isinstance(b, tuple):
            b = Vector(b[0], b[1])
        if isinstance(c, tuple):
            c = Vector(c[0], c[1])
        self.points = [a, b, c]



class Path(Actor):

    def __init__(self, name, state=None, radius=50):
        super().__init__(name, state=state)
    

class Text(Actor):
    
    def __init__(self, name, state=None, text=''):
        super().__init__(name, state)
        self.text = text or self.name


class Star(Polygon):

    def __init__(self, name, radius=100, **kwargs):
        super().__init__(name, **kwargs)
        
        x, y = 0, -radius
        self.points = []
        for i in range(1, 10):
            a = i * math.pi / 5
            r = radius/2.5 if i % 2 else radius
            new_x = math.sin(a) * r
            new_y = -math.cos(a) * r
            self.points.append(Vector(new_x - x, new_y - y))
            x = new_x 
            y = new_y






class RoundSquare(Polygon):
    def __init__(self, name, width=50, height=50, **kwargs):
        super().__init__(name, **kwargs)
        if width < 20:
            width = 20
        if height < 20:
            height = 20

        offset = Vector(width // 2, height // 2)

        self.size = Vector(width, height)

        self.points.append(Vector(10, 0))
        self.points.append(Vector(width-10, 0))

        self.points.append(Vector(-6, 1))
        self.points.append(Vector(-3, 3))
        self.points.append(Vector(-1, 6))

        self.points.append(Vector(0, 10))
        self.points.append(Vector(0, height-10))

        self.points.append(Vector(-1, -6))
        self.points.append(Vector(-3, -3))
        self.points.append(Vector(-6, -1))

        self.points.append(Vector(-width+10, 0))
        self.points.append(Vector(10, 0))

        self.points.append(Vector(6, -1))
        self.points.append(Vector(3, -3))
        self.points.append(Vector(1, -6))

        self.points.append(Vector(0, -10))
        self.points.append(Vector(0, 10))
        
        self.points.append(Vector(1, 6))
        self.points.append(Vector(3, 3))
        self.points.append(Vector(6, 1))


class Dice(Actor):
    def __init__(self, name, num=1, width=50, height=50, **kwargs):
        super().__init__(name, **kwargs)
        self.num = num
        self.width, self.height = (width, height)
        self.size = Vector(width, height)
        border = Square('dice.border', 
            color='ghostgray',
            width=width,
            height=height
            )
        self.add_son(border)
        r = width // 10
        if num == 1:
            dot1 = Circle('dice.dot1', 
                pos=Vector(0, 0),
                color='dimgray',
                radius = width // 5,
                )
            self.add_son(dot1)
        elif num == 2:
            dot1 = Circle('dice.dot1', 
                pos=Vector(0, -height//4), 
                color='dimgray',
                radius = r,
                )
            self.add_son(dot1)
            dot2 = Circle('dice.dot2', 
                pos=Vector(0, height//4),
                color='dimgray',
                radius = r,
                )
            self.add_son(dot2)
        elif num == 3:
            dot1 = Circle('dice.dot1', 
                pos=Vector(width//4, -height//4), color='dimgray',
                radius = r,
                )
            self.add_son(dot1)

            dot2 = Circle('dice.dot2', 
                pos=zero, color='dimgray',
                radius = r,
                )
            self.add_son(dot2)

            dot3 = Circle('dice.dot3', 
                pos=Vector(-width//4, height//4), color='dimgray',
                radius = r,
                )
            self.add_son(dot3)
        elif num == 4:
            dot1 = Circle('dice.dot1', 
                pos=Vector(-width//4, -height//4), color='dimgray',
                radius = r,
                )
            self.add_son(dot1)

            dot2 = Circle('dice.dot2', 
                pos=Vector(width//4, -height//4), color='dimgray',
                radius = r,
                )
            self.add_son(dot2)

            dot3 = Circle('dice.dot3', 
                pos=Vector(-width//4, height//4), color='dimgray',
                radius = r,
                )
            self.add_son(dot3)

            dot4 = Circle('dice.dot4', 
                pos=Vector(width//4, height//4), color='dimgray',
                radius = r,
                )
            self.add_son(dot4)

        elif num == 5:
            dot1 = Circle('dice.dot1', 
                pos=Vector(-width//4, -height//4), color='dimgray',
                radius = r,
                )
            self.add_son(dot1)

            dot2 = Circle('dice.dot2', 
                pos=Vector(width//4, -height//4), color='dimgray',
                radius = r,
                )
            self.add_son(dot2)

            dot3 = Circle('dice.dot3', 
                pos=Vector(-width//4, height//4), color='dimgray',
                radius = r,
                )
            self.add_son(dot3)

            dot4 = Circle('dice.dot4', 
                pos=Vector(width//4, height//4), color='dimgray',
                radius = r,
                )
            self.add_son(dot4)

            dot5 = Circle('dice.dot5', 
                pos=zero, color='dimgray',
                radius = r,
                )
            self.add_son(dot5)

        elif num == 6:
            dot1 = Circle('dice.dot1', 
                pos=Vector(-width//4, -height//3), color='dimgray',
                radius = r,
                )
            self.add_son(dot1)

            dot2 = Circle('dice.dot2', 
                pos=Vector(-width//4, 0), color='dimgray',
                radius = r,
                )
            self.add_son(dot2)

            dot3 = Circle('dice.dot3', 
                pos=Vector(-width//4, height//3), color='dimgray',
                radius = r,
                )
            self.add_son(dot3)

            dot4 = Circle('dice.dot4', 
                pos=Vector(width//4, -height//3), color='dimgray',
                radius = r,
                )
            self.add_son(dot4)

            dot5 = Circle('dice.dot5', 
                pos=Vector(width//4, 0), color='dimgray',
                radius = r,
                )
            self.add_son(dot5)

            dot6 = Circle('dice.dot6', 
                pos=Vector(width//4, height//3), color='dimgray',
                radius = r,
                )
            self.add_son(dot6)

    def draw(self, engine):
        pass

def create_actor(name, rol, **kwargs):
    print('create_actor({}, {}, {})'.format(
        name, rol, kwargs))
    state = State()
    state.pos = kwargs.pop('pos', state.pos)
    state.color = kwargs.pop('color', state.color)
    state.scale = kwargs.pop('scale', state.scale)
    state.alpha = kwargs.pop('alpha', state.alpha)
    
    print('state', state)
    print('rest_of_options', rest_of_options) 
    if rol == 'Square':
        return Square(name, state, **rest_of_options)
    elif rol == 'Star':
        return Star(name, state, **rest_of_options)




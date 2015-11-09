#!/usr/bni/env python3

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import six
import re
import sys
import math
from copy import copy
import pprint
import logging
from collections import defaultdict
from vectors import Vector, origin, zero
from colors import Color, black, white
import logs


logger = logs.create(__name__)

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

    def get_color(self): return self.state.color
    def set_color(self, new_color): self.state.color = new_color

    color = property(get_color, set_color)

    def get_scale(self): return self.state.scale
    def set_scale(self, new_scale): self.state.scale = new_scale

    scale = property(get_scale, set_scale)

    def get_alpha(self): return self.state.alpha
    def set_alpha(self, new_alpha): self.state.alpha = new_alpha

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


    def place(self, x, y):
        self.pos = Vector(x, y)
        self.initial_state.pos = Vector(x, y)

    def start_draw(self, engine):
        self.draw(engine)
        for son in self.sons:
            son.start_draw(engine)

    def draw(self, engine):
        raise NotImplementedError(
            'La clase {} debe definir su método draw'.format(
                self.__class__.__name__
                )
            )

class Rect(Actor):

    def __init__(self, name, width=50, height=50, **kwargs):
        super().__init__(name, **kwargs)
        self.width = width
        self.height = height
        self.size = (self.width, self.height)

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


class RoundRect(Actor):

    def __init__(self, name, width=50, height=50, **kwargs):
        super().__init__(name, **kwargs)
        self.width = int(width) if width > 20 else 20
        self.height = int(height) if height > 20 else 20
        self.size = Vector(self.width, self.height)
        if 'border_radius' in kwargs:
            self.border_radius = kwargs['border_radius'] 
        else:
            self.border_radius = int(round(min(self.width, self.height) // 12))

    def draw(self, engine):
        pos = self.pos + self.get_offset()
        engine.roundrect(
            pos.x, pos.y, self.width, self.height, 
            self.border_radius,
            color=self.color,
            alpha=self.alpha,
            )

class Dice(RoundRect):

    def __init__(self, name, num=1, side=50, **kwargs):
        super().__init__(name, width=side, height=side, **kwargs)
        self.num = num
        self.side = side
        self.dot_color = self.color.inverse()
        x1q = self.width // 4 ; y1q = self.height // 4
        x2q = x1q + x1q       ; y2q = y1q + y1q
        x3q = 3 * x1q         ; y3q = 3 * y1q
        default_dot_radius = self.width // 10
        if num == 1:
            self.add_dot(Vector(x2q, y2q), r=2*default_dot_radius)
        elif num == 2:
            self.add_dot(Vector(x2q, y1q))
            self.add_dot(Vector(x2q, y3q))
        elif num == 3:
            self.add_dot(Vector(x3q, y1q))
            self.add_dot(Vector(x2q, y2q))
            self.add_dot(Vector(x1q, y3q))
        elif num == 4:
            self.add_dot(Vector(x1q, y1q))
            self.add_dot(Vector(x3q, y1q))
            self.add_dot(Vector(x1q, y3q))
            self.add_dot(Vector(x3q, y3q))
        elif num == 5:
            self.add_dot(Vector(x1q, y1q))
            self.add_dot(Vector(x3q, y1q))
            self.add_dot(Vector(x1q, y3q))
            self.add_dot(Vector(x3q, y3q))
            self.add_dot(Vector(x2q, y2q))
        elif num == 6:
            y1 = self.side // 5 
            y2 = y2q
            y3 = 4 * y1
            self.add_dot(Vector(x1q, y1))
            self.add_dot(Vector(x1q, y2))
            self.add_dot(Vector(x1q, y3))
            self.add_dot(Vector(x3q, y1))
            self.add_dot(Vector(x3q, y2))
            self.add_dot(Vector(x3q, y3))

    def add_dot(self, pos, r=None):
        if hasattr(self.add_dot, '_counter'):
            self._dot_counter += 1
        else:
            setattr(self, '_dot_counter', 1)
        radius = r if r else self.side // 10
        name = '{}.dot{}'.format(self.name, self._dot_counter)
        new_dot = Circle(name, radius=radius,
            pos=pos,
            color=self.dot_color,
            alpha=self.alpha,
            )
        self.add_son(new_dot)


class Label(Actor):
    
    def __init__(self, name, text, **kwargs):
        if six.PY2:
            super(Label, self).__init__(name, **kwargs)
        else:
            super().__init__(name, **kwargs)
        self.text = text
        self.font_size = kwargs.get('fontsize', 31)

        scale = 90/72.  # 90dpi / 72 points in one inch
        self.height = self.font_size * scale
        self.width = len(text) * self.height / 2.0
        self.border = RoundRect('{}.border'.format(self.name),
            width=self.width,
            height=self.height,
            color=self.color.inverse(),
            pos=(0,0)
            )

    def draw(self, engine):
        
        #width-offwet = self.pos.x 
        engine.circle(self.pos.x, self.pos.y, 3, color='green') 
        self.border.pos.x = self.pos.x - self.width//2
        self.border.pos.y = self.pos.y
        self.border.draw(engine)

        engine.text(self.pos.x, self.pos.y, self.text,
            color=self.color,
            alpha=self.alpha,
            )

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




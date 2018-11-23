#!/usr/bni/env python3

import math

from vectors import Vector, zero
import colors
from colors import Color, white
import logs
from enum import IntEnum
import fileutils

logger = logs.create(__name__)


class Level(IntEnum):
    OFF_STAGE = 0
    ON_BACKGROUND = 1
    ON_STAGE = 2
    ON_FOREGROUND = 3


class Actor():

    def _save_state(self, **kwargs):
        result = {
            'pos': self._pos,
            'color': self._color,
            'alpha': self.alpha,
            'scale': self.scale,
            'level': self.level,
            'debug': self.debug,
            }
        for k in kwargs:
            result[k] = kwargs[k]
        return result

    def _load_state(self, state):
        for k in state:
            setattr(self, k, state[k])

    def __init__(self, name, **kwargs):
        self.name = name
        self.level = Level.ON_STAGE if 'pos' in kwargs else Level.OFF_STAGE
        self._pos = kwargs.pop('pos', zero)
        if isinstance(self._pos, tuple):
            self._pos = Vector(self.pos[0], self.pos[1])
        self._color = kwargs.pop('color', Color('silver'))
        if isinstance(self._color, str):
            self._color = Color(self.color)
        self.scale = kwargs.pop('scale', Vector(1, 1))
        self.alpha = kwargs.pop('alpha', 1.0)
        self.sons = []
        self.parent = None
        self.debug = False
        self.initial_state = self._save_state()
        self.reset()

    def reset(self):
        self.frame = 0
        self._load_state(self.initial_state)
        for son in self.sons:
            son.reset()

    def get_pos(self):
        return self._pos

    def set_pos(self, new_pos):
        if isinstance(new_pos, tuple):
            new_pos = Vector(new_pos[0], new_pos[1])
        self._pos = new_pos

    pos = property(get_pos, set_pos)

    def get_color(self):
        return self._color

    def set_color(self, new_color):
        if isinstance(new_color, str):
            new_color = Color(new_color)
        self._color = new_color

    color = property(get_color, set_color)

    def get_offset(self):
        if self.parent:
            return self.parent.get_offset() + self.parent.pos
        else:
            return zero

    def add_son(self, actor):
        actor.parent = self
        self.sons.append(actor)

    def __repr__(self):
        return '{}("{}", pos={}, color="{}")'.format(
            self.__class__.__name__,
            self.name,
            self.pos,
            self.color,
            )

    def __str__(self):
        return 'Actor {nom} as {rol}'.format(
            rol=self.__class__.__name__,
            nom=self.name
            )

    def place(self, x, y):
        self.initial_state['pos'] = self.pos = Vector(x, y)
        self.initial_state['level'] = self.level = Level.ON_STAGE

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

    def spot_center(self, engine):
        pos = self.get_offset() + self.pos
        engine.line(pos.x, pos.y-15, pos.x, pos.y+15, color='red')
        engine.line(pos.x-15, pos.y, pos.x+15, pos.y, color='red')
        engine.polygon(pos.x, pos.y-5, [
            (5, 5), (-5, 5), (-5, -5)
            ], alpha=0.5)


class Square(Actor):

    def __init__(self, name, side=50, **kwargs):
        super().__init__(name, **kwargs)
        self.width = self.height = side

    def draw(self, engine):
        pos = self.pos + self.get_offset()
        x = pos.x - self.width / 2
        y = pos.y - self.height / 2
        engine.rect(
            x, y, self.width, self.height,
            color=self.color,
            alpha=self.alpha,
            )


class Box(Actor):

    def __init__(self, name, width=50, height=50, **kwargs):
        super().__init__(name, **kwargs)
        self.width = width
        self.height = height
        self.size = (self.width, self.height)

    def __str__(self):
        return 'Box {} at {} [width={} heigth={}]'.format(
            self.name,
            self.pos,
            self.width,
            self.height,
            )

    def draw(self, engine):
        pos = self.pos + self.get_offset()
        x = pos.x - self.width / 2
        y = pos.y - self.height / 2
        engine.box(
            x, y, self.width, self.height,
            color=self.color,
            alpha=self.alpha,
            )


class Rect(Actor):

    def __init__(self, name, width=50, height=50, **kwargs):
        super().__init__(name, **kwargs)
        self.width = width
        self.height = height
        self.size = (self.width, self.height)

    def __str__(self):
        return 'Rect {} at {} [width={} heigth={}]'.format(
            self.name,
            self.pos,
            self.width,
            self.height,
            )

    def draw(self, engine):
        pos = self.pos + self.get_offset()
        x = pos.x - self.width / 2
        y = pos.y - self.height / 2
        engine.rect(
            x, y, self.width, self.height,
            color=self.color,
            alpha=self.alpha,
            )


class Circle(Actor):

    def __init__(self, name, radius=50, **kwargs):
        super().__init__(name, **kwargs)
        self.radius = radius

    def draw(self, engine):
        pos = self.pos + self.get_offset()
        engine.circle(
            pos.x, pos.y, self.radius,
            color=self.color,
            alpha=self.alpha,
            )


class Path(Actor):

    def __init__(self, name, points=None, **kwargs):
        super().__init__(name, **kwargs)
        self.points = points[:]
        total = zero
        for p in points:
            total += p
        self.centroid = total / len(points)

    def draw(self, engine):
        p1 = self.points[0]
        for p2 in self.points[1:]:
            engine.line(
                p1.x, p1.y, p2.x, p2.y,
                color=self.color,
                alpha=self.alpha
                )
            p1 = p2


class Polygon(Actor):

    def __init__(self, name, points=None, **kwargs):
        super().__init__(name, **kwargs)
        acc = total = zero
        for p in points:
            acc += p
            total += acc
        self.centroid = total / (len(points) + 1)
        self.points = points or []

    def draw(self, engine):
        pos = self.pos + self.get_offset() - self.centroid
        engine.polygon(
            pos.x, pos.y, self.points,
            color=self.color,
            alpha=self.alpha,
            )


class Triangle(Polygon):
    def __init__(self, name, points=None, **kwargs):
        if not points:
            a = Vector(0, 0)
            b = Vector(50, 25)
            c = Vector(-50, 25)
        else:
            a = points[0]
            if isinstance(a, tuple):
                a = Vector(*a)
            b = points[1]
            if isinstance(b, tuple):
                b = Vector(*b)
            c = points[2]
            if isinstance(c, tuple):
                c = Vector(*c)
        super().__init__(name, points=[b-a, c-b], **kwargs)


class Star(Polygon):

    def __init__(self, name, radius=100, **kwargs):
        x, y = 0, -radius
        points = []
        for i in range(1, 10):
            a = i * math.pi / 5
            r = radius/2.5 if i % 2 else radius
            new_x = math.sin(a) * r
            new_y = -math.cos(a) * r
            points.append(Vector(new_x - x, new_y - y))
            x = new_x
            y = new_y
        super().__init__(name, points=points, **kwargs)


class RoundRect(Actor):

    def __init__(self, name, width=50, height=50, **kwargs):
        super().__init__(name, **kwargs)
        self.width = int(width) if width > 20 else 20
        self.height = int(height) if height > 20 else 20
        self.size = Vector(self.width, self.height)
        if 'radius' in kwargs:
            self.radius = kwargs['radius']
        else:
            self.radius = int(round(min(self.width, self.height) // 12))

    def draw(self, engine):
        pos = self.pos + self.get_offset()
        x = pos.x - self.width / 2
        y = pos.y - self.height / 2
        engine.roundrect(
            x, y, self.width, self.height,
            self.radius,
            color=self.color,
            alpha=self.alpha,
            )


class Dice(RoundRect):

    def __str__(self):
        return 'Dice {} at {} [num:{}]'.format(
            self.name,
            self.pos,
            self.num,
            )

    def __init__(self, name, num=1, side=50, **kwargs):
        super().__init__(name, width=side, height=side, **kwargs)
        self.num = num
        self.side = side
        self.dot_color = self.color.inverse()
        x = self.width // 4
        y = self.height // 4
        default_dot_radius = self.width // 10
        if num == 1:
            self.add_dot(zero, r=2*default_dot_radius)
        elif num == 2:
            self.add_dot(Vector(0, -y))
            self.add_dot(Vector(0, y))
        elif num == 3:
            self.add_dot(Vector(-x, y))
            self.add_dot(Vector(0, 0))
            self.add_dot(Vector(x, -y))
        elif num == 4:
            self.add_dot(Vector(-x, -y))
            self.add_dot(Vector(x, -y))
            self.add_dot(Vector(-x, y))
            self.add_dot(Vector(x, y))
        elif num == 5:
            self.add_dot(Vector(-x, -y))
            self.add_dot(Vector(x, -y))
            self.add_dot(Vector(-x, y))
            self.add_dot(Vector(x, y))
            self.add_dot(Vector(0, 0))
        elif num == 6:
            y = self.side // 4
            self.add_dot(Vector(-x, -y))
            self.add_dot(Vector(-x, 0))
            self.add_dot(Vector(-x, y))
            self.add_dot(Vector(x, -y))
            self.add_dot(Vector(x, 0))
            self.add_dot(Vector(x, y))

    def add_dot(self, pos, r=None):
        if hasattr(self.add_dot, '_counter'):
            self._dot_counter += 1
        else:
            setattr(self, '_dot_counter', 1)
        radius = r if r else self.side // 10
        name = '{}.dot{}'.format(self.name, self._dot_counter)
        new_dot = Circle(
            name, radius=radius,
            pos=pos,
            color=self.dot_color,
            alpha=self.alpha,
            )
        self.add_son(new_dot)


class Text(Actor):

    def __init__(self, name, text='', **kwargs):
        self.text = text or name
        self.font_size = kwargs.pop('fontsize', 32)
        scale = 90/72.  # 90dpi / 72 points in one inch
        self.height = self.font_size * scale
        self.width = len(text) * self.height / 2.0
        super().__init__(name, **kwargs)

    def __str__(self):
        return 'Actor {} as Text [text:"{}"|font_size:{}]'.format(
            self.name,
            self.text,
            self.font_size,
            )

    def draw(self, engine):
        logger.info('Text.draw method called'.format(self.name))
        pos = self.pos + self.get_offset()
        x = pos.x
        y = pos.y
        if self.debug:
            engine.line(x-30, y, x+30, y, color='gold')
            engine.line(x, y-30, x, y+30, color='gold')
        engine.text(
            x, y, self.text,
            color=self.color,
            alpha=self.alpha,
            font_size=self.font_size
            )


class Bitmap(Actor):

    def __init__(self, name, filename, **kwargs):
        super().__init__(name, **kwargs)
        self.width, self.height = fileutils.get_image_size(filename)
        self.filename = filename

    def draw(self, engine):
        engine.bitmap(
            self.pos.x, self.pos.y,
            self.filename,
            alpha=self.alpha,
            )


class Label(RoundRect):

    def __init__(self, name, text='', **kwargs):
        self.font_size = kwargs.pop('fontsize', 32)
        height = kwargs.pop('height', None)
        width = kwargs.pop('width', None)
        color = kwargs.pop('color', white)
        if isinstance(color, str):
            color = colors.Color(color)
        background = kwargs.pop('background', None)
        if isinstance(background, str):
            background = colors.Color(background)
        if not background:
            background = color.inverse()
        self._text = Text(
            '{}.text'.format(name),
            text,
            color=color,
            fontsize=self.font_size,
            pos=(0, 0),
            )
        super().__init__(
            name,
            width=width or self._text.width,
            height=height or self._text.height,
            color=color.inverse(),
            **kwargs
            )
        self.add_son(self._text)

    def set_text(self, text):
        self._text.text = text

    def get_text(self):
        return self._text.text

    text = property(get_text, set_text)

    def draw(self, engine):
        super().draw(engine)
        self._text.draw(engine)


def create_actor(name, role, **kwargs):
    import actors
    buff = ['called create_actor({}, {}'.format(name, role)]
    for k in kwargs:
        buff.append(', {}={}'.format(k, repr(kwargs[k])))
    buff.append(')')
    logger.info(''.join(buff))
    _Klass = getattr(actors, role)
    return _Klass(name, **kwargs)

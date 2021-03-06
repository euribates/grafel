#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# vector.py

import random
import math
from math import sin, cos, atan2, sqrt, pi


MSG_VECTOR_ARGS_WRONG = (
    'El argumento: {} para el constructor de la clase'
    ' Vector no es válido. Esperaba una tupla u otro'
    ' Vector, o dos números'
    )


class Vector(object):

    def __init__(self, *args):
        argc = len(args)
        if argc == 0:
            self.x = self.y = 0
        elif argc == 1:
            arg = args[0]
            if isinstance(arg, tuple):
                self.x, self.y = arg
            elif isinstance(arg, self.__class__):
                self.x, self.y = arg.x, arg.y
            else:
                raise ValueError(MSG_VECTOR_ARGS_WRONG.format(arg))
        elif argc == 2:
            self.x, self.y = float(args[0]), float(args[1])
        else:
            raise ValueError(MSG_VECTOR_ARGS_WRONG.format(args))

    width = property(lambda self: self.x)
    height = property(lambda self: self.y)

    def __str__(self):
        return 'Vector({:.3f}, {:.3f})'.format(self.x, self.y)

    __repr__ = __str__

    def _get_theta(self):
        return atan2(self.y, self.x)

    def _set_theta(self, v):
        m = self.mod
        self.x = round(m * cos(v), 9)
        self.y = round(m * sin(v), 9)

    theta = property(_get_theta, _set_theta)

    def _get_mod(self):
        return sqrt(self.x**2 + self.y**2)

    def _set_mod(self, v):
        angle = self.theta
        self.x = round(cos(angle) * v, 9)
        self.y = round(sin(angle) * v, 9)

    mod = property(_get_mod, _set_mod)

    def as_tuple(self):
        return (
            int(round(self.x)),
            int(round(self.y)),
            )

    def __add__(self, op2):
        if isinstance(op2, tuple):
            op2 = Vector(op2[0], op2[1])
        return Vector(self.x + op2.x, self.y + op2.y)

    def __sub__(self, op2):
        if isinstance(op2, tuple):
            op2 = Vector(op2[0], op2[1])
        return Vector(self.x - op2.x, self.y - op2.y)


    def __mul__(self, op2):
        return Vector(self.x * op2, self.y * op2)

    def __truediv__(self, op2):
        return Vector(self.x / op2, self.y / op2)

    def __div__(self, op2): # Python 2 campatibility
        return type(self).__truediv__(self, op2) 

    def __floordiv__(self, op2):
        return Vector(self.x // op2, self.y // op2)

    def __eq__(self, op2):
        if isinstance(op2, tuple):
            x, y = op2
        else:
            x = op2.x
            y = op2.y
        return round(self.x, 6) == round(x, 6)  \
           and round(self.y, 6) == round(y, 6)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == 0:
            self._index = 1
            return int(round(self.x))
        elif self._index == 1:
            self._index = 2
            return int(round(self.y))
        else:
            raise StopIteration

    def __getitem__(self, index):
        if index == 0:
            return int(round(self.x))
        elif index == 1:
            return int(round(self.y))
        else:
            raise KeyError('El índice {} no es correcto'.format(index))

    def __len__(self):
        return 2

    def __copy__(self):
        return Vector(self.x, self.y)



def get_random_position_vector(width=100, height=100):
    return Vector(
        random.randrange(0, width),
        random.randrange(0, height),
        )

def get_random_unitary_vector():
    angle = random.uniform(0, 2* pi)
    return Vector(cos(angle), sin(angle))

zero = origin = Vector(0, 0)
up = Vector(0, -1)
down = Vector(0, 1)
left = Vector(-1, 0)
right = Vector(1, 0)

#~ def draw_vector(screen, color, a, b):
#~     pygame.draw.circle(screen, color, a, 3, 0)
#~     pygame.draw.line(screen, color, a, b, 1)
#~     left = b - a
#~     left.mod = 10
#~     left.theta -= 7. * math.pi / 8.0
#~     pygame.draw.line(screen, color, b, b+left, 1)
#~     right = b-a
#~     right.mod = 10
#~     right.theta += 7. * math.pi / 8.0
#~     pygame.draw.polygon(screen, color, [b, b+left, b+right, b], 0)

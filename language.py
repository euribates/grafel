#!/usr/bin/python3
# -*- coding: utf-8 -*-    

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import sys
from itertools import islice
from vectors import Vector
from colors import Color
import actors

from pyparsing import (
    Word, alphas, alphanums, nums, Literal, Group,
    ZeroOrMore, OneOrMore, oneOf, StringEnd,
    Optional, Suppress,
    )

table_of_symbols = {}

def get_symbol(name):
    global table_of_symbols
    return table_of_symbols[name]

def params_to_dict(sequence):
    options = dict(zip(islice(sequence, 0, None, 2), islice(sequence, 1, None, 2)))
    return options

def parse_castline(l):
    global table_of_symbols
    name, role, args = l
    options = {}
    if args:
        options = params_to_dict(args)
    print('options', options)
    try:
        new_actor = actors.create_actor(name, role, **options)
        print('new_actor', new_actor) 
        table_of_symbols[name] = new_actor
    except Exception as err:
        print('err', err)
    return l

# Gramatica

colon = Suppress(Literal(':'))
EOL = Suppress(';')
number = Word(nums)
vector = number + Literal('x') + number
color = oneOf("black white red blue green yellow")
attr = Literal("size") + vector | Literal("color") + color
attrs = ZeroOrMore(attr)
identifier = Word(alphas, alphanums)
role = oneOf('Square Star')
castline = (
    identifier('name')
    + Suppress('=')
    + role('role')
    + Group(attrs)('params')
    )
cast = Literal('Cast') + colon + OneOrMore(castline)
script = cast + StringEnd()

# set parse actions

castline.setParseAction(parse_castline)
number.setParseAction(lambda l: int(l[0]))
vector.setParseAction(lambda l: Vector(int(l[0]), int(l[2])))
color.setParseAction(lambda l: Color(l[0]))

def get_parser():
    global script
    return script




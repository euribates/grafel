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
    Optional,
    Suppress,
    )

table_of_symbols = {}


def parse_castline(l):
    global table_of_symbols
    name, role, args = l
    options = {}
    if args:
        options = dict(zip(islice(args, 0, None, 2), islice(args, 1, None, 2)))
    print('options', options)
    try:
        new_actor = actors.create_actor(name, role, **options)
        print('new_actor', new_actor) 
        table_of_symbols[name] = new_actor
    except Exception as err:
        print('err', err)
    
    return l


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
    identifier.setResultsName('name')
    + Suppress('=')
    + role.setResultsName('role')
    + Group(attrs)
    )
cast = Literal('Cast') + colon + OneOrMore(castline)
script = cast + StringEnd()


castline.setParseAction(parse_castline)

number.setParseAction(lambda l: int(l[0]))
vector.setParseAction(lambda l: Vector(int(l[0]), int(l[2])))
color.setParseAction(lambda l: Color(l[0]))

result = script.parseString('''
Cast:

    bob = Square size 50x50 color red 
    star = Star color white
''', parseAll=True)

print(table_of_symbols)
print(result.asList())


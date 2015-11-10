#!/usr/bin/python3
# -*- coding: utf-8 -*-    

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import re
import sys
import traceback
from itertools import islice
from vectors import Vector
from colors import Color
import actors
import actions
import logs

import pyparsing
from pyparsing import (
    Word, alphas, alphanums, nums, Literal, Group,
    ZeroOrMore, OneOrMore, oneOf, StringEnd,
    Optional, Suppress, Keyword, Regex,
    quotedString, delimitedList,
    ParseException, dblSlashComment,
    )

logger = logs.create(__name__)

table_of_symbols = {}
_actions = []

def get_actions():
    global _actions
    return _actions

def dump(s, loc, toks):
    logger.error('dump s: {}'.format(s))
    logger.error('dump loc: {}'.format(loc))
    logger.error('dumo toks: {}'.format(toks))

def create_interval(s, loc, toks):
    left, sign, right = tuple(toks[0])
    left = int(left)
    right = int(right)
    if sign == '-':
        return actions.Interval(left, right)
    else:
        return actions.Interval(left, left+right)



def add_action(s, loc, toks):
    global _actions
    tupla = tuple(toks[0])
    _actions.append(tupla)


def remove_quotes(s, loc, toks):
    logger.info('s: {}'.format(s))
    logger.info('loc: {}'.format(loc))
    logger.info('toks: {}'.format(toks))
    result = toks[0]
    return result[1:-1]  

def get_actor(name):
    global table_of_symbols
    return table_of_symbols[name]

def actors_list():
    return table_of_symbols.keys()

def params_to_dict(sequence):
    options = dict(zip(islice(sequence, 0, None, 2), islice(sequence, 1, None, 2)))
    return options

def parse_castline(l):
    logger.info('called parse_castline with l={}'.format(l))
    global table_of_symbols
    name, role, args = l
    options = {}
    if args:
        options = params_to_dict(args)
    new_actor = actors.create_actor(name, role, **options)
    table_of_symbols[name] = new_actor
    return l

# Gramatica

LPAR = Suppress(Literal("("))
RPAR = Suppress(Literal(")"))

alpha = Regex('0?\.\d+')
colon = Suppress(Literal(':'))
EOL = Suppress(';')
number = Word(nums)
vector = number + Literal('x') + number

colorcode = Regex('#[0-9a-f]{6}', re.IGNORECASE) \
    | oneOf("black white red blue green yellow gold silver purple orange") 

attr = (
    Keyword("size") + vector
    | Keyword("pos") + vector
    | Keyword('num') + oneOf("1 2 3 4 5 6").setParseAction(lambda l: int(l[0]))
    | Keyword('side') + number
    | Keyword('radius') + number
    | Keyword('width') + number
    | Keyword('height') + number
    | Keyword('text') + quotedString.setParseAction(remove_quotes)
    | Keyword('alpha') + alpha
    | Keyword('points') + LPAR
                        + Group(delimitedList(vector))('points')
                        + RPAR
    | Keyword("color") + colorcode
    )

attrs = ZeroOrMore(attr)
Identifier = Word(alphas, alphanums)
role = oneOf('Square Rect RoundRect Star Dice Label Text Circle Triangle')
castline = (
    Identifier('name')
    + Suppress('=')
    + role('role')
    + Group(attrs)('params')
    )
Cast = Keyword('Cast') + colon + OneOrMore(castline)('castlines')

Interval = Group(number + oneOf('- +') + number)
Verb = oneOf('Move Fall Land')
Delta = vector

ActionLine = Group(Interval + Verb + Identifier + Delta)

Actions = Keyword('Actions') + colon + OneOrMore(ActionLine)('action_lines')

script = Cast + Actions + StringEnd()
script.ignore(dblSlashComment)

# set parse actions

Interval.setParseAction(create_interval)
ActionLine.setParseAction(add_action)
alpha.setParseAction(lambda l: float(l[0]))
castline.setParseAction(parse_castline)
number.setParseAction(lambda l: int(l[0]))
vector.setParseAction(lambda l: Vector(int(l[0]), int(l[2])))
colorcode.setParseAction(lambda l: Color(l[0]))


def get_parser():
    global script
    return script




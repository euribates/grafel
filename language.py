#!/usr/bin/env python3
# -*- coding: utf-8 -*-    

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
    quotedString, delimitedList, Combine,
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

def parse_integer(s, loc, toks):
    #dump(s, loc, toks)
    l = tuple(toks)
    return int(l[0])

def create_interval(s, loc, toks):
    # dump(s, loc, toks)
    t = tuple(toks[0])
    if len(t) == 3:
        left, sign, right = t
        left = int(left)
        right = int(right)
        if sign == '-':
            return (left, right)
        else:
            return (left, left+right)
    elif len(t) == 1:
        n = int(t[0])
        return (n, n+1)



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
Positive = Word(nums)
Integer = Combine(Optional('-')+Word(nums))
vector = Integer + Literal('x') + Integer

colorcode = Regex('#[0-9a-f]{6}', re.IGNORECASE) \
    | oneOf("black white red blue green yellow gold silver gray purple orange") 

attr = (
    Keyword("size") + vector
    | Keyword("pos") + vector
    | Keyword('num') + oneOf("1 2 3 4 5 6").setParseAction(lambda l: int(l[0]))
    | Keyword('side') + Positive
    | Keyword('fontsize') + Positive 
    | Keyword('radius') + Positive
    | Keyword('width') + Positive
    | Keyword('height') + Positive
    | Keyword('text') + quotedString.setParseAction(remove_quotes)
    | Keyword('filename') + quotedString.setParseAction(remove_quotes)
    | Keyword('alpha') + alpha
    | Keyword('points') + LPAR
                        + Group(delimitedList(vector))('points')
                        + RPAR
    | Keyword("color") + colorcode
    )

attrs = ZeroOrMore(attr)
Identifier = Word(alphas, alphanums)
role = oneOf('Square Rect RoundRect Star Dice Label Text Circle Triangle Bitmap')
castline = (
    Identifier('name')
    + Suppress('=')
    + role('role')
    + Group(attrs)('params')
    )
Cast = Keyword('Cast') + colon + OneOrMore(castline)('castlines')

Interval = Group(Integer + oneOf('- +') + Integer) | Group(Integer)

Action = (
      Keyword("Move") + vector
    | Keyword("Fall") + vector
    | Keyword("Land") + vector
    | Keyword("EaseIn") + vector
    | Keyword("EaseOut") + vector
    | Keyword("Swing") + vector
    | Keyword("Enter") + vector
    | Keyword("Colorize") + colorcode
    | Keyword("Exit")
    | Keyword("Background")
    | Keyword("Foreground")
    )

ActionLine = Group(Interval + Identifier + Action)

Actions = Keyword('Actions') + colon + OneOrMore(ActionLine)('action_lines')

script = Cast + Actions + StringEnd()
script.ignore(dblSlashComment)

# set parse actions

Interval.setParseAction(create_interval)
ActionLine.setParseAction(add_action)
alpha.setParseAction(lambda l: float(l[0]))
castline.setParseAction(parse_castline)
Positive.setParseAction(lambda l: int(l[0]))
Integer.setParseAction(parse_integer)
vector.setParseAction(lambda l: Vector(int(l[0]), int(l[2])))
colorcode.setParseAction(lambda l: Color(l[0]))


def get_parser():
    global script
    return script




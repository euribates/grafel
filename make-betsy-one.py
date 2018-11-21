#!/usr/bin/env python3

import math
import random
from decimal import Decimal
from collections import OrderedDict

random.seed(123)

class OpVal:

    NUM = 0

    def __init__(self, v, color=''):
        v = float(v)
        self.value = Decimal('{:.2f}'.format(v))
        self.x = 0
        self.y = 0
        self.color = color
        self.num = OpVal.NUM
        OpVal.NUM += 1

    @property
    def name(self):
        return 'n_{}'.format(self.num)

    def __repr__(self):
        return '{:.2f}'.format(self.value)

    def __add__(self, other):
        result = OpVal(0)
        result.value = self.value + other.value
        return result


samples = OrderedDict([
    ('#FFF68F', (940.06, -304.99, -635.07)),
    ('#7FFFD4', (63.27, -797.41, -120.84, 905.04, -559.56, -358.85, 173.14, 695.21)),
    ('#FF7F50', (333.73, 114.91, 104.67, 139.79, -693.10)),
    ('#18838B', (-261.16, -937.44, -99.88, 1298.48)),
    ('#9C661F', (450.57, 281.47, 47.77, -361.52, -504.21, -633.64, 719.56)),
    ('#FF6103', (-332.01, -924.77, 535.43, 561.64, 692.6, 863.49, -1396.38)),
    ('#ED9121', (532.03, -782.65, -753.82, 945.49, -278.17, 355.55, 915.07, -933.5)),
    ('#8FBC8F', (477.39, 807.34, 203.59, 861.63, 23.9, 244.41, -2618.26)),
    ])

for color in samples:
    samples[color] = [OpVal(v, color) for v in samples[color]]

numbers = [ num for color in samples for num in samples[color] ]

color = '#FFF68F'
print([v.value for v in samples[color]])
print([type(v.value) for v in samples[color]])
print(sum([v.value for v in samples[color]]))

for color in samples:
    acc = sum([v.value for v in samples[color]])
    print(acc)
    assert acc == Decimal('0.0')


# random.shuffle(numbers)


def get_col_row(n):
    return n % 8, n // 8


def get_coords(row, col):
    return 80 + row * 160, 60 + col * 120


with open('betsy-01.grafel', 'w') as f:
    f.write('Cast:\n\n')
    for i, n in enumerate(numbers):
        col, row = get_col_row(i)
        x, y = get_coords(col, row)
        pos = '{}x{}'.format(x, -100)
        f.write('   {act} = Text text "{num}" pos {pos} color {clr}\n'.format(
            act=n.name,
            num=str(n),
            pos=pos,
            clr='#CECECE',
            ))
    f.write('Actions:\n\n')
    # Numbers fall
    for (i, n) in enumerate(numbers):
        start = random.randrange(12, 25)
        finish = start + random.randrange(10, 25)
        actor = n.name
        x, y = get_coords(*get_col_row(i))
        f.write('    {start}-{finish} Land {actor} {x}x{y}\n'.format(
            **locals()
            ))
    # Number get colorized
    for n in numbers:
        f.write('    {start}-{finish} Colorize {actor} {color}\n'.format(
            start=75,
            finish=100,
            actor=n.name,
            color=n.color,
            ))
    # Fade Out all except first group (yellow)
    for n in numbers:
        if n.color == '#FFF68F':
            continue
        f.write('    {start}-{finish} FadeOut {actor}\n'.format(
            start=150,
            finish=175,
            actor=n.name,
            ))




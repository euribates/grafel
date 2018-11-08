#!/usr/bin/env python

import random

random.seed(123)

# Los primeros 8 suman 0

numbers = [63.27, -797.41, -120.84, 905.04, -559.56, -358.85, 173.14, 695.21,
 261.16, 937.44, 99.88, 396.07, 333.73, 114.91, 104.67, 139.79, 31.29,
 450.57, 281.47, 47.77, 361.52, 504.21, 633.64, 588.81,
 332.01, 924.77, 535.43, 561.64, 692.6, 863.49, 694.42,
 532.03, 782.65, 753.82, 945.49, 278.17, 355.55, 915.07,
 477.39, 807.34, 203.59, 861.63, 23.9, 244.41, 523.72,
 940.06, 304.99, 997.76]

# numbers = [
    # round(random.randrange(10.0, 1000.0) + random.random(), 2)
    # for _ in range(48)
    # ]


print(numbers)
# numbers = list(range(1, 49))

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
        f.write('   {act} = Label text "{num}" pos {pos} color {clr}\n'.format(
            act='n_{}'.format(i+1),
            num=n,
            pos=pos,
            clr='red' if n < 0 else '#1212FF',
            ))
    f.write('Actions:\n\n')
    for (i, n) in enumerate(numbers):
        start = random.randrange(12, 25)
        finish = random.randrange(75, 90)
        actor = 'n_{}'.format(i+1)
        x, y = get_coords(*get_col_row(i))
        f.write('    {start}-{finish} EaseIn {actor} {x}x{y}\n'.format(
            **locals()
            ))





#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# colors.py

import re

class Color:

    pat_hex_color = re.compile(
        '#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})',
        re.IGNORECASE
        )
    
    name_map = {
        'white': (255, 255, 255),
        'red': (255,0,0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'black': (0, 0, 0),
        'yellow': (255, 255, 0),
        'fuchsia': (255, 0, 255),
        'aliceblue': (240, 248, 255),
        'brown4': (139, 35, 35),
        'cadetblue': (95, 158, 160),
        'khaki': (240,230,140),
        'maroon': (128,0,0),
        'gold': (255, 215, 0),
        'silver': (192, 192, 192),
        'dimgray': (105, 105, 105),
        'ghostgray': (248, 248, 255),
        }

    def __init__(self, *args):
        argc = len(args)
        if argc == 1:
            self.name = args[0]
            if self.name in Color.name_map:
                self.red, self.green, self.blue = Color.name_map[self.name]
            else:
                m = Color.pat_hex_color.match(self.name)
                if m:
                    self.red = int(m.group(1), 16)
                    self.green = int(m.group(2), 16)
                    self.blue = int(m.group(3), 16)
                else:
                    raise ValueError('No se ha especificado correctamente el color')
        elif argc == 3:
            self.red = args[0]
            self.green = args[1]
            self.blue = args[2]
        else:
            raise ValueError('No se ha especificado correctamente el color')

    def as_rgb(self):
        return (self.red, self.green, self.blue,)

    def as_hex(self):
        return '#{:02x}{:02x}{:02x}'.format(
            self.red, self.green, self.blue
            )

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        else:
            return self.as_hex()


black = Color('black')
white = Color('white')
red = Color('red')
blue = Color('blue')
green = Color('green')
yellow = Color('yellow')
khaki = Color('khaki')
maroon = Color('maroon')

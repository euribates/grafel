#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# colors.py

import six
import re

_name_map = {
    'black': (0, 0, 0),
    'brown4': (139, 35, 35),
    'ghostgray': (248, 248, 255),
    'navy': (0x00, 0x00, 0x80),
    'darkblue': (0x00, 0x00, 0x8b),
    'mediumblue': (0x00, 0x00, 0xcd),
    'blue': (0x00, 0x00, 0xff),
    'darkgreen': (0x00, 0x64, 0x00),
    'green': (0x00, 0x80, 0x00),
    'teal': (0x00, 0x80, 0x80),
    'darkcyan': (0x00, 0x8b, 0x8b),
    'deepskyblue': (0x00, 0xbf, 0xff),
    'darkturquoise': (0x00, 0xce, 0xd1),
    'mediumspringgreen': (0x00, 0xfa, 0x9a),
    'lime': (0x00, 0xff, 0x00),
    'springgreen': (0x00, 0xff, 0x7f),
    'aqua': (0x00, 0xff, 0xff),
    'cyan': (0x00, 0xff, 0xff),
    'midnightblue': (0x19, 0x19, 0x70),
    'dodgerblue': (0x1e, 0x90, 0xff),
    'lightseagreen': (0x20, 0xb2, 0xaa),
    'forestgreen': (0x22, 0x8b, 0x22),
    'seagreen': (0x2e, 0x8b, 0x57),
    'darkslategray': (0x2f, 0x4f, 0x4f),
    'limegreen': (0x32, 0xcd, 0x32),
    'mediumseagreen': (0x3c, 0xb3, 0x71),
    'turquoise': (0x40, 0xe0, 0xd0),
    'royalblue': (0x41, 0x69, 0xe1),
    'steelblue': (0x46, 0x82, 0xb4),
    'darkslateblue': (0x48, 0x3d, 0x8b),
    'mediumturquoise': (0x48, 0xd1, 0xcc),
    'indigo  ': (0x4b, 0x00, 0x82),
    'darkolivegreen': (0x55, 0x6b, 0x2f),
    'cadetblue': (0x5f, 0x9e, 0xa0),
    'cornflowerblue': (0x64, 0x95, 0xed),
    'rebeccapurple': (0x66, 0x33, 0x99),
    'mediumaquamarine': (0x66, 0xcd, 0xaa),
    'dimgray': (0x69, 0x69, 0x69),
    'slateblue': (0x6a, 0x5a, 0xcd),
    'olivedrab': (0x6b, 0x8e, 0x23),
    'slategray': (0x70, 0x80, 0x90),
    'lightslategray': (0x77, 0x88, 0x99),
    'mediumslateblue': (0x7b, 0x68, 0xee),
    'lawngreen': (0x7c, 0xfc, 0x00),
    'chartreuse': (0x7f, 0xff, 0x00),
    'aquamarine': (0x7f, 0xff, 0xd4),
    'maroon': (0x80, 0x00, 0x00),
    'purple': (0x80, 0x00, 0x80),
    'olive': (0x80, 0x80, 0x00),
    'gray': (0x80, 0x80, 0x80),
    'skyblue': (0x87, 0xce, 0xeb),
    'lightskyblue': (0x87, 0xce, 0xfa),
    'blueviolet': (0x8a, 0x2b, 0xe2),
    'darkred': (0x8b, 0x00, 0x00),
    'darkmagenta': (0x8b, 0x00, 0x8b),
    'saddlebrown': (0x8b, 0x45, 0x13),
    'darkseagreen': (0x8f, 0xbc, 0x8f),
    'lightgreen': (0x90, 0xee, 0x90),
    'mediumpurple': (0x93, 0x70, 0xdb),
    'darkviolet': (0x94, 0x00, 0xd3),
    'palegreen': (0x98, 0xfb, 0x98),
    'darkorchid': (0x99, 0x32, 0xcc),
    'yellowgreen': (0x9a, 0xcd, 0x32),
    'sienna': (0xa0, 0x52, 0x2d),
    'brown': (0xa5, 0x2a, 0x2a),
    'darkgray': (0xa9, 0xa9, 0xa9),
    'lightblue': (0xad, 0xd8, 0xe6),
    'greenyellow': (0xad, 0xff, 0x2f),
    'paleturquoise': (0xaf, 0xee, 0xee),
    'lightsteelblue': (0xb0, 0xc4, 0xde),
    'powderblue': (0xb0, 0xe0, 0xe6),
    'firebrick': (0xb2, 0x22, 0x22),
    'darkgoldenrod': (0xb8, 0x86, 0x0b),
    'mediumorchid': (0xba, 0x55, 0xd3),
    'rosybrown': (0xbc, 0x8f, 0x8f),
    'darkkhaki': (0xbd, 0xb7, 0x6b),
    'silver': (0xc0, 0xc0, 0xc0),
    'mediumvioletred': (0xc7, 0x15, 0x85),
    'indianred ': (0xcd, 0x5c, 0x5c),
    'peru': (0xcd, 0x85, 0x3f),
    'chocolate': (0xd2, 0x69, 0x1e),
    'tan': (0xd2, 0xb4, 0x8c),
    'lightgray': (0xd3, 0xd3, 0xd3),
    'thistle': (0xd8, 0xbf, 0xd8),
    'orchid': (0xda, 0x70, 0xd6),
    'goldenrod': (0xda, 0xa5, 0x20),
    'palevioletred': (0xdb, 0x70, 0x93),
    'crimson': (0xdc, 0x14, 0x3c),
    'gainsboro': (0xdc, 0xdc, 0xdc),
    'plum': (0xdd, 0xa0, 0xdd),
    'burlywood': (0xde, 0xb8, 0x87),
    'lightcyan': (0xe0, 0xff, 0xff),
    'lavender': (0xe6, 0xe6, 0xfa),
    'darksalmon': (0xe9, 0x96, 0x7a),
    'violet': (0xee, 0x82, 0xee),
    'palegoldenrod': (0xee, 0xe8, 0xaa),
    'lightcoral': (0xf0, 0x80, 0x80),
    'khaki': (0xf0, 0xe6, 0x8c),
    'aliceblue': (0xf0, 0xf8, 0xff),
    'honeydew': (0xf0, 0xff, 0xf0),
    'azure': (0xf0, 0xff, 0xff),
    'sandybrown': (0xf4, 0xa4, 0x60),
    'wheat': (0xf5, 0xde, 0xb3),
    'beige': (0xf5, 0xf5, 0xdc),
    'whitesmoke': (0xf5, 0xf5, 0xf5),
    'mintcream': (0xf5, 0xff, 0xfa),
    'ghostwhite': (0xf8, 0xf8, 0xff),
    'salmon': (0xfa, 0x80, 0x72),
    'antiquewhite': (0xfa, 0xeb, 0xd7),
    'linen': (0xfa, 0xf0, 0xe6),
    'lightgoldenrodyellow': (0xfa, 0xfa, 0xd2),
    'oldlace': (0xfd, 0xf5, 0xe6),
    'red': (0xff, 0x00, 0x00),
    'fuchsia': (0xff, 0x00, 0xff),
    'magenta': (0xff, 0x00, 0xff),
    'deeppink': (0xff, 0x14, 0x93),
    'orangered': (0xff, 0x45, 0x00),
    'tomato': (0xff, 0x63, 0x47),
    'hotpink': (0xff, 0x69, 0xb4),
    'coral': (0xff, 0x7f, 0x50),
    'darkorange': (0xff, 0x8c, 0x00),
    'lightsalmon': (0xff, 0xa0, 0x7a),
    'orange': (0xff, 0xa5, 0x00),
    'lightpink': (0xff, 0xb6, 0xc1),
    'pink': (0xff, 0xc0, 0xcb),
    'gold': (0xff, 0xd7, 0x00),
    'peachpuff': (0xff, 0xda, 0xb9),
    'navajowhite': (0xff, 0xde, 0xad),
    'moccasin': (0xff, 0xe4, 0xb5),
    'bisque': (0xff, 0xe4, 0xc4),
    'mistyrose': (0xff, 0xe4, 0xe1),
    'blanchedalmond': (0xff, 0xeb, 0xcd),
    'papayawhip': (0xff, 0xef, 0xd5),
    'lavenderblush': (0xff, 0xf0, 0xf5),
    'seashell': (0xff, 0xf5, 0xee),
    'cornsilk': (0xff, 0xf8, 0xdc),
    'lemonchiffon': (0xff, 0xfa, 0xcd),
    'floralwhite': (0xff, 0xfa, 0xf0),
    'snow': (0xff, 0xfa, 0xfa),
    'yellow': (0xff, 0xff, 0x00),
    'lightyellow': (0xff, 0xff, 0xe0),
    'ivory': (0xff, 0xff, 0xf0),
    'white': (0xff, 0xff, 0xff),
    }

class Color:

    pat_hex_color = re.compile(
        '#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})',
        re.IGNORECASE
        )

    def __init__(self, *args):
        global _name_map
        argc = len(args)
        if argc == 1:
            self.name = args[0]
            if self.name in _name_map:
                self.r, self.g, self.b = _name_map[self.name]
            else:
                m = Color.pat_hex_color.match(self.name)
                if m:
                    self.r = int(m.group(1), 16)
                    self.g = int(m.group(2), 16)
                    self.b = int(m.group(3), 16)
                else:
                    raise ValueError('No se ha especificado correctamente el color')
        elif argc == 3:
            self.r = args[0]
            self.g = args[1]
            self.b = args[2]
        else:
            raise ValueError('No se ha especificado correctamente el color')

    def as_rgb(self):
        return (self.r, self.g, self.b,)

    def as_hex(self):
        return '#{:02x}{:02x}{:02x}'.format(self.r, self.g, self.b)

    def as_svg(self):
        return "rgb({},{},{})".format(self.r, self.g, self.b)

    def __eq__(self, op2):
        if isinstance(op2, six.string_types):
            op2 = Color(op2)
        return (
            self.r == op2.r and 
            self.g == op2.g and
            self.b == op2.b
            )

    def inverse(self):
        r = 255 - self.r
        g = 255 - self.g
        b = 255 - self.b
        return Color(r, g, b)

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        else:
            return self.as_hex()

    def __repr__(self):
        if hasattr(self, 'name'):
            return 'Color("{}")'.format(self.name)
        else:
            return 'Color("{}")'.format(self.as_hex())

    def get_red(self): return self.r
    def set_red(self, new_red): self.r = new_red
    red = property(get_red, set_red)

    def get_green(self): return self.g
    def set_green(self, new_green): self.g = new_green
    green = property(get_green, set_green)

    def get_blue(self): return self.b
    def set_blue(self, new_blue): self.b = new_blue
    blue = property(get_blue, set_blue)



black = Color('black')
white = Color('white')
red = Color('red')
blue = Color('blue')
green = Color('green')
yellow = Color('yellow')
khaki = Color('khaki')
maroon = Color('maroon')

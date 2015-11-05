#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import svgwrite

dwg = svgwrite.Drawing('test.svg', size=(1024, 720))
dwg.add(dwg.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.text('This is a test', insert=(1024//2, 3*720//10), fill='red', font_size="27", text_anchor="middle"))
dwg.add(dwg.text('This is a test', insert=(1024//2, 720//2), fill='red', font_size="27"))
dwg.add(dwg.text('This is another test', insert=(1024//4, 3*720//4), fill='blue', font_size="12"))
dwg.save()


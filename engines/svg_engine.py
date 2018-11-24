#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

import svgwrite
import logs
import fileutils

import colors
from .base_engine import BaseEngine

logger = logs.create(__name__)


def as_color_svg(c):
    if not isinstance(c, colors.Color):
        c = colors.Color(c)
    return c.as_svg()


class SVGEngine(BaseEngine):

    def __init__(self, width=1280, height=720, fps=25, output_dir='/tmp'):
        super().__init__(width, height, fps)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        self.output_dir = output_dir

    def clear(self, frame, grid=False):
        super().clear(frame)
        filename = 'frame_{:05d}.svg'.format(frame)
        full_fn = os.path.join(self.output_dir, filename)
        self.dwg = svgwrite.Drawing(full_fn, size=(self.width, self.height))
        self.dwg.add(
            self.dwg.rect(
                insert=(0, 0),
                size=(self.width, self.height),
                fill=self.bg_color.as_svg(),
                )
            )
        if grid:
            self.grid()

    def line(self, x0, y0, x1, y1, color=None, alpha=1.0):
        color = color or self.fg_color
        self.dwg.add(self.dwg.line(
            start=(x0, y0),
            end=(x1, y1),
            stroke=as_color_svg(color),
            ))

    def rect(self, x, y, width, height, color=None, alpha=1.0):
        color = color or self.fg_color
        self.dwg.add(
            self.dwg.rect(
                (x, y),
                (width, height),
                fill=as_color_svg(color),
                opacity=alpha,
                ))

    def box(self, x, y, width, height, color=None, alpha=1.0):
        color = color or self.fg_color
        self.dwg.add(
            self.dwg.rect(
                (x, y),
                (width, height),
                fill_opacity=0,
                stroke=color,
                stroke_width=3,
                opacity=alpha,
                ))

    def roundrect(self, x, y, width, height, r, color=None, alpha=1.0):
        color = color or self.fg_color
        self.dwg.add(
            self.dwg.rect(
                (x, y),
                (width, height),
                rx=r,
                ry=r,
                fill=as_color_svg(color),
                opacity=alpha,
                ))

    def bitmap(self, x, y, filename, alpha=1.0):
        (w, h) = fileutils.get_image_size(filename)
        target_name = os.path.join(self.output_dir, filename)
        if not os.path.exists(target_name):
            shutil.copyfile(filename, target_name)
        self.dwg.add(
            self.dwg.image(
                fileutils.get_image_data(filename),
                insert=(x - w / 2, y - h / 2),
                opacity=alpha,
                ))
        if self.debug:
            self.line(x-10, y, x+10, y)
            self.line(x, y-10, x, y+10)

    def circle(self, x, y, r, color=None, alpha=1.0):
        color = color or self.fg_color
        self.dwg.add(
            self.dwg.circle(
                (x, y),
                r,
                fill=as_color_svg(color),
                opacity=alpha,
                ))

    def polygon(self, x, y, rpoints, color=None, alpha=1.0):
        color = color or self.fg_color
        points = [(x, y)]
        for p in rpoints:
            x += p[0]
            y += p[1]
            points.append((x, y))
        self.dwg.add(
            self.dwg.polygon(
                points,
                fill=as_color_svg(color),
                opacity=alpha,
                ))

    def text(self, x, y, text, color=None, alpha=1.0, font_size=32):
        color = color or self.fg_color
        self.dwg.add(
            self.dwg.text(
                text,
                insert=(x, y),
                text_anchor='middle',
                dy=['0.33em'],
                dominant_baseline="middle",
                font_family='Delicious',
                font_size=font_size,
                fill=as_color_svg(color),
                opacity=alpha,
                ))

    def end(self):
        self.dwg.save()

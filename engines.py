#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

import colors
from colors import white
import vectors

import svgwrite
import pygame
import logs
import fileutils

logger = logs.create(__name__)

class BaseEngine:

    def __init__(self, width=1280, height=720, fps=25):
        self.width = width
        self.height = height
        self.size = vectors.Vector(width, height)
        self.fps = fps
        self.bg_color = colors.black
        self.fg_color = colors.white
        self.frame = 0
        self.debug = False

    def clear(self, frame):
        logger.info('Clear screen; prepare for start drawing frame {}.'.format(frame))
        self.frame = frame

    def line(self, x0, y0, x1, y1, color=colors.white, alpha=1.0):
        logger.info('Draw line from {}x{} to {}x{} [color:{}|alpha:{}]'.format(
            x0, y0, x1, y1,
            color, alpha
            ))

    def grid(self, step=100):
        for x in range(step, self.width, step):
            self.line(x, 0, x, self.height, alpha=0.25)
        for y in range(step, self.height, step):
            self.line(0, y, self.width, y, alpha=0.25)

    def box(self, x, y, width, height, color=white, alpha=1.0):
        logger.info('Draw box ({}, {}, {}, {}) [color:{}|alpha:{}]'.format(
            x, y, width, height, color, alpha,
            ))

    def rect(self, x, y, width, height, color=white, alpha=1.0):
        logger.info('Draw rect ({}, {}, {}, {}) [color:{}|alpha:{}]'.format(
            x, y, width, height, color, alpha,
            ))

    def circle(self, x, y, r, color=white, alpha=1.0):
        logger.info('Draw circle at {}x{}, radius {} [color:{}|alpha:{}]'.format(
            x, y, r, color, alpha,
            ))

    def polygon(self, x, y, rpoints, color=white, alpha=1.0):
        logger.info('Draw polygon starting as {}x{}+{} points [color:{}|alpha:{}]'.format(
            x, y, len(rpoints), color, alpha,
            ))

    def end(self):
        logger.debug('End of drawing.')

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


    def clear(self, frame):
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

    def line(self, x0, y0, x1, y1, color=None, alpha=1.0):
        color = color or self.fg_color
        self.dwg.add(self.dwg.line(
            start=(x0, y0),
            end=(x1, y1),
            stroke=as_color_svg(color),
            ))

    def rect(self, x, y, width, height, color=None, alpha=1.0):
        color = color or self.fg_color
        self.dwg.add(self.dwg.rect((x, y), (width, height),
            fill=as_color_svg(color),
            opacity=alpha,
            ))

    def box(self, x, y, width, height, color=None, alpha=1.0):
        color = color or self.fg_color
        self.dwg.add(self.dwg.rect((x, y), (width, height),
            fill_opacity=0,
            stroke=color,
            stroke_width=3,
            opacity=alpha,
            ))

    def roundrect(self, x, y, width, height, r, color=None, alpha=1.0):
        color = color or self.fg_color
        self.dwg.add(self.dwg.rect((x, y), (width, height), rx=r, ry=r,
            fill=as_color_svg(color),
            opacity=alpha,
            ))


    def bitmap(self, x, y, filename):
        (w, h) = fileutils.get_image_size(filename)
        target_name = os.path.join(self.output_dir, filename)
        if not os.path.exists(target_name):
            shutil.copyfile(filename, target_name)
        self.dwg.add(self.dwg.image(
            fileutils.get_image_data(filename),
            insert = (x - w / 2, y - h /2),
            ))
        if self.debug:
            self.line(x-10, y, x+10, y)
            self.line(x, y-10, x, y+10)

    def circle(self, x, y, r, color=None, alpha=1.0):
        color = color or self.fg_color
        self.dwg.add(self.dwg.circle(
            (x, y), r,
            fill=as_color_svg(color),
            opacity=alpha,
            ))

    def polygon(self, x, y, rpoints, color=None, alpha=1.0):
        color = color or self.fg_color
        points = [(x,y)]
        for p in rpoints:
            x += p[0]
            y += p[1]
            points.append((x, y))
        self.dwg.add(self.dwg.polygon(
            points,
            fill=as_color_svg(color),
            opacity=alpha,
            ))

    def text(self, x, y, text, color=None, alpha=1.0, font_size=32):
        color = color or self.fg_color
        self.dwg.add(self.dwg.text(
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

class PyGameEngine(BaseEngine):

    def __init__(self, width=1280, height=720, fps=25):
        super().__init__(width=width, height=height, fps=fps)
        logger.error('sizr: {}'.format(self.size))
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            self.size,
            pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.SRCALPHA
            )

    def add_alpha_color(self, color, alpha):
        if not isinstance(color, colors.Color):
            color = colors.Color(color)
        alpha = min(255, int(round(alpha*255)))
        color = (color.red, color.green, color.blue, alpha)
        return color

    def clear(self, frame, grid=False):
        super().clear(frame)
        self.screen.fill(self.bg_color.as_rgb())
        if grid:
            self.grid()

    def line(self, x0, y0, x1, y1, color=None, alpha=1.0):
        color = color or self.fg_color
        super().line(x0, y0, x1, y1, color, alpha)
        color = self.add_alpha_color(color, alpha)
        pygame.draw.line(self.screen, color, (x0, y0), (x1, y1), 1) 

    def rect(self, x, y, width, height, color=None, alpha=1.0):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        s = pygame.Surface((width, height), pygame.SRCALPHA)   # per-pixel alpha
        s.fill(color)
        self.screen.blit(s, (x, y))

    def box(self, x, y, width, height, color=None, alpha=1.0):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        s = pygame.Surface((width+1, height+1), pygame.SRCALPHA)   # per-pixel alpha
        pygame.draw.rect(s, color, (1, 1, width-1, height-1), 3)
        self.screen.blit(s, (x, y))


    def roundrect(self, x, y, width, height, r, color=None, alpha=1.0):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        s = pygame.Surface((width, height), pygame.SRCALPHA)   # per-pixel alpha
        pygame.draw.circle(s, color, (r, r), r)
        pygame.draw.circle(s, color, (width-r,r), r)
        pygame.draw.circle(s, color, (r, height-r),r)
        pygame.draw.circle(s, color, (width-r, height-r),r)

        pygame.draw.rect(s, color, (r, 0, width-(2*r), height))
        pygame.draw.rect(s, color, (0, r, width, height-2*r))
        self.screen.blit(s,(x, y))

    def circle(self, x, y, r, color=None, alpha=1.0):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        side = r << 2
        s = pygame.Surface((side, side), pygame.SRCALPHA)   # per-pixel alpha
        pygame.draw.circle(s, color, (r, r), r, 0)
        self.screen.blit(s, (x-r, y-r))

    def polygon(self, x, y, rpoints, color=None, alpha=1.0):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        points = [(x,y)]
        for p in rpoints:
            x += p[0]
            y += p[1]
            points.append((x, y))
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)   # per-pixel alpha
        pygame.draw.polygon(s, color, points, 0)
        if self.debug:
            for p in points:
                v = vectors.Vector(p[0], p[1])
                pygame.draw.circle(s, colors.red.as_rgb(), v, 3, 0)
        self.screen.blit(s, (0, 0))


    def lines(self, points, color=None):
        color = color or self.fg_color
        pygame.draw.polygon(self.screen, color.as_rgb(), points, 0)
        pygame.draw.aalines(
            self.screen,
            color.as_rgb(),
            True,
            points
            )
        if self.debug:
            for v in points:
                pygame.draw.circle(scr, (255, 0, 0), v, 3, 0)

    def text(self, x, y, text, color=None, alpha=1.0, font_size=32):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        f = pygame.font.SysFont('Delicious', font_size, bold=False, italic=False)
        s = f.render(text, True, color)
        rect = s.get_rect()
        rect.center = (x, y)
        self.screen.blit(s, rect)

    def bitmap(self, x, y, filename):
        img = pygame.image.load(filename)
        rect = img.get_rect()
        rect.center = (x, y)
        self.screen.blit(img, rect)
        if self.debug:
            self.line(x-20, y, x+20, y)
            self.line(x, y-20, x, y+20)

    def end(self):
        pygame.display.flip()
        self.clock.tick(self.fps)




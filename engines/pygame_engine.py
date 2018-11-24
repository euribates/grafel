#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import logs

import colors
from .base_engine import BaseEngine

logger = logs.create(__name__)


class PyGameEngine(BaseEngine):

    def pygame_init(self):
        pygame.display.init()
        pygame.joystick.init()
        # pygame.threads.init()
        pygame.font.init()
        pygame.scrap.init()
        pygame.fastevent.init()

    def __init__(self, width=1280, height=720, fps=25):
        super().__init__(width=width, height=height, fps=fps)
        self.pygame_init()
        self.clock = pygame.time.Clock()
        mode = (
            pygame.HWSURFACE |
            pygame.DOUBLEBUF |
            pygame.SRCALPHA |
            pygame.NOFRAME
            )
        self.screen = pygame.display.set_mode(self.size, mode)

    def get_surface(self, width=None, height=None):
        width = width or self.width
        height = height or self.height
        return pygame.Surface(
            (width, height),
            pygame.SRCALPHA,  # per-pixel alpha
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
        s = self.get_surface(width, height)
        s.fill(color)
        self.screen.blit(s, (x, y))

    def box(self, x, y, width, height, color=None, alpha=1.0):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        s = self.get_surface(width+1, height+1)
        pygame.draw.rect(s, color, (1, 1, width-1, height-1), 3)
        self.screen.blit(s, (x, y))

    def roundrect(self, x, y, width, height, r, color=None, alpha=1.0):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        s = self.get_surface(width, height)
        pygame.draw.circle(s, color, (r, r), r)
        pygame.draw.circle(s, color, (width-r, r), r)
        pygame.draw.circle(s, color, (r, height-r), r)
        pygame.draw.circle(s, color, (width-r, height-r), r)
        pygame.draw.rect(s, color, (r, 0, width - (2*r), height))
        pygame.draw.rect(s, color, (0, r, width, height - 2*r))
        self.screen.blit(s, (x, y))

    def circle(self, x, y, r, color=None, alpha=1.0):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        side = r << 2
        s = self.get_surface(side, side)
        pygame.draw.circle(s, color, (r, r), r, 0)
        self.screen.blit(s, (x-r, y-r))

    def polygon(self, x, y, rpoints, color=None, alpha=1.0):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        points = [(x, y)]
        for p in rpoints:
            x += p[0]
            y += p[1]
            points.append((x, y))
        s = self.get_surface()
        pygame.draw.polygon(s, color, points, 0)
        if self.debug:
            for p in points:
                v = (p[0], p[1])
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
                pygame.draw.circle(self.screen, (255, 0, 0), v, 3, 0)

    def text(self, x, y, text, color=None, alpha=1.0, font_size=32):
        color = color or self.fg_color
        color = self.add_alpha_color(color, alpha)
        f = pygame.font.SysFont(
            'Delicious',
            font_size,
            bold=False,
            italic=False,
            )
        s = f.render(text, True, color)
        if alpha < 1.0:
            s.convert_alpha()
            s.set_alpha(alpha*255)
            s.fill((255, 255, 255, alpha*255), None, pygame.BLEND_RGBA_MULT) 
        rect = s.get_rect()
        rect.center = (x, y)
        self.screen.blit(s, rect)

    def bitmap(self, x, y, filename, alpha=1.0):
        img = pygame.image.load(filename)
        if alpha < 1.0:
            img.convert_alpha()
            img.set_alpha(alpha*255)
            img.fill((255, 255, 255, alpha*255), None, pygame.BLEND_RGBA_MULT) 
        rect = img.get_rect()
        rect.center = (x, y)
        self.screen.blit(img, rect)
        if not self.debug:
            self.line(x-20, y, x+20, y)
            self.line(x, y-20, x, y+20)

    def end(self):
        pygame.display.flip()
        self.clock.tick(self.fps)

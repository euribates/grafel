#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import functools

import pygame

@functools.lru_cache(maxsize=None)
def get_image_size(filename):
    if not os.path.exists(filename):
        raise ValueError(
            'No puedo encontrar el fichero: {}'.format(filename)
            )
    return pygame.image.load(filename).get_size()

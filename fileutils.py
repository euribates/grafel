#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import functools
import base64

import pygame

@functools.lru_cache(maxsize=None)
def get_image_size(filename):
    if not os.path.exists(filename):
        raise ValueError(
            'No puedo encontrar el fichero: {}'.format(filename)
            )
    return pygame.image.load(filename).get_size()

@functools.lru_cache(maxsize=None)
def get_image_data(filename):
    with open(filename, 'rb') as f:
        buff = f.read()
    return 'data:image/png;base64,{}'.format(
        base64.b64encode(buff).decode()
        )


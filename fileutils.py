#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import six
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

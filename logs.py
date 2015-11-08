#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging

def create(name, level=logging.WARNING):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler(stream=sys.stderr)
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
        ))
    logger.addHandler(ch)
    return logger


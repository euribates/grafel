#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import defaults
import argparse

options_parser = argparse.ArgumentParser()
options_parser.add_argument("script", help="Script de animación en Grafel")

options_parser.add_argument(
    "--grid", help="Mostrar rejilla",
    action='store_true',
    )

options_parser.add_argument(
    "--num-frames", help="Total de frames a mostrar",
    default=defaults.NUM_FRAMES, type=int,
    )

options_parser.add_argument(
    "--background", help="color de fondo",
    default=defaults.BACKGROUND,
    )

options_parser.add_argument(
    "--foreground", help="color de fondo",
    default=defaults.FOREGROUND,
    )

options_parser.add_argument(
    "--fps", help="Frames / sec",
    default=defaults.FPS, type=int,
    )

options_parser.add_argument(
    "--size", help="Resolución en pixels (Ancho x Alto)",
    default='{}x{}'.format(defaults.WIDTH, defaults.HEIGHT),
    )

options_parser.add_argument(
    "--output-dir", help="Directorio de salida (./tmp por defecto)",
    default='./tmp'
    )


def get_options():
    global options_parser
    return options_parser.parse_args()

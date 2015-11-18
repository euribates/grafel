#!/usr/bin/env python3
# -*- coding: utf-8 -*-    

import defaults
import argparse

options_parser = argparse.ArgumentParser()
options_parser.add_argument("script", help="Script de animación en Grafel")

options_parser.add_argument("--grid",
    help="Mostrar rejilla",
    action='store_true',
    )

options_parser.add_argument("--num-frames",
    help="Total de frames a mostrar",
    default=defaults.NUM_FRAMES,
    type=int,
    )

options_parser.add_argument("--background",
    default=defaults.BACKGROUND,
    help="color de fondo",
    )

options_parser.add_argument("--foreground",
    default=defaults.FOREGROUND, 
    help="color de fondo",
    )

options_parser.add_argument("--fps",
    default=defaults.FPS,
    help="Frames / sec",
    type=int, 
    )

options_parser.add_argument("--size",
    default='{}x{}'.format(defaults.WIDTH, defaults.HEIGHT),
    help="Resolución en pixels (Ancho x Alto)",
    )

options_parser.add_argument("--output_dir",
    help="Directorio de salida (./tmp por defecto)",
    default='./tmp'
    )

def get_options():
    global options_parser
    return  options_parser.parse_args()

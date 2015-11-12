#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import sys
import pygame
import language
import argparse

import vectors
import actions
from control import Scheduler
from studio import Stage
from engines import SVGEngine
import logs

logger = logs.create(__name__)

options_parser = argparse.ArgumentParser()
options_parser.add_argument("script", help="Script de animación en Grafel")
options_parser.add_argument("--grid",
    help="Mostrar rejilla",
    action='store_true',
    )
options_parser.add_argument("--num_frames",
    help="Total de frames a mostrar",
    type=int,
    )
options_parser.add_argument("--background", help="color de fondo",)
options_parser.add_argument("--foreground", help="color de fondo",)
options_parser.add_argument("--output_dir",
    help="Directorio de salida (./tmp por defecto)",
    default='./tmp'
    )

opts = options_parser.parse_args()

logger.error('background: {}'.format(opts.background))

actors = []
if opts.script:
    parser = language.get_parser()
    try:
        tree = parser.parseFile(opts.script)

    except language.ParseException as err:
        print('Error de parseo en {}'.format(opts.script))
        print(err)
        print('num línea: {}'.format(err.lineno))
        print('>>> {}'.format(err.line))
        print('---' + '-'*err.col + '^')
        sys.exit()

    actors = [language.get_actor(_) for _ in language.actors_list()]
    sch = Scheduler()
    engine = SVGEngine(output_dir=opts.output_dir)
    stage = Stage(engine,
        background=opts.background,
        foregroud=opts.foreground,
        num_frames=opts.num_frames,
        )
    stage.add_actors(*actors)
    for t in language.get_actions():
        (interval, actor_name, action_name) = t[0:3]
        args = t[3:]
        if action_name == 'Move':
            ActionKlass = actions.MoveTo
        elif action_name == 'Land':
            ActionKlass = actions.Land
        elif action_name == 'Fall':
            ActionKlass = actions.Fall
        elif action_name == 'Enter':
            ActionKlass = actions.Enter
        elif action_name == 'Background':
            ActionKlass = actions.Background
        elif action_name == 'Foreground':
            ActionKlass = actions.Foreground
        elif action_name == 'Exit':
            ActionKlass = actions.Exit
        elif action_name == 'Swing':
            ActionKlass = actions.Swing
        elif action_name == 'EaseIn':
            ActionKlass = actions.EaseIn
        elif action_name == 'EaseOut':
            ActionKlass = actions.EaseOut

        actor = language.get_actor(actor_name)
        action = ActionKlass(
            actor,
            interval.lower_bound,
            interval.upper_bound,
            *args
            )
        logger.error('action: {}'.format(action))
        sch.add_action(action)
    force_exit = False
    for frame in range(stage.num_frames):
        stage.draw(frame) 
        sch.next()


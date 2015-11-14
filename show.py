#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse

import pygame
import language

import vectors
import actions
from control import Scheduler
from studio import Stage
from engines import PyGameEngine
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
options_parser.add_argument("--background",
    default='black',
    help="color de fondo",
    )
options_parser.add_argument("--foreground",
    default='white', 
    help="color de fondo",
    )
options_parser.add_argument("--fps", help="Frames / sec", type=int, default=25)

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
    engine = PyGameEngine()
    stage = Stage(engine,
        background=opts.background,
        foregroud=opts.foreground,
        num_frames=opts.num_frames,
        fps=opts.fps,
        )
    stage.add_actors(*actors)
    for t in language.get_actions():
        (interval, actor_name, action_name) = t[0:3]
        from_frame, to_frame = interval
        actor = language.get_actor(actor_name)
        args = t[3:]
        action = actions.create_action(
            action_name, actor,
            from_frame, to_frame,
            *args
            )
        sch.add_action(action)
    force_exit = False
    for frame in range(stage.num_frames):
        stage.draw(frame) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                force_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    force_exit = True
        if force_exit:
            break
        sch.next()
for a in stage.actors:
    print('{} {}'.format(a, repr(a)))

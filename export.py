#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import language

import actions
from studio import Stage
from engines import SVGEngine
import config
import logs

logger = logs.create(__name__)
opts = config.get_options()

if opts.script:
    parser = language.get_parser()
    try:
        tree = parser.parseFile(opts.script)
    except language.ParseException as err:
        logger.error('Error de parseo en {}'.format(opts.script))
        logger.error(err)
        logger.error('num línea: {}'.format(err.lineno))
        logger.error('>>> {}'.format(err.line))
        logger.error('---' + '-'*err.col + '^')
        sys.exit()

    actors = [language.get_actor(_) for _ in language.actors_list()]
    engine = SVGEngine(output_dir=opts.output_dir)
    stage = Stage(engine, options=opts)
    stage.add_actors(*actors)
    for t in language.get_actions():
        interval, action_name, actor_name,  *args = t
        from_frame, to_frame = interval
        actor = language.get_actor(actor_name)
        action = actions.create_action(
            action_name, actor,
            from_frame, to_frame,
            *args
            )
        stage.add_action(action)
    for frame in range(stage.num_frames):
        stage.draw(frame)

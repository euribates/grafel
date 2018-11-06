#!/usr/bin/env python

import pytest

import actions
from actors import Label
from control import Scheduler
from studio import Stage
from engines import PyGameEngine


def test_easing():
    move = Label('Move', width=190, pos=(100, 30), color='gold')
    fall = Label('Fall', width=190, pos=(300, 30), color='gold')
    land = Label('Land', width=190, pos=(500, 30), color='gold')
    ease_in = Label('EaseIn', width=190, pos=(700, 30), color='gold')
    ease_out = Label('EaseOut', width=190, pos=(900, 30), color='gold')
    swing = Label('Swing', width=190, pos=(1100, 30), color='gold')
    sch = Scheduler()
    sch.add_action(actions.Move(move, 5, 70, (100, 700)))
    sch.add_action(actions.Fall(fall, 5, 70, (300, 700)))
    sch.add_action(actions.Land(land, 5, 70, (500, 700)))
    sch.add_action(actions.EaseIn(ease_in, 5, 70, (700, 700)))
    sch.add_action(actions.EaseOut(ease_out, 5, 70, (900, 700)))
    sch.add_action(actions.Swing(swing, 5, 70, (1100, 700)))
    engine = PyGameEngine()
    stage = Stage(engine)
    stage.add_actors(move, fall, land, ease_in, ease_out, swing)
    for frame in range(75):
        stage.draw(frame)
        sch.next()


if __name__ == '__main__':
    pytest.main()

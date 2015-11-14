#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test_actors.py

class Scheduler():

    def __init__(self):
        self.actions = {}
        self.actors = set()
        self.active_actions = []
        self.frame = 0

    def reset(self):
        for actor in self.actors:
            actor.reset()
        self.active_actions = []
        self.frame = 0

    def add_action(self, action):
        start_frame = action.lower_bound
        self.actors.add(action.actor)
        key = (action.actor.name, start_frame)
        self.actions.setdefault(key, []).append(action)

    def next(self):
        for action in self.active_actions[:]:
            action.step(self.frame)
            if action.is_last(self.frame):
                action.end(self.frame)
                self.active_actions.remove(action)
        for actor in self.actors:  # New actions that must start
            key = (actor.name, self.frame)
            if key in self.actions:
                for a in self.actions[key]:
                    a.start(self.frame)
                    self.active_actions.append(a)
        self.frame += 1
        return self.frame

    def dump(self, num_frames=15):
        buff = ['\n--[Scheduler actors:{}]----------------------\n'.format(
            len(self.actors)
            )]
        for f in range(num_frames):
            buff.append('{:5d} '.format(f))
            for actor in self.actors:
                pk = (actor.name, f)
                if pk in self.actions:
                    for action in self.actions[pk]:
                        buff.append('Starts {}'.format(
                            action
                            ))
            buff.append('\n')
        buff.append('-------------------------------------\n')
        return ''.join(buff)


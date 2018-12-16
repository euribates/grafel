#!/usr/bin/env python3

import os
import sys
import subprocess
import glob


def get_real_path(filename, base=os.getcwd()):
    return os.path.join(base, filename)


def inkscape_export(source_filename, target_filename):
    commands = [
        "inkscape",
        "-e",
        get_real_path(target_filename),
        get_real_path(source_filename),
        ]
    print(" ".join(commands))
    subprocess.call(commands)


def rsvg_export(source_filename, target_filename):
    commands = [
        "rsvg",
        "-o",
        get_real_path(target_filename),
        get_real_path(source_filename),
        ]
    print(" ".join(commands))
    subprocess.call(commands)


for filename in sorted(glob.glob('./tmp/frame_*.svg')):
    target_filename = filename[:-4] + '.png'
    if os.path.exists(target_filename):
        print('[Skipped]', end='')
        continue
    else:
        print('.', end="")
        sys.stdout.flush()
    inkscape_export(filename, target_filename)
print('Preparando vídeo', end=' ')
subprocess.call([
    'avconv',
    '-i',
    './tmp/frame_%05d.png',
    '-c:v',
    'libx264',
    '-pix_fmt', 'yuv420p',
    './out.mp4',
    ])
print('\nvlc out.mp4')

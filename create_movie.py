#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import glob

for filename in sorted(glob.glob('./tmp/frame_*.svg')):
    target_filename = filename[:-4] + '.png'
    if os.path.exists(target_filename):
        print('[Skipped]', end='')
        continue
    else:
        print('.', end="")
        sys.stdout.flush()
    print("rsvg", filename, target_filename)
    subprocess.call([
        "rsvg",
        "-o",
        target_filename,
        filename,
        ])
print('Preparando vídeo', end=' ')
subprocess.call([
    'avconv',
    '-i','./tmp/frame_%05d.png',
    '-c:v',
    'libx264',
    '-pix_fmt', 'yuv420p',
    './out.mp4',
    ])
print('\nvlc out.mp4')

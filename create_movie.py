#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import glob

for filename in sorted(glob.glob('./tmp/frame_*.svg')):
    print(filename, end=" ")
    target_filename = filename[:-4] + '.png'
    if os.path.exists(target_filename):
        print('[Skipped]')
        continue
    subprocess.call([
        "inkscape", 
        "-z",
        "-e", target_filename,
        "-w", "1280",
        "-h", "720",
        filename
        ])
    print("[ok]")
print('Preparando vídeo', end=' ')
subprocess.call([
    'avconv',
    '-i','./tmp/frame_%05d.png',
    '-c:v',
    'libx264',
    '-pix_fmt', 'yuv420p',
    '/home/jileon/tmp/out.mp4',
    ])

#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os
import sys
import subprocess
import glob

for filename in sorted(glob.glob('/tmp/frame_*.svg')):
    print(filename, end=" ")
    target_filename = filename[:-4] + '.png'
    if os.path.exists(target_filename):
        print('[Skipped]')
        continue
    subprocess.call([
        "inkscape", 
        "-z",
        "-e", target_filename,
        "-w", "1024",
        "-h", "760",
        filename
        ])
    print("[ok]")
print('Preparando vídeo', end=' ')
subprocess.call([
    'avconv',
    '-i','/tmp/frame_%05d.png',
    '-c:v',
    'libx264',
    '-pix_fmt', 'yuv420p',
    '/tmp/out.mp4',
    ])

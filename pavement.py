#!/usr/bin/env

import paver
from paver.easy import path, task, cmdopts, sh


@task
@cmdopts([('filename=', 'f', 'Grafel file')])
def hola(options):
    '''Pruebas con paver.
    '''
    filename = options.hola.filename + '.grafel'
    tmpdir = path("tmp")
    tmpdir.rmtree()
    sh('./export.py {}'.format(filename))
    sh('./create_movie.py')


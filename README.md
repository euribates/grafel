# GRAFEL #

Lenguaje sencillo para la realización de 
secuencias animadas explicativas

## Requerimientos

El desarrollo principal está hecho en Python, y usa pygame y svgwriter para producir 
la salida, y pyparsing para interpretar el lenguaje. El resto de los requerimientos está en el fichero `requirements.txt`.

## Version actual

La versión actual está en alpha.

## Requerimientos

### pygame

Para instalar pygame en Python 3 no podemos usar pip, tenemos que compilar nosostros
mismos el código fuente.

#### Instalar PyGame en Python 3.x

Primero tenemos que instalar las siguientes dependencias:

    sudo apt-get install mercurial python3-dev python3-numpy libav-tools \
        libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
        libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev
 
Después, obtenemos el código fuente de PyGame:

    hg clone https://bitbucket.org/pygame/pygame
 
Luego debemos compilar e instalar:

    cd pygame
    python3 setup.py build
    sudo python3 setup.py install

#### Instalar PyGame en Python 3.x con virtualenv

Si queremos instalar usando virtualenv, simplemente hay que hacer lo mismo 
pero activando previamente el entorno, y luego realizando los pasos
anteriores. Este es un ejemplo, suponiendo que queremos crear el directorio
del entorno virtual `.venv` en el mismo directorio del proyecto, y que tenemos
instaladas todas las dependiencias:

    virtualenv .venv
    source .venv/bin/activate
    hg clone https://bitbucket.org/pygame/pygame
    cd pygame
    python3 setup.py build
    python3 setup.py install --prefix=".venv"

### pyparsing

### svgwrite

### Paquetes Opcionales

 * freetype-py


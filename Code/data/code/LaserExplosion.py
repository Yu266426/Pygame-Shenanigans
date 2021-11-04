import os

from data.code.FileSetup import *
from data.code.Constants import *
from data.code.Explosion import Explosion

class LaserExplosion(Explosion):
    def __init__(self, pos):
        super().__init__(pos, 6, laserExplosionScale, os.path.join(EXPLOSION_FOLDER, "Laser Explosion"))
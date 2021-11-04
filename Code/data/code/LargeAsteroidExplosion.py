import os

from data.code.FileSetup import *
from data.code.Constants import *
from data.code.Explosion import Explosion

class LargeAsteroidExplosion(Explosion):
    def __init__ (self, pos):
        super().__init__(pos, 17, largeAsteroidExplosionScale, os.path.join(EXPLOSION_FOLDER, "Large Asteroid Explosion"))
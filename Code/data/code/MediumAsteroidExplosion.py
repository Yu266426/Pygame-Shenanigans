import os

from data.code.FileSetup import *
from data.code.Constants import *
from data.code.Explosion import Explosion

class MediumAsteroidExplosion(Explosion):
    def __init__ (self, pos):
        super().__init__(pos, 9, mediumAsteroidExplosionScale, os.path.join(EXPLOSION_FOLDER, "Medium Asteroid Explosion"))
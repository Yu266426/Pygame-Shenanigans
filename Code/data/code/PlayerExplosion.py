import os

from data.code.FileSetup import *
from data.code.Constants import *
from data.code.Explosion import Explosion

class PlayerExplosion(Explosion):
    def __init__ (self, pos):
        super().__init__(pos, 15, playerExplosionScale, os.path.join(EXPLOSION_FOLDER, "Player Death Explosion"))
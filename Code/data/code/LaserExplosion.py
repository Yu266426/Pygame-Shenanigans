from data.code.base.Constants import *
from data.code.base.Explosion import Explosion
from data.code.base.Images import laserExplosion


class LaserExplosion(Explosion):
    def __init__(self, pos):
        super().__init__(pos, laserExplosion)
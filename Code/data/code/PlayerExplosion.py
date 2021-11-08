from data.code.base.Constants import *
from data.code.base.Explosion import Explosion
from data.code.base.Images import playerExplosion


class PlayerExplosion(Explosion):
    def __init__(self, pos):
        super().__init__(pos, playerExplosion)

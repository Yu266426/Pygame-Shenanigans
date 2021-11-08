from data.code.base.Explosion import Explosion
from data.code.base.Images import largeAsteroidExplosion


class LargeAsteroidExplosion(Explosion):
    def __init__ (self, pos):
        super().__init__(pos, largeAsteroidExplosion)
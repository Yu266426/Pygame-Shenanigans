from data.code.base.Explosion import Explosion
from data.code.base.Images import mediumAsteroidExplosion


class MediumAsteroidExplosion(Explosion):
    def __init__(self, pos):
        super().__init__(pos, mediumAsteroidExplosion)

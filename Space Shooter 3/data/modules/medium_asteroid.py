from data.modules.asteroid_object import AsteroidObject
from data.modules.helper import get_random_float
from data.modules.images import MEDIUM_ASTEROID_IMAGE


class MediumAsteroid(AsteroidObject):
    def __init__(self, pos, direction, speed_range=(3, 6), spin_speed_range=(-6, 6)):
        super().__init__(pos, MEDIUM_ASTEROID_IMAGE, direction, get_random_float(speed_range[0], speed_range[1]), get_random_float(spin_speed_range[0], spin_speed_range[1]), 8, 8)

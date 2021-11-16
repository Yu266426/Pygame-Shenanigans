import random

from data.modules.helper import get_random_float
from data.modules.asteroid_object import AsteroidObject
from data.modules.images import LARGE_ASTEROID_IMAGE


class LargeAsteroid(AsteroidObject):
    def __init__(self, pos, direction, speed_range=(2, 5), spin_speed_range=(-5, 5)):
        super().__init__(pos, LARGE_ASTEROID_IMAGE, direction, get_random_float(speed_range), get_random_float(spin_speed_range), 20)

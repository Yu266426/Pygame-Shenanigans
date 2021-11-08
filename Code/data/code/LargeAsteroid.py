import json
import os
import random

import pygame
from pygame import mixer

from data.code.LargeAsteroidExplosion import LargeAsteroidExplosion
from data.code.Laser import Laser
from data.code.Player import Player
from data.code.base.AsteroidObject import AsteroidObject
from data.code.base.Constants import largeAsteroidScale, largeAsteroidAccuracy, largeAsteroidExplosionScale, screenScale
from data.code.base.FileSetup import SETTINGS_FILE, AUDIO_FOLDER
from data.code.base.Images import largeAsteroidImage

with open(SETTINGS_FILE) as file:
    settings = json.load(file)


def getDirection(directionPos, pos):
    direction = pygame.math.Vector2(0, 0)

    direction.x = directionPos[0] - (pos[0] + largeAsteroidScale[0] / 2)
    direction.y = directionPos[1] - (pos[1] + largeAsteroidScale[1] / 2)

    direction.normalize_ip()

    angleOffset = random.randint(-largeAsteroidAccuracy, largeAsteroidAccuracy)
    return direction.rotate(angleOffset)


class LargeAsteroid(AsteroidObject):
    def __init__(self, pos, directionPos):
        direction = getDirection(directionPos, pos)

        super().__init__(pos, largeAsteroidImage, largeAsteroidScale, random.randint(1, 360), direction, 5, random.randint(3, 5) * screenScale, random.randint(1, 5))

        self.score = 20

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Big Explosion.wav"))
        self.removeSound.set_volume(0.5 * settings["volume"])

    # Find Angle To Player

    # Removes Health And Checks To See If Removable
    def remove(self, collidedObject, explosionList):
        self.health -= collidedObject.damage
        if self.checkHealth():
            self.removeSound.play()

            # Adds Score If Needed
            if isinstance(collidedObject, Laser):
                if isinstance(collidedObject.origin, Player):
                    collidedObject.origin.addScore(self.score)

            explosionList.add(LargeAsteroidExplosion((self.rect.center[0] - largeAsteroidExplosionScale[0] / 2, self.rect.center[1] - largeAsteroidExplosionScale[1] / 2)))

            self.kill()

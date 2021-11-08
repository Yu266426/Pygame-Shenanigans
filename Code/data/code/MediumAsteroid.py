import json
import random

from pygame import mixer

from data.code.Laser import Laser
from data.code.MediumAsteroidExplosion import MediumAsteroidExplosion
from data.code.Player import Player
from data.code.base.AsteroidObject import AsteroidObject
from data.code.base.Constants import *
from data.code.base.FileSetup import *
from data.code.base.Images import mediumAsteroidImage

with open(SETTINGS_FILE) as file:
    settings = json.load(file)


def offsetDirection(direction):
    angleOffset = random.randint(-mediumAsteroidAccuracy, mediumAsteroidAccuracy)
    return direction.rotate(angleOffset)


class MediumAsteroid(AsteroidObject):
    def __init__(self, pos, direction):
        super().__init__(pos, mediumAsteroidImage, mediumAsteroidScale, random.randint(1, 360), offsetDirection(direction), 2, random.randint(4, 6) * screenScale, random.randint(3, 7))

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Medium Explosion.wav"))
        self.removeSound.set_volume(0.3 * settings["volume"])

        self.score = 5

    # Find Angle To Player

    # Removes A Health And Checks To See If Removable
    def remove(self, collidedObject, explosionList):
        self.health -= collidedObject.damage
        if self.checkHealth():
            self.removeSound.play()

            # Adds Score If Needed
            if isinstance(collidedObject, Laser):
                if isinstance(collidedObject.origin, Player):
                    collidedObject.origin.addScore(self.score)

            explosionList.add(MediumAsteroidExplosion((self.rect.center[0] - mediumAsteroidExplosionScale[0] / 2, self.rect.center[1] - mediumAsteroidExplosionScale[1] / 2)))

            self.kill()

import pygame
import random
import math
import os

from pygame import mixer

from data.code.FileSetup import *
from data.code.Constants import *
from data.code.Settings import *
from data.code.AsteroidObject import AsteroidObject

from data.code.Player import Player
from data.code.Laser import Laser
from data.code.MediumAsteroidExplosion import MediumAsteroidExplosion

class MediumAsteroid(AsteroidObject):
    def __init__(self, pos, direction):
        super().__init__(pos, os.path.join(ASSET_FOLDER, "Medium Asteroid.png"), mediumAsteroidScale, random.randint(1,360), self.offsetDirection(direction), 2, random.randint(4, 6) * screenScale, random.randint(3,7))

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Medium Explosion.wav"))
        self.removeSound.set_volume(0.3 * volume)

        self.score = 5

    # Find Angle To Player
    def offsetDirection(self, direction):
        angleOffset = random.randint(-mediumAsteroidAccuracy, mediumAsteroidAccuracy)
        return direction.rotate(angleOffset)

    # Removes A Health And Checks To See If Removeable
    def remove(self, object, explosionList):
        self.health -= object.damage
        if(self.checkHealth() == True):
            self.removeSound.play()

            # Adds Score If Needed
            if(isinstance(object, Laser)):
                if(isinstance(object.origin, Player)):
                    object.origin.addScore(self.score)

            explosionList.add(MediumAsteroidExplosion((self.rect.center[0] - mediumAsteroidExplosionScale[0] / 2, self.rect.center[1] - mediumAsteroidExplosionScale[1] / 2)))

            self.kill()
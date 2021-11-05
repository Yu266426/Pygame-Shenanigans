import pygame
import random
import os

from pygame import mixer

from data.code.FileSetup import *
from data.code.Constants import *
from data.code.Settings import *
from data.code.AsteroidObject import AsteroidObject

from data.code.Player import Player
from data.code.Laser import Laser
from data.code.LargeAsteroidExplosion import LargeAsteroidExplosion

class LargeAsteroid(AsteroidObject):
    def __init__(self, pos, directionPos):
        direction = self.getDirection(directionPos, pos)

        super().__init__(pos, os.path.join(ASSET_FOLDER, "Large Asteroid.png"), largeAsteroidScale,  random.randint(1,360), direction, 5, random.randint(3, 5) * screenScale, random.randint(1,5))

        self.score = 20

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Big Explosion.wav"))
        self.removeSound.set_volume(0.5 * volume)

    
    # Find Angle To Player
    def getDirection(self, directionPos, pos):
        direction = pygame.math.Vector2(0,0)

        direction.x = directionPos[0] - (pos[0] + largeAsteroidScale[0]/2)
        direction.y = directionPos[1] - (pos[1] + largeAsteroidScale[1]/2)

        direction.normalize_ip()

        angleOffset = random.randint(-largeAsteroidAccuracy, largeAsteroidAccuracy)
        return direction.rotate(angleOffset)

    # Removes Health And Checks To See If Removeable
    def remove(self, object, explosionList):
        self.health -= object.damage
        if(self.checkHealth() == True):
            self.removeSound.play()

            # Adds Score If Needed
            if(isinstance(object, Laser)):
                if(isinstance(object.origin, Player)):
                    object.origin.addScore(self.score)

            explosionList.add(LargeAsteroidExplosion((self.rect.center[0] - largeAsteroidExplosionScale[0] / 2, self.rect.center[1] - largeAsteroidExplosionScale[1] / 2)))

            self.kill()
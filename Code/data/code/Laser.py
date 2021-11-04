import pygame
import math
import os

from pygame import mixer

from data.code.FileSetup import *
from data.code.Constants import *
from data.code.Settings import *
from data.code.Rotatable import Rotatable

from data.code.LaserExplosion import LaserExplosion

class Laser(Rotatable):
    def __init__(self, pos, angle, speed, origin):
        super().__init__(pos, os.path.join(ASSET_FOLDER, "Laser.png"), laserScale, angle)

        self.speed = speed * screenScale

        self.radius = laserScale[1]

        self.sound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Laser.wav"))
        self.sound.set_volume(0.1 * volume)

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Laser Hit.wav"))

        self.health = 1
        self.damage = self.health

        self.origin = origin

    # Offsets To Avoid Player !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Move Into Player Class
    def offset(self):
        offsetter = pygame.math.Vector2(math.cos(math.radians(self.angle)) * laserScale[1] * 2.75, -1 * math.sin(math.radians(self.angle)) * laserScale[1] * 2.75)
        
        self.baseRect.topleft += offsetter

    # Checks To See If Health Is Below Or Equal To 0
    def checkHealth(self):
        return self.health <= 0

    # Returns True To Remove
    def remove(self, object, explosionList):
        self.health -= object.damage
        if(self.checkHealth() == True):
            self.removeSound.play()

            explosionList.add(LaserExplosion((self.rect.center[0] - laserScale[0] / 2, self.rect.center[1] - laserScale[1] / 2)))

            self.kill()

    # Moves In Direction
    def update(self, deltaTime, targetFPS):
        offsetter = pygame.math.Vector2(math.cos(math.radians(self.angle)) * self.speed * deltaTime * targetFPS, -1 * math.sin(math.radians(self.angle)) * self.speed * deltaTime * targetFPS)

        self.baseRect.topleft += offsetter

        self.angleSelf()

        if(self.checkBounds()):
            self.kill()

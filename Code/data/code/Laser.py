import json
import math
import os

import pygame
from pygame import mixer

from data.code.LaserExplosion import LaserExplosion
from data.code.base.Constants import laserScale, screenScale
from data.code.base.FileSetup import AUDIO_FOLDER, SETTINGS_FILE
from data.code.base.Images import laserImage
from data.code.base.Rotatable import Rotatable

with open(SETTINGS_FILE) as file:
    settings = json.load(file)


class Laser(Rotatable):
    def __init__(self, pos, angle, speed, origin):
        super().__init__(pos, laserImage, laserScale, angle)

        self.speed = speed * screenScale

        self.radius = laserScale[1]

        self.sound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Laser.wav"))
        self.sound.set_volume(0.1 * settings["volume"])
        self.sound.play()

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Laser Hit.wav"))
        self.removeSound.set_volume(settings["volume"])

        self.health = 1
        self.damage = self.health

        self.origin = origin

        self.angleSelf()

    # Offsets To Avoid Player
    def offset(self):
        offsetter = pygame.math.Vector2(math.cos(math.radians(self.angle)) * laserScale[1] * 2.75, -1 * math.sin(math.radians(self.angle)) * laserScale[1] * 2.75)

        self.baseRect.topleft += offsetter

    # Checks To See If Health Is Below Or Equal To 0
    def checkHealth(self):
        return self.health <= 0

    # Returns True To Remove
    def remove(self, colllidedObject, explosionList):
        self.health -= colllidedObject.damage
        if self.checkHealth():
            self.removeSound.play()

            explosionList.add(LaserExplosion((self.rect.center[0] - laserScale[0] / 2, self.rect.center[1] - laserScale[1] / 2)))

            self.kill()

    # Moves In Direction
    def update(self, deltaTime, targetFPS):
        offsetter = pygame.math.Vector2(math.cos(math.radians(self.angle)) * self.speed * deltaTime * targetFPS, -1 * math.sin(math.radians(self.angle)) * self.speed * deltaTime * targetFPS)

        self.baseRect.topleft += offsetter

        self.moveSelf()

        if self.checkBounds():
            self.kill()

import json
import math
import os

import pygame
from pygame import mixer

from data.code.PlayerExplosion import PlayerExplosion
from data.code.base.Constants import playerScale, screenScale, playerStartingHealth, screenWidth, screenHeight
from data.code.base.FileSetup import SETTINGS_FILE, AUDIO_FOLDER
from data.code.base.Images import playerImage
from data.code.base.Rotatable import Rotatable

with open(SETTINGS_FILE) as file:
    settings = json.load(file)


class Player(Rotatable):
    def __init__(self, pos):
        super().__init__(pos, playerImage, playerScale, 0)

        self.radius = playerScale[0] / 2

        self.acceleration = 0.9 * screenScale
        self.drag = 0.9

        self.input = pygame.math.Vector2(0, 0)

        self.angle = 0

        self.movement = pygame.math.Vector2(0, 0)

        self.health = playerStartingHealth
        self.damage = self.health

        self.removeSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Player Death.wav"))
        self.removeSound.set_volume(0.6 * settings["volume"])

        self.score = 0

    # Gets Inputs
    def getInput(self, event, up, down, left, right):
        if event.type == pygame.KEYDOWN:
            if event.key == left:
                self.input.x += -1
            if event.key == right:
                self.input.x += 1
            if event.key == up:
                self.input.y += -1
            if event.key == down:
                self.input.y += 1

        if event.type == pygame.KEYUP:
            if event.key == left:
                self.input.x -= -1
            if event.key == right:
                self.input.x -= 1
            if event.key == up:
                self.input.y -= -1
            if event.key == down:
                self.input.y -= 1

    # Moves The Player
    def movePlayer(self):
        # Move Player
        if self.input != (0, 0):
            self.movement += self.acceleration * self.input.normalize()

        self.movement *= self.drag

        self.baseRect.move_ip(self.movement.x, self.movement.y)

        # Check Bounds
        if self.baseRect.right < 0:
            self.baseRect.left = screenWidth
        if self.baseRect.left > screenWidth:
            self.baseRect.right = 0

        if self.baseRect.bottom < 0:
            self.baseRect.top = screenHeight
        if self.baseRect.top > screenHeight:
            self.baseRect.bottom = 0

    # Finds Angle To Mouse
    def getRelativeAngle(self):
        mousePos = pygame.mouse.get_pos()
        mouseX = mousePos[0]
        mouseY = mousePos[1]
        self.angle = math.degrees(math.atan2(self.rect.centery - mouseY, mouseX - self.rect.centerx))

    # Checks To See If Health Is Below Or Equal To 0
    def checkHealth(self):
        return self.health <= 0

    # Adds To Score
    def addScore(self, score):
        self.score += score

    # Returns True To Remove
    def remove(self, collidedObject, explosionList):
        self.health -= collidedObject.damage
        if self.checkHealth():
            self.removeSound.play()

            explosionList.add(PlayerExplosion((self.rect.center[0] - playerScale[0] / 2, self.rect.center[1] - playerScale[1] / 2)))

            self.kill()

    # Runs Most Needed Functions
    def update(self):
        self.movePlayer()

        self.getRelativeAngle()

        self.updateSelf()

import random

from data.code.Settings import *
from data.code.Constants import *
from data.code.FileSetup import *
from data.code.Rotatable import Rotatable


class AsteroidObject(Rotatable):
    def __init__(self, pos, imagePath, scale, angle, direction, health, speed, spinSpeed):
        super().__init__(pos, imagePath, scale, angle)

        self.radius = scale[0]/2

        self.health = health
        self.damage = self.health

        self.direction = direction

        self.speed = speed

        self.spinDirection = random.randint(1,2)
        if(self.spinDirection == 2):
            self.spinDirection = -1
        self.spinSpeed = spinSpeed

        
    # Checks To See If Health Is Below Or Equal To 0
    def checkHealth(self):
        return self.health <= 0

    # Update Function
    def update(self, deltaTime, targetFPS):
        self.move(deltaTime, targetFPS)

        self.angleSelf()

        if(self.checkBounds()):
            self.kill()

    # Override To Give More Wiggle Room
    def checkBounds(self):
        return self.baseRect.right < -200 or self.baseRect.left > screenWidth + 200 or self.baseRect.bottom < -200 or self.baseRect.top > screenHeight + 200

    # Move The Player
    def move(self, deltaTime, targetFPS):
        offsetter = self.direction * self.speed * deltaTime * targetFPS

        self.baseRect.topleft += offsetter
        
        self.angle += self.spinSpeed * self.spinDirection * deltaTime * targetFPS


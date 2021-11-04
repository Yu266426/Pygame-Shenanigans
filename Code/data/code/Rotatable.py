import pygame

from data.code.Constants import *
from data.code.GameObject import GameObject

class Rotatable(GameObject):
    def __init__(self, pos, imagePath, scale, angle):
        super().__init__(pos, imagePath, scale)

        # Save The Default Configuration
        self.baseImage = self.image.copy()
        self.baseRect = self.rect.copy()

        self.angle = angle
    
    def checkBounds(self):
        return self.baseRect.right < 0 or self.baseRect.left > screenWidth or self.baseRect.bottom < 0 or self.baseRect.top > screenHeight

    def angleSelf(self):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.rect = self.image.get_rect(center = self.baseImage.get_rect(topleft = self.baseRect.topleft).center)
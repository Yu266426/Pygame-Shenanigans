import pygame

from data.code.Constants import *

class GameObject(pygame.sprite.Sprite):
    def __init__ (self, pos, imagePath, scale):
        super().__init__()
        
        # Loads Image, And Makes Rect From Image
        self.image = pygame.image.load(imagePath).convert_alpha()
        self.image = pygame.transform.scale(self.image, scale)

        self.rect = self.image.get_rect(topleft = pos)
    
    def checkBounds(self):
        return self.rect.right < 0 or self.rect.left > screenWidth or self.rect.bottom < 0 or self.rect.top > screenHeight

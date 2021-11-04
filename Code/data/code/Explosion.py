import pygame
import os

class Explosion(pygame.sprite.Sprite):
    def __init__ (self, pos, maxFrame, scale, FRAME_PATH):
        super().__init__()

        self.frame = -1
        self.maxFrame = maxFrame

        self.images = []
        for i in range(0,self.maxFrame):
            img = pygame.image.load(os.path.join(FRAME_PATH, str(i) + ".png")).convert_alpha()
            img = pygame.transform.scale(img, scale)
            self.images.append(img)
        
        self.image = self.images[0]

        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self):
        self.frame += 1

        self.image = self.images[self.frame]
        
        self.rect = self.image.get_rect(topleft = self.rect.topleft)

        if(self.frame >= self.maxFrame - 1):
            self.kill()
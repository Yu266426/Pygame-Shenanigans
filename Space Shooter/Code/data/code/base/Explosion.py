import pygame

from data.code.base.Constants import animationSpeed


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, explosionSequence):
        super().__init__()

        self.frame = 0

        self.images = explosionSequence

        self.image = self.images[0]

        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        self.frame += animationSpeed

        self.image = self.images[int(self.frame)]

        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        if self.frame >= len(self.images) - 1:
            self.kill()

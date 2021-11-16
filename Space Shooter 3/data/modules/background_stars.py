import pygame
from data.modules.game_object import GameObject


class BackgroundStar(GameObject):
    def __init__(self, pos, size):
        # Premake image
        self.size = size

        image = pygame.Surface((size, size))
        image.fill((255, 255, 255))

        super().__init__(pos, image)

    def move(self, scroll):
        self.rect = self.pos - scroll*(self.size / 10)

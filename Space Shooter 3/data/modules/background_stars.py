import pygame
from data.modules.game_object import GameObject


class BackgroundStar(GameObject):
    def __init__(self, pos, size, bounds):
        # Premake image
        self.size = size

        image = pygame.Surface((size, size))
        image.fill((255, 255, 255))

        super().__init__(pos, image)

        self.bounds = bounds

    def move(self, scroll):
        self.rect.center = self.pos - scroll*(self.size / 10)

    def update(self, scroll, screen_size):
        self.move(scroll)

        # Make stars loop
        if self.rect.center[0] >= screen_size[0] + 200:
            self.pos.x -= screen_size[0] + 200
        elif self.rect.center[0] <= -200:
            self.pos.x += screen_size[0] + 200

        if self.rect.center[1] >= screen_size[1] + 200:
            self.pos.y -= screen_size[0] + 200
        elif self.rect.center[1] <= -200:
            self.pos.y += screen_size[1] + 200

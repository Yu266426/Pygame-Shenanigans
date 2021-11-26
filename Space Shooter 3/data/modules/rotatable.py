import pygame

from data.modules.game_object import GameObject


class Rotatable(GameObject):
    def __init__(self, pos, image):
        super().__init__(pos, image)

        # Save The Default Configuration
        self.base_image = self.image.copy()
        self.base_rect = self.rect.copy()

        self.angle = 0

    def angle_self(self):
        self.image = pygame.transform.rotate(self.base_image, self.angle)

    def update_rect(self):
        self.rect = self.image.get_rect(center=self.base_image.get_rect(topleft=self.base_rect.topleft).center)

    def update_angle(self):
        self.angle_self()
        self.update_rect()

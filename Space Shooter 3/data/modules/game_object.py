import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()

        self.image = image.convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(pos[0], pos[1])

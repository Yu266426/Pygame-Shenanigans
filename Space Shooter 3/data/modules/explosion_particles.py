import pygame
import random

from data.modules.game_object import GameObject


colour_palette = {"large_asteroid": [(235, 143, 30), (235, 62, 14), (255, 208, 54)], "laser": [(252, 207, 3), (255, 248, 43), (255, 166, 0)]}


class ExplosionParticle(GameObject):
    def __init__(self, pos, scale, speed, decay_rate, particle_type):
        # Make image to pass into initialization
        image = pygame.Surface((scale, scale))
        image.fill(colour_palette[particle_type][random.randint(0, len(colour_palette[particle_type]) - 1)])

        # Initialize
        super().__init__(pos, image)

        # Position
        self.pos = pygame.math.Vector2(pos[0], pos[1])

        self.scale = float(scale)
        self.decay_rate = decay_rate

        self.movement = pygame.math.Vector2(1, 1)
        self.movement.normalize_ip()
        self.movement *= speed
        self.movement.rotate_ip(float(random.randint(0, 360 * 4)) / 4)

    def move(self, delta, scroll):
        # Move
        self.pos += self.movement * delta

        # Change angle slightly
        self.movement.rotate_ip(float(random.randint(-8, 8)) / 2)

        self.scale -= self.decay_rate * delta

        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos - scroll

    def update(self, delta, scroll):
        self.move(delta, scroll)

        if self.scale <= 2:
            self.kill()

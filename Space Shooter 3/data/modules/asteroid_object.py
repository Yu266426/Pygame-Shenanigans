from data.modules.helper import get_movement, check_distance
from data.modules.rotatable import Rotatable


class AsteroidObject(Rotatable):
    def __init__(self, pos, image, direction, speed, spin_speed, health, damage, delete_range=2000):
        super().__init__(pos, image)

        self.angle = 0
        self.direction = direction

        self.movement = get_movement(direction, speed)

        self.spin_speed = spin_speed

        self.radius = self.image.get_width() / 2

        self.delete_range = delete_range

        self.health = health
        self.damage = damage

    def move(self, delta, scroll):
        self.pos += self.movement * delta
        self.base_rect.center = self.pos - scroll
        self.update_rect()

        self.angle += self.spin_speed * delta

    def update(self, delta, scroll, player_pos, display):
        # Only update angle if it is visible
        if self.rect.colliderect(display):
            self.angle_self()

        self.move(delta, scroll)

        if check_distance(self.pos, player_pos, self.delete_range):
            self.kill()

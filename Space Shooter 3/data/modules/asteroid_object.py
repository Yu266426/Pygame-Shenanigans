from data.modules.rotatable import Rotatable
from data.modules.helper import get_movement, check_distance


class AsteroidObject(Rotatable):
    def __init__(self, pos, image, direction, speed, spinSpeed, health):
        super().__init__(pos, image)

        self.angle = 0

        self.movement = get_movement(direction, speed)

        self.spinSpeed = spinSpeed

        self.radius = self.image.get_width() / 2 

        self.health = health

    def move(self, delta, scroll):
        self.pos += self.movement * delta
        self.base_rect.center = self.pos - scroll

        self.angle += 1 * delta

    def update(self, delta, scroll, player):
        self.move(delta, scroll)

        self.update_angle()

        if check_distance(self.pos, player.pos, 2000):
            self.kill()

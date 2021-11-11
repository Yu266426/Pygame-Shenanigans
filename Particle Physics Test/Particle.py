import pygame.math


class Particle:
    def __init__(self, pos, direction, scale):
        self.pos = pygame.math.Vector2(pos)

        self.direction = pygame.math.Vector2(direction)

        self.scale = scale

    def moveX(self, delta, rects):
        self.pos.x += self.direction.x * delta
        for rect in rects:
            if rect.collidepoint(self.pos):
                self.direction.x = -0.8 * self.direction.x
                self.direction.y *= 0.95
                self.pos.x += self.direction.x * 1.2 * delta

    def moveY(self, delta, rects):
        self.pos.y += self.direction.y * delta
        for rect in rects:
            if rect.collidepoint(self.pos):
                self.direction.y = -0.8 * self.direction.y
                self.direction.x *= 0.95
                self.pos.y += self.direction.y * 1.2 * delta

    def update(self, delta, rects):
        self.direction.y += 0.35 * delta

        self.moveX(delta, rects)

        self.moveY(delta, rects)

        self.scale -= 0.01

    def draw(self, drawSurface):
        pygame.draw.circle(drawSurface, (255, 255, 255), self.pos, self.scale)
